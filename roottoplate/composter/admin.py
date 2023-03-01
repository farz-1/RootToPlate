from django.contrib import admin
from django.contrib.auth.models import User
from composter.models import InputType, Input, InputEntry, TemperatureEntry, RestaurantRequest, Output, EnergyUsage


class InputInline(admin.TabularInline):
    model = Input
    list_display = ('inputType', 'InputAmount')


class InputEntryAdmin(admin.ModelAdmin):
    list_display = ('entryTime', 'user', 'notes')
    inlines = [InputInline]


# show user activity under user
class InputEntryInline(admin.TabularInline):
    model = InputEntry
    list_display = ('entryTime', 'notes', 'inputs')

    def inputs(self, obj):
        return [x.inputType for x in Input.objects.filter(inputEntry=obj.entryId)]


class OutputEntryInline(admin.TabularInline):
    model = Output
    list_display = ('time', 'amount', 'notes')


class TemperatureEntryInline(admin.TabularInline):
    model = TemperatureEntry
    list_display = ('entryTime', 'probe1', 'probe2', 'probe3', 'probe4', 'notes')


class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('username', 'first_name', 'last_name', 'last_login', 'is_staff', 'is_superuser')
    inlines = [InputEntryInline, OutputEntryInline, TemperatureEntryInline]


class TypeAddedInline(admin.TabularInline):
    model = Input
    list_display = ('entry_time', 'user', 'inputAmount')

    def entry_time(self, obj):
        x = InputEntry.objects.filter(entryID=obj.inputEntry)
        if x is not None:
            return x.get('entryTime')
        return 'IntegrityError'

    def user(self, obj):
        x = InputEntry.objects.filter(entryID=obj.inputEntry)
        if x is not None:
            return x.get('user')
        return 'IntegrityError'


class InputTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'CNRatio', 'nitrogenPercent', 'moisturePercent')
    inlines = [TypeAddedInline]


class TemperatureEntryAdmin(admin.ModelAdmin):
    list_display = ('entryTime', 'user', 'probe1', 'probe2', 'probe3', 'probe4', 'notes')


class OutputAdmin(admin.ModelAdmin):
    list_display = ('time', 'user', 'amount', 'notes')


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'dateRequested', 'deadlineDate', 'collected')


class EnergyAdmin(admin.ModelAdmin):
    list_display = ('date', 'gas', 'electricity')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(InputType, InputTypeAdmin)
admin.site.register(InputEntry, InputEntryAdmin)
admin.site.register(TemperatureEntry, TemperatureEntryAdmin)
admin.site.register(RestaurantRequest, RestaurantAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(EnergyUsage, EnergyAdmin)
