from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from datetime import date


class InputType(models.Model):
    NAME_MAX_LENGTH = 128
    RATIO_DECIMAL_PLACES = 2
    RATIO_MAX_DIGITS = 5

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True, validators=[MinLengthValidator(2)])
    woodChipRatio = models.DecimalField(decimal_places=RATIO_DECIMAL_PLACES, max_digits=RATIO_MAX_DIGITS,
                                        validators=[MinValueValidator(1)])
    CNRatio = models.DecimalField(decimal_places=RATIO_DECIMAL_PLACES, max_digits=RATIO_MAX_DIGITS,
                                  validators=[MinValueValidator(1)])

    def __str__(self):
        return self.name


class InputEntry(models.Model):
    NOTES_MAX_LENGTH = 2048

    entryID = models.IntegerField(unique=True)
    entryTime = models.DateTimeField()
    notes = models.CharField(max_length=NOTES_MAX_LENGTH, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Input entries'

    def __str__(self):
        return str(self.entryID)


class Input(models.Model):
    INPUT_DECIMAL_PLACES = 2
    INPUT_MAX_DIGITS = 5

    inputEntry = models.ForeignKey(InputEntry, on_delete=models.CASCADE, null=True)
    inputType = models.ForeignKey(InputType, on_delete=models.CASCADE)
    inputAmount = models.DecimalField(decimal_places=INPUT_DECIMAL_PLACES, max_digits=INPUT_MAX_DIGITS,
                                      validators=[MinValueValidator(0)])


class TemperatureEntry(models.Model):
    NOTES_MAX_LENGTH = 2048
    TEMP_DECIMAL_PLACES = 2
    TEMP_MAX_DIGITS = 5

    entryID = models.IntegerField(unique=True)
    entryTime = models.DateTimeField()
    probe1 = models.DecimalField(decimal_places=TEMP_DECIMAL_PLACES, max_digits=TEMP_MAX_DIGITS,
                                 validators=[MinValueValidator(-40), MaxValueValidator(150)])
    probe2 = models.DecimalField(decimal_places=TEMP_DECIMAL_PLACES, max_digits=TEMP_MAX_DIGITS,
                                 validators=[MinValueValidator(-40), MaxValueValidator(150)])
    probe3 = models.DecimalField(decimal_places=TEMP_DECIMAL_PLACES, max_digits=TEMP_MAX_DIGITS,
                                 validators=[MinValueValidator(-40), MaxValueValidator(150)])
    probe4 = models.DecimalField(decimal_places=TEMP_DECIMAL_PLACES, max_digits=TEMP_MAX_DIGITS,
                                 validators=[MinValueValidator(-40), MaxValueValidator(150)])
    notes = models.CharField(max_length=NOTES_MAX_LENGTH, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = 'Temperature entries'

    def __str__(self):
        return str(self.entryID)


class UserProfile(User):
    # user contains username, firstname, lastname, email, password
    isAdmin = models.BooleanField()

    def __str__(self):
        return self.user.username


class RestaurantRequest(models.Model):
    NAME_MAX_LENGTH = 128
    ADDRESS_MAX_LENGTH = 1024
    EMAIL_MAX_LENGTH = 128
    NOTES_MAX_LENGTH = 20048

    requestID = models.IntegerField(unique=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH)
    address = models.CharField(max_length=ADDRESS_MAX_LENGTH)
    dateRequested = models.DateTimeField()
    deadlineDate = models.DateTimeField(validators=[MinValueValidator(limit_value=date.today)])
    email = models.CharField(max_length=EMAIL_MAX_LENGTH)
    phoneNumber = models.IntegerField()
    notes = models.CharField(max_length=NOTES_MAX_LENGTH, null=True, blank=True)
    numberOfBags = models.IntegerField()
    collected = models.BooleanField(default=False)

    def __str__(self):
        return str(self.requestID)


class Output(models.Model):
    NOTES_MAX_LENGTH = 2048
    OUTPUT_DECIMAL_PLACES = 2
    OUTPUT_MAX_DIGITS = 5

    outputID = models.IntegerField(unique=True)
    amount = models.DecimalField(decimal_places=OUTPUT_DECIMAL_PLACES, max_digits=OUTPUT_MAX_DIGITS)
    time = models.DateTimeField()
    notes = models.CharField(max_length=NOTES_MAX_LENGTH, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.outputID)
