from django import forms
from .models import DeviceActivationLog

class UpdateStateForm(forms.ModelForm):
    class Meta:
        model = DeviceActivationLog
        fields = ('measure',)
