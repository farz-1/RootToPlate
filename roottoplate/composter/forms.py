from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from composter.models import InputType, InputEntry, Input, TemperatureEntry, UserProfile, RestaurantRequest, Output
import datetime


class UserForm(UserCreationForm):
    # accessible by admin only
    isAdmin = forms.BooleanField(required=True)

    class Meta:
        model = UserProfile
        fields = {'username',
                  'first_name', 'last_name',
                  'password1',
                  'password2',
                  'isAdmin'}


class UserLoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = {'username', 'password'}


class ChangePasswordForm(forms.ModelForm):
    # accessible by admin only
    username = forms.CharField()  # needs some validation
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = {'username', 'password'}


class InputTypeForm(forms.ModelForm):
    # accessible by admin only
    name = forms.CharField(required=True)
    woodChipRatio = forms.DecimalField()
    CNRatio = forms.DecimalField()

    class Meta:
        model = InputType
        fields = {'name', 'CNRatio'}  # is the wood_chip calculated or input?


class InputEntryForm(forms.ModelForm):
    entryTime = forms.DateTimeField(initial=datetime.date.today(), required=True)  # filled with current time, can be amended
    notes = forms.CharField()

    class Meta:
        model = InputEntry
        fields = {'entryTime', 'notes'}


# the idea is that a variable number of this form
# appears on the same page as the InputEntryForm and then is dealt with in the view
class InputForm(forms.ModelForm):
    inputType = forms.ModelChoiceField(queryset=InputType.objects.all(), required=True)
    inputAmount = forms.DecimalField()

    class Meta:
        model = Input
        fields = {'inputType', 'inputAmount'}


class TempEntryForm(forms.ModelForm):
    entryTime = forms.DateTimeField(initial=datetime.date.today(), required=True)  # filled with current time, can be amended
    probe1 = forms.DecimalField(required=True)
    probe2 = forms.DecimalField(required=True)
    probe3 = forms.DecimalField(required=True)
    probe4 = forms.DecimalField(required=True)
    notes = forms.CharField()

    class Meta:
        model = TemperatureEntry
        fields = {'entryTime', 'probe1', 'probe2', 'probe3', 'probe4', 'notes'}


class RestaurantForm(forms.ModelForm):
    name = forms.CharField(required=True)
    address = forms.CharField(required=True)
    dateRequested = forms.DateTimeField(initial=datetime.date.today())
    deadlineDate = forms.DateTimeField(initial=datetime.date.today() + datetime.timedelta(weeks=1), required=True)
    email = forms.CharField(required=True)
    phoneNumber = forms.IntegerField()
    notes = forms.CharField()
    numberOfBags = forms.IntegerField()

    class Meta:
        model = RestaurantRequest
        exclude = {'dateRequested'}


class OutputForm(forms.ModelForm):
    amount = forms.DecimalField(required=True)
    time = forms.DateTimeField(initial=datetime.date.today(), required=True)
    notes = forms.CharField()

    class Meta:
        model = Output
        fields = {'amount', 'time', 'notes'}
