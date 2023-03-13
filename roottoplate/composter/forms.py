from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from composter.models import InputType, InputEntry, Input, TemperatureEntry, RestaurantRequest, Output, EnergyUsage
from crispy_forms.helper import FormHelper
from datetime import date
import datetime


class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = [(day, day) for day in range(1, 32)]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in range(2000, 2100)]
        widgets = [
            forms.Select(attrs=attrs, choices=days),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split('-')
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        return '{}-{}-{}'.format(year, month, day)


class UserForm(UserCreationForm):
    # accessible by admin only
    add_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = User
        fields = {'username',
                  'first_name', 'last_name',
                  'password1',
                  'password2',
                  'is_staff'}


class UserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = {'username', 'password'}


class ChangePasswordForm(forms.ModelForm):
    # accessible by admin only
    username = forms.CharField(required=True)  # needs some validation
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    change_password = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['username'].help_text = "The username of the user"
        self.fields['password'].help_text = "New password for the username"
        self.fields['change_password'].help_text = ""

    class Meta:
        model = User
        fields = {'username', 'password'}


class InputTypeForm(forms.ModelForm):
    # accessible by admin only
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    CNRatio = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}),
                                 required=True, label='Carbon : Nitrogen ratio')
    nitrogenPercent = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}),
                                         required=True, label='Nitrogen percentage')
    moisturePercent = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}),
                                         required=True, label='Moisture percentage')
    add_input_type = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        super(InputTypeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].help_text = "Type of material to be added"
        self.fields['CNRatio'].help_text = "Carbon nitrogen ratio of the material"

    class Meta:
        model = InputType
        fields = {'name', 'CNRatio', 'nitrogenPercent', 'moisturePercent'}


class InputEntryForm(forms.ModelForm):
    entryTime = forms.DateTimeField(initial=datetime.datetime.today, label='Time',
                                    widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))

    def __init__(self, *args, **kwargs):
        super(InputEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['entryTime'].help_text = "Time and date when the measurement was taken"
        self.fields['notes'].help_text = "Additional notes"

    class Meta:
        model = InputEntry
        fields = {'entryTime', 'notes'}


# the idea is that a variable number of this form
# appears on the same page as the InputEntryForm and then is dealt with in the view
class InputForm(forms.ModelForm):
    inputType = forms.ModelChoiceField(widget=forms.Select(attrs={'placeholder': 'Required Field'}),
                                       queryset=InputType.objects.all(), required=True, label='Input type')
    inputAmount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}),
                                     required=True, label='Input amount')

    def __init__(self, *args, **kwargs):
        super(InputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['inputType'].help_text = "Type of material added"
        self.fields['inputAmount'].help_text = "Amount of material added in litres/kg"

    class Meta:
        model = Input
        fields = {'inputType', 'inputAmount'}


InputFormSet = forms.formsets.formset_factory(InputForm, extra=1, max_num=5)


class TempEntryForm(forms.ModelForm):
    entryTime = forms.DateTimeField(initial=datetime.datetime.today, label='Time',
                                    widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)

    probe1 = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True,
                                label='Probe 1')
    probe2 = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True,
                                label='Probe 2')
    probe3 = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True,
                                label='Probe 3')
    probe4 = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True,
                                label='Probe 4')
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))

    def __init__(self, *args, **kwargs):
        super(TempEntryForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['entryTime'].help_text = "Time and date when the measurement was taken"
        self.fields['probe1'].help_text = "Temperature for Probe 1 in Degrees Celsius"
        self.fields['probe2'].help_text = "Temperature for Probe 2 in Degrees Celsius"
        self.fields['probe3'].help_text = "Temperature for Probe 3 in Degrees Celsius"
        self.fields['probe4'].help_text = "Temperature for Probe 4 in Degrees Celsius"
        self.fields['notes'].help_text = "Additional notes"

    class Meta:
        model = TemperatureEntry
        fields = {'entryTime', 'probe1', 'probe2', 'probe3', 'probe4', 'notes'}


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Required Field', 'rows': '3'}),
                              required=True)
    dateRequested = forms.DateTimeField(initial=datetime.datetime.now, required=False)
    deadlineDate = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                       initial=datetime.datetime.now() + datetime.timedelta(weeks=1), required=True,
                                       label='Last date to be picked up')
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Required Field'}), required=True)
    phoneNumber = forms.IntegerField(required=False, label='Phone number',
                                     widget=forms.TextInput(attrs={'placeholder': 'Enter 0 to leave empty'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))
    numberOfBags = forms.IntegerField(required=False, label='Number of bags of food waste',
                                      widget=forms.NumberInput(attrs={'placeholder': 'Enter 0 if unknown'}))

    def __init__(self, *args, **kwargs):
        super(RestaurantForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['name'].help_text = "Name of the restaurant"
        self.fields['address'].help_text = "Address of the restaurant"
        self.fields['dateRequested'].help_text = "Deadline date"
        self.fields['email'].help_text = "Email to be contacted"
        self.fields['phoneNumber'].help_text = "Phone number to be contacted"
        self.fields['notes'].help_text = "Additional notes"
        self.fields['numberOfBags'].help_text = "Number of bags to be collected"

    class Meta:
        model = RestaurantRequest
        exclude = {'dateRequested'}


class OutputForm(forms.ModelForm):
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True)
    time = forms.DateTimeField(initial=datetime.datetime.today,
                               widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))

    def __init__(self, *args, **kwargs):
        super(OutputForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['time'].help_text = "Time and date when the measurement was taken"
        self.fields['amount'].help_text = "Amount of composter material taken out"
        self.fields['notes'].help_text = "Additional notes"

    class Meta:
        model = Output
        fields = {'amount', 'time', 'notes'}


class EnergyForm(forms.ModelForm):
    date = forms.DateField(initial=date.today, widget=forms.DateInput(attrs={'type': 'date'}),
                           required=True)
    gas = forms.IntegerField(required=True)
    electricity = forms.IntegerField(required=True)
    add_meter_reading = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    def __init__(self, *args, **kwargs):
        super(EnergyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['date'].help_text = "Time when the measurement was taken"
        self.fields['gas'].help_text = "Gas reading"
        self.fields['electricity'].help_text = "Electricity reading"

    class Meta:
        model = EnergyUsage
        fields = {'date', 'gas', 'electricity'}
