from django.db import models
from datetime import datetime


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, **kwargs):
        self.deleted_at = datetime.now()
        self.save()


class Messages(BaseModel):
    """收发消息表"""
    RECEIVED = 0
    SENT = 1
    DEVICE_ACTIVATION = "webApp/actuator"
    TEMPERATURE_MEASURES = "DHT22/temperature"
    HUMIDITY_MEASURES = "DHT22/humidity"
    # RELAY_MEASURES = "monitoring/relay"

    Status = (
        (RECEIVED, 'Received'),
        (SENT, 'Sent')
    )

    topic = models.CharField(max_length=255)
    device = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    type = models.IntegerField(choices=Status, default=None)

    def save(self, **kwargs):
        super(Messages, self).save()

        if self.topic == self.DEVICE_ACTIVATION:
            DeviceActivationLog.objects.create(
                device=self.device,
                measure=self.message,
                message=self
            )
        elif self.topic == self.TEMPERATURE_MEASURES:
            TemperatureMeasures.objects.create(
                device=self.device,
                measure=self.message,
                message=self
            )
        elif self.topic == self.HUMIDITY_MEASURES:
            HumidityMeasures.objects.create(
                device=self.device,
                measure=self.message,
                message=self
            )



class TemperatureMeasures(BaseModel):
    """温度测量值"""
    device = models.CharField(max_length=255)
    measure = models.DecimalField(decimal_places=3, max_digits=7)
    message = models.ForeignKey(Messages, on_delete=models.PROTECT, default=None)


class HumidityMeasures(BaseModel):
    """湿度测量值"""
    device = models.CharField(max_length=255)
    measure = models.DecimalField(decimal_places=3, max_digits=7)
    message = models.ForeignKey(Messages, on_delete=models.PROTECT, default=None)


class DeviceActivationLog(BaseModel):
    """设备行为日志"""
    device = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)
    message = models.ForeignKey(Messages, on_delete=models.PROTECT, default=None)

   # def update_state(self, current_state):
        # toggle
    #    return not current_state
