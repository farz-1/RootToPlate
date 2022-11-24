from django.db import models
from django.contrib.auth.models import User


class InputType(models.Model):
    NAME_MAX_LENGTH = 128
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    factor = models.DecimalField(decimal_places=2, max_digits=5)

    def __str__(self):
        return self.inputType


class DataEntry(models.Model):
    NOTES_MAX_LENGTH = 2048
    INPUT_NAME_MAX_LENGTH = 128
    entryID = models.IntegerField(unique=True)
    entryTime = models.DateTimeField()
    temperature1 = models.DecimalField(decimal_places=2, max_digits=5)
    temperature2 = models.DecimalField(decimal_places=2, max_digits=5)
    inputType = models.ForeignKey(InputType, max_length=INPUT_NAME_MAX_LENGTH, on_delete=models.SET_NULL, null=True)
    inputAmount = models.IntegerField()
    notes = models.CharField(max_length=NOTES_MAX_LENGTH)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.entryID


class UserProfile(models.Model):
    # user contains username, firstname, lastname, email, password
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
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
    deadlineDate = models.DateTimeField()
    email = models.CharField(max_length=EMAIL_MAX_LENGTH)
    phoneNumber = models.IntegerField()
    notes = models.CharField(max_length=NOTES_MAX_LENGTH)
    numberOfBags = models.IntegerField()
    collected = models.BooleanField(default=False)

    def __str__(self):
        return self.requestID
