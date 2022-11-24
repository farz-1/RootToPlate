from django.contrib import admin
from composter.models import InputType, DataEntry, UserProfile, RestaurantRequest

admin.site.register(InputType)
admin.site.register(DataEntry)
admin.site.register(UserProfile)
admin.site.register(RestaurantRequest)
