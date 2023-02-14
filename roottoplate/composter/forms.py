from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from composter.models import InputType, InputEntry, Input, TemperatureEntry, RestaurantRequest, Output, EnergyUsage
from datetime import date, datetime, timedelta


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

    class Meta:
        model = User
        fields = {'username', 'password'}


class InputTypeForm(forms.ModelForm):
    # accessible by admin only
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    woodChipRatio = forms.DecimalField(required=False)
    CNRatio = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}),
                                 required=True, label='Carbon : Nitrogen ratio')
    add_input_type = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = InputType
        fields = {'name', 'CNRatio'}  # is the wood_chip calculated or input?


class InputEntryForm(forms.ModelForm):
    entryTime = forms.DateTimeField(initial=datetime.datetime.today, label='Time',
                                    widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))

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

    class Meta:
        model = Input
        fields = {'inputType', 'inputAmount'}


InputFormSet = forms.formsets.formset_factory(InputForm, extra=1, max_num=5)


class TempEntryForm(forms.ModelForm):
    entryTime = forms.DateTimeField(initial=datetime.datetime.today, label='Time',
                                    widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    probe1 = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True, label='Probe 1')
    probe2 = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True, label='Probe 2')
    probe3 = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True, label='Probe 3')
    probe4 = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True, label='Probe 4')
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))

    class Meta:
        model = TemperatureEntry
        fields = {'entryTime', 'probe1', 'probe2', 'probe3', 'probe4', 'notes'}


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Required Field', 'rows': '3'}), required=True)
    dateRequested = forms.DateTimeField(initial=datetime.datetime.now, required=False)
    deadlineDate = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                       initial=datetime.datetime.now() + datetime.timedelta(weeks=1), required=True,
                                       label='Last date to be picked up')
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Required Field'}), required=True)
    phoneNumber = forms.IntegerField(required=False, label='Phone number')
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))
    numberOfBags = forms.IntegerField(required=False, label='Number of bags of food waste')

    class Meta:
        model = RestaurantRequest
        exclude = {'dateRequested'}


class OutputForm(forms.ModelForm):
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Required Field'}), required=True)
    time = forms.DateTimeField(initial=datetime.datetime.today,
                               widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': '2'}))

    class Meta:
        model = Output
        fields = {'amount', 'time', 'notes'}


class EnergyForm(forms.ModelForm):
    date = forms.DateField(initial=date.today, widget=DateSelectorWidget(), required=True)
    gas = forms.IntegerField(required=True)
    electricity = forms.IntegerField(required=True)
    add_meter_reading = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = EnergyUsage
        fields = {'date', 'gas', 'electricity'}
