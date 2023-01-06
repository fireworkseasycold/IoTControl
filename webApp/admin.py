from django.contrib import admin
from webApp import models
# Register your models here.
admin.site.register(models.DeviceActivationLog)
admin.site.register(models.HumidityMeasures)
admin.site.register(models.Messages)
admin.site.register(models.TemperatureMeasures)