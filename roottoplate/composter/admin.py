from django.contrib import admin
from composter.models import InputType, Input, InputEntry, TemperatureEntry, UserProfile, RestaurantRequest, Output

admin.site.register(InputType)
admin.site.register(Input)
admin.site.register(InputEntry)
admin.site.register(TemperatureEntry)
admin.site.register(UserProfile)
admin.site.register(RestaurantRequest)
admin.site.register(Output)
