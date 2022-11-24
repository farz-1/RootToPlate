from django.db import models
from django.contrib.auth.models import User


class Input(models.Model):
    NAME_MAX_LENGTH = 128
    inputType = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    inputAmount = models.IntegerField()
    date = models.DateTimeField()


class DataEntry(models.Model):
    NOTES_MAX_LENGTH = 2048
    entryTime = models.DateTimeField()
    temperature1 = models.DecimalField()
    temperature2 = models.DecimalField()
    notes = models.CharField(max_length=NOTES_MAX_LENGTH)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    isAdmin = models.BooleanField()


class RestaurantRequest(models.Model):
    name = models.CharField()
    address = models.CharField()
    dateRequested = models.DateTimeField()
    deadlineDate = models.DateTimeField()
    email = models.CharField()
    phoneNumber = models.IntegerField()
    notes = models.CharField()
    numberOfBags = models.IntegerField()
    collected = models.BooleanField(default=False)
