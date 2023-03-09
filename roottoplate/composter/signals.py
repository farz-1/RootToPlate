from django.db.models.signals import post_save
from django.dispatch import receiver
from composter.models import *
import datetime


class GraphState:
    _instance = None
    typeNames = []
    typePercentages = []
    tempEntries = []
    tempTimes = []
    tempTimesInt = []
    cMonth = None
    cYear = None
    notEnoughEnergyInfo = True

    def __new__(self):
        if self._instance is None:
            self._instance = super(GraphState, self).__new__(self)
            self._instance.calculate_type_percentages()
            self._instance.calculate_carbon_neutrality()
            self._instance.calculate_temperatures()
        return self._instance

    def calculate_carbon_neutrality(self):
        def get_inputs_from_entry(entryid):
            return Input.objects.filter(inputEntry=entryid)


        def sum_amounts_from_entries(entry_set):
            return sum([sum([y.inputAmount for y in get_inputs_from_entry(x.entryID)]) for x in entry_set])
        
        def calculate_carbon():
            cubic_m_to_co2 = 1.9  # kg / m^3
            kwh_to_co2 = 0.082  # edf co2 kg/kwh as taken from their website
            compost_to_co2_saved = 1.495  # kg/kg, assuming food waste would be landfilled otherwise
            labels = ['This Month', 'Last Month', 'This Year']
            carbon = {label: {'cPositive': None, 'cNegative': None} for label in labels}

            this_month = datetime.date.today().replace(day=1)
            last_month = this_month - datetime.timedelta(days=1)
            start_of_this_year = datetime.date.today() - datetime.timedelta(days=365)

            meter_readings = EnergyUsage.objects.filter(date__gte=start_of_this_year).order_by('-date').values()
            if len(meter_readings) > 1:
                dates = [x.get('date') for x in meter_readings]
                elec = [x.get('electricity') for x in meter_readings]
                gas = [x.get('gas') for x in meter_readings]

                lm_factor = 30 / (dates[0] - dates[1]).days
                lm_elec = (elec[0] - elec[1]) * lm_factor
                lm_gas = (gas[0] - gas[1]) * lm_factor

                carbon[labels[0]]['cPositive'] = int(lm_elec * kwh_to_co2 + lm_gas * cubic_m_to_co2)
                # this is the same as the last month
                carbon[labels[1]]['cPositive'] = int(lm_elec * kwh_to_co2 + lm_gas * cubic_m_to_co2)

                ty_factor = 365 / (dates[0] - dates[-1]).days
                ty_elec = (elec[0] - elec[-1]) * ty_factor
                ty_gas = (gas[0] - gas[-1]) * ty_factor

                carbon[labels[2]]['cPositive'] = int(ty_elec * kwh_to_co2 + ty_gas * cubic_m_to_co2)

                # and le composting
                tm_compost = InputEntry.objects.filter(entryTime__month=this_month.month,
                                               entryTime__year=this_month.year)
                lm_compost = InputEntry.objects.filter(entryTime__month=last_month.month,
                                               entryTime__year=last_month.year)
                ty_compost = InputEntry.objects.filter(entryTime__year=this_month.year)
                for label, entry_set in {'This Month': tm_compost, 'Last Month': lm_compost, 'This Year': ty_compost}.items():
                    compost_total = sum_amounts_from_entries(entry_set)
                    carbon[label]['cNegative'] = int(float(compost_total) * compost_to_co2_saved)
                return carbon
            else:
                return None
    
        mLabels, mPositive, mNegative = [], [], []
        yLabels, yPositive, yNegative = [], [], []
        carbon = calculate_carbon()
        if carbon is None:
            self.notEnoughEnergyInfo = True
        else:
            self.notEnoughEnergyInfo = False
            for label, value in carbon.items():
                if label == 'This Year':
                    yLabels, yPositive, yNegative = [label], [value['cPositive']], [value['cNegative']]
                else:
                    mLabels.append(label)
                    mPositive.append(value['cPositive'])
                    mNegative.append(value['cNegative'])

        self.cMonth = {'label': mLabels, 'positive': mPositive, 'negative': mNegative}
        self.cYear = {'label': yLabels, 'positive': yPositive, 'negative': yNegative}

    def calculate_type_percentages(self):
        self.typeNames = [x.name for x in InputType.objects.all()]
        typeCounts = [float(sum(y.inputAmount for y in Input.objects.filter(inputType=x))) for x in self.typeNames]
        total = float(sum(typeCounts))
        self.typePercentages = [(count / total * 100)for count in typeCounts]
        n = len(self.typeNames) - 1
        for i in range(n + 1):
            if typeCounts[n-i] == 0:
                del typeCounts[n-i]
                del self.typeNames[n-i]
                del self.typePercentages[n-i]

    def calculate_temperatures(self):
        self.tempEntries = TemperatureEntry.objects.all().order_by('entryTime').values()
        if len(self.tempEntries) > 30:
            self.tempEntries = self.tempEntries[len(self.tempEntries)-30:]

        self.tempTimes = [x.get('entryTime').strftime("%d-%m-%Y") for x in self.tempEntries]
        self.tempTimesInt = [int(x.get('entryTime').timestamp()) for x in self.tempEntries]

@receiver(post_save, sender=InputEntry)
@receiver(post_save, sender=EnergyUsage)
def update_carbon_neutrality(sender, **kwargs):
    state = GraphState()
    state.calculate_carbon_neutrality()

@receiver(post_save, sender=TemperatureEntry)
def update_temperatues(sender, **kwargs):
    state = GraphState()
    state.calculate_temperatures()

@receiver(post_save, sender=InputEntry)
def update_input_types(sender, **kwargs):
    state = GraphState()
    state.calculate_type_percentages()

