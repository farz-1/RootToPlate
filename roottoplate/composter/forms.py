from django import forms
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from composter.models import InputType, InputEntry, Input, TemperatureEntry, RestaurantRequest, Output
import datetime

date_requested = timezone.make_aware(datetime.datetime.now(), timezone.utc)


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
    CNRatio = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    add_input_type = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = InputType
        fields = {'name', 'CNRatio'}  # is the wood_chip calculated or input?


class InputEntryForm(forms.ModelForm):
    entryTime = forms.DateTimeField(initial=date_requested,
                                    widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    notes = forms.CharField(required=False)

    class Meta:
        model = InputEntry
        fields = {'entryTime', 'notes'}


# the idea is that a variable number of this form
# appears on the same page as the InputEntryForm and then is dealt with in the view
class InputForm(forms.ModelForm):
    inputType = forms.ModelChoiceField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}),
                                       queryset=InputType.objects.all(), required=True)
    inputAmount = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)

    class Meta:
        model = Input
        fields = {'inputType', 'inputAmount'}


InputFormSet = forms.formsets.formset_factory(InputForm, extra=1, max_num=5)


class TempEntryForm(forms.ModelForm):
    entryTime = forms.DateTimeField(initial=date_requested,
                                    widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    probe1 = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    probe2 = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    probe3 = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    probe4 = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    notes = forms.CharField(required=False)

    class Meta:
        model = TemperatureEntry
        fields = {'entryTime', 'probe1', 'probe2', 'probe3', 'probe4', 'notes'}


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    dateRequested = forms.DateTimeField(initial=datetime.datetime.now(), required=False)
    deadlineDate = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}),
                                       initial=datetime.datetime.now() + datetime.timedelta(weeks=1), required=True)
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    phoneNumber = forms.IntegerField(required=False)
    notes = forms.CharField(required=False)
    numberOfBags = forms.IntegerField(required=False)

    class Meta:
        model = RestaurantRequest
        exclude = {'dateRequested'}


class OutputForm(forms.ModelForm):
    amount = forms.DecimalField(widget=forms.TextInput(attrs={'placeholder': 'Required Field'}), required=True)
    time = forms.DateTimeField(initial=date_requested,
                               widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}), required=True)
    notes = forms.CharField(required=False)

    class Meta:
        model = Output
        fields = {'amount', 'time', 'notes'}
