from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from composter.forms import InputEntryForm, InputFormSet, TempEntryForm, OutputForm, EnergyForm
from composter.forms import RestaurantForm, UserForm, InputTypeForm, ChangePasswordForm
from composter.models import InputType, Input, InputEntry, TemperatureEntry, RestaurantRequest, EnergyUsage
from django.utils import timezone
import datetime


def index(request):
    typeNames = [x.name for x in InputType.objects.all()]
    typeCounts = [float(sum(y.inputAmount for y in Input.objects.filter(inputType=x))) for x in typeNames]
    total = float(sum(typeCounts))
    percentages = [(count / total * 100)for count in typeCounts]
    n = len(typeNames) - 1
    for i in range(n + 1):
        if typeCounts[n-i] == 0:
            del typeCounts[n-i]
            del typeNames[n-i]

    tempEntries = TemperatureEntry.objects.all().order_by('entryTime').values()
    if len(tempEntries) > 30:
        tempEntries = tempEntries[-30:]

    tempTimes = [x.get('entryTime').strftime("%d-%m-%Y") for x in tempEntries]
    tempTimesInt = [int(x.get('entryTime').timestamp()) for x in tempEntries]

    context = {'typeNames': typeNames, 'typeCounts': typeCounts, 'tempEntries': tempEntries,
               'tempTimes': tempTimes, 'tempTimesInt': tempTimesInt, 'percentages': percentages}

    mLabels, mPositive, mNegative = [], [], []
    yLabels, yPositive, yNegative = [], [], []
    carbon = calculate_carbon_neutrality()
    if carbon is None:
        context['notEnoughEnergyInfo'] = 'true'
    else:
        for label, value in carbon.items():
            if label == 'This Year':
                yLabels, yPositive, yNegative = [label], [value['cPositive']], [value['cNegative']]
            else:
                mLabels.append(label)
                mPositive.append(value['cPositive'])
                mNegative.append(value['cNegative'])

    context['cMonth'] = {'label': mLabels, 'positive': mPositive, 'negative': mNegative}
    context['yMonth'] = {'label': yLabels, 'positive': yPositive, 'negative': yNegative}

    return render(request, "composter/index.html", context)


def get_inputs_from_entry(entryid):
    return Input.objects.filter(inputEntry=entryid)


def sum_amounts_from_entries(entry_set):
    return sum([sum([y.inputAmount for y in get_inputs_from_entry(x.entryID)]) for x in entry_set])


def calculate_carbon_neutrality():
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


def about(request):
    return render(request, "composter/about.html")


def composter(request):
    context = {}
    last_five_entries = InputEntry.objects.all().order_by('-entryTime').values()[:5]

    # get time the composter was last fed
    if last_five_entries:
        compost_last_fed = last_five_entries[0].get('entryTime')
        compost_last_fed_js = compost_last_fed.strftime("%Y-%m-%dT%H:%M:%SZ")
        context = {'compost_last_fed': compost_last_fed, 'compost_last_fed_js': compost_last_fed_js}

        if request.user.is_staff:
            for entry in last_five_entries:
                entry['username'] = User.objects.get(id=entry['user_id']).username
                inputs = Input.objects.filter(inputEntry=entry['entryID']).values()
                entry['inputs'] = [{'type': i.get('inputType_id'), 'amount': i.get('inputAmount')} for i in inputs]
            context['last_five_entries'] = last_five_entries

    return render(request, "composter/composter.html", context)


@csrf_protect
def user_login(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect(reverse('index'))
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            messages.error(request, "Invalid login details.")

    return render(request, 'composter/login.html')


@login_required(login_url='/composter/login/')
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def calculate_mixture_sums(cur_inputs):
    sumN = float(sum([i['amount']*i['type'].nitrogenPercent*i['type'].moisturePercent for i in cur_inputs]))
    for i in cur_inputs:
        i['carbon'] = i['type'].nitrogenPercent*i['type'].CNRatio
    sumC = float(sum([i['amount']*i['carbon']*i['type'].moisturePercent for i in cur_inputs]))
    return sumC, sumN


def calculate_recommended_addition(rec_input, sumC, sumN):
    cn = sumC/sumN
    nitrogen, moisture = rec_input.get('nitrogenPercentage'), rec_input.get('moisturePercentage')
    carbon = rec_input.get('nitrogenPercentage')*rec_input.get('CNRatio')
    return (cn*sumN - sumC) / (carbon*moisture - nitrogen*moisture*cn)


class InputFormView(TemplateView):
    template_name = "composter/compost_form.html"

    @method_decorator(login_required(login_url='/composter/login/'))
    def get(self, *args, **kwargs):
        context = {'input_formset': InputFormSet, 'entry_form': InputEntryForm()}
        return self.render_to_response(context)

    @method_decorator(login_required(login_url='/composter/login/'))
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)

        entry_form = InputEntryForm(self.request.POST)
        input_formset = InputFormSet(self.request.POST)
        context = {}

        if 'get_advice' in self.request.POST:
            cur_inputs = []
            for input in input_formset:
                input = input.save(commit=False)
                cur_inputs.append({'amount': input.inputAmount, 'type': input.inputType})
            sumC, sumN = calculate_mixture_sums(cur_inputs)
            if sumC/sumN > 35:
                rec_input = InputType.objects.filter(name='Food waste')
                rec_input_amount = calculate_recommended_addition(rec_input, sumC, sumN)
                advice = f"The carbon-nitrogen ratio of this mixture is too high. Recommended addition: roughly {rec_input_amount} of green material."  # noqa:E501
            elif sumC/sumN < 20:
                rec_input = InputType.objects.filter(name='Woodchips')
                rec_input_amount = calculate_recommended_addition(rec_input, sumC, sumN)
                advice = f"The carbon-nitrogen ratio of this mixture is too low. Recommended addition: roughly {rec_input_amount} of brown material."  # noqa:E501
            else:
                advice = "The carbon-nitrogen ratio is within the recommended range."
            tempEntries = TemperatureEntry.objects.all().order_by('entryTime').values()
            tempAvg = sum([tempEntries[-1].get(x) for x in ['probe1', 'probe2', 'probe3', 'probe4']])/4
            if tempAvg > 55:
                advice += f"\nThe temperature of the composter is above 55, add more brown material than normally recommended"
            if tempAvg < 45:
                advice+= f"\nThe temperature of the composter is below 45, add more green material than normally recommended"
            context['advice'] = advice

        elif entry_form.is_valid() and input_formset.is_valid():
            entry = entry_form.save(commit=False)
            entry.user = user
            entry.save()
            for inputs in input_formset:
                input = inputs.save(commit=False)
                input.inputEntry = entry
                input.save()
            return redirect(reverse('composter:composter'))
        else:
            print(entry_form.errors)
            for inputs in input_formset:
                print(inputs.errors)

        context['input_formset'] = input_formset
        context['entry_form'] = entry_form
        return render(request, self.template_name, context)


@login_required(login_url='/composter/login/')
def temp_entry(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        temp_form = TempEntryForm(request.POST)
        if temp_form.is_valid():
            temperature = temp_form.save(commit=False)
            temperature.user = user
            temperature.save()
            return redirect(reverse('composter:composter'))
        else:
            print(temp_form.errors)

    else:
        temp_form = TempEntryForm()
    return render(request, 'composter/temperature_form.html', {'temperature_form': temp_form})


@login_required(login_url='/composter/login/')
def output_entry(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        output_form = OutputForm(request.POST)
        if output_form.is_valid():
            output = output_form.save(commit=False)
            output.user = user
            output.save()
            return redirect(reverse('composter:composter'))
        else:
            print(output_form.errors)
    else:
        output_form = OutputForm()
    return render(request, 'composter/compost_output_form.html', {'output_form': output_form})


def restaurant_request_form(request):
    if request.user.is_authenticated:
        restaurant_notifs = RestaurantRequest.objects.all()
        return render(request, 'composter/restaurant_notifs.html', {'restaurant_notifs': restaurant_notifs})
    else:
        if request.method == "POST":
            restaurant_form = RestaurantForm(request.POST)
            if restaurant_form.is_valid():
                restaurant_req = restaurant_form.save(commit=False)
                restaurant_req.dateRequested = timezone.now()
                restaurant_req.save()
                return redirect(reverse('composter:index'))
            else:
                print(restaurant_form.errors)

        else:
            restaurant_form = RestaurantForm()
        return render(request, 'composter/restaurant_form.html', {'restaurant_form': restaurant_form})


@login_required(login_url='/composter/')
def collect_request(request, request_id):
    req = RestaurantRequest.objects.get(requestID=request_id)
    req.collected = True
    req.save()
    return redirect('composter:restaurant_form')


# admin only views
@login_required(login_url='/composter/')
def simple_admin(request):
    user = User.objects.get(username=request.user.username)
    context = {'user_form': UserForm(), 'input_type_form': InputTypeForm(),
               'change_password_form': ChangePasswordForm(), 'energy_form': EnergyForm()}
    if not user.is_staff:
        messages.error(request, "You are not authorised to access this.")
        return redirect('composter:index')
    if request.method == 'POST':
        # deal with each form and add success message if successful
        if 'add_user' in request.POST:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                context['success_message'] = f"New user {user_form.data['username']} added."
            else:
                context['user_form'] = user_form
        elif 'change_password' in request.POST:
            change_password_form = ChangePasswordForm(request.POST)
            if change_password_form.data['username'] is not None and change_password_form.data['password'] is not None:
                changed_user = User.objects.get(username=change_password_form.data['username'])
                changed_user.set_password(change_password_form.data['password'])
                changed_user.save()
                context['success_message'] = f"Password for user {change_password_form.data['username']} changed."
            else:
                context['change_password_form'] = change_password_form
        elif 'add_input_type' in request.POST:
            input_type_form = InputTypeForm(request.POST)
            if input_type_form.is_valid():
                input_type_form.save()
                context['success_message'] = f"Input type {input_type_form.data['name']} added successfully"
            else:
                context['input_type_form'] = input_type_form
        elif 'add_meter_reading' in request.POST:
            energy_form = EnergyForm(request.POST)
            if energy_form.is_valid():
                energy_form.save()
                context['success_message'] = "Meter readings taken."
            else:
                context['energy_form'] = energy_form

    return render(request, 'composter/simple_admin.html', context)
