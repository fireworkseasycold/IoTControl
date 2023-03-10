from django.http import HttpResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from json import dumps
from django.db.models import Max

from .services import get_mqtt
from .forms import UpdateStateForm
from .models import TemperatureMeasures
from .models import HumidityMeasures
from .models import DeviceActivationLog
from django.contrib.auth.decorators import login_required
# Create your views here.
# @login_required
def actuators(request):
    # return render(request, 'webApp/actuators.html')
    # relays_list = DeviceActivationLog.objects.all()
    relays_list = DeviceActivationLog.objects.all().order_by('created_at')
    # relay_latest = DeviceActivationLog.objects.all().aggregate(Max('id'))
    # print(f"MEASURE {measure}")
    relays = relays_list.filter().last()

    form = UpdateStateForm()
    context = {
        'relays_list': relays,
        'title': 'Available Relays',
        'form': form
    }
    return render(request, 'webApp/index.html', context)


def blink_led_on(request):
    mqtt = get_mqtt()

    mqtt.publish_message('webApp/actuator', 'true')

    return HttpResponse(status=200)

def blink_led_off(request):
    mqtt = get_mqtt()

    mqtt.publish_message('webApp/actuator', 'false')

    return HttpResponse(status=200)

def temperature_measures(request):
    temperature_measures_list = TemperatureMeasures.objects.all().order_by('-created_at')

    paginator = Paginator(temperature_measures_list, 30)
    page = request.GET.get('page')
    measures = paginator.get_page(page)

    return render(request, 'webApp/temperature_measures.html', {'temperature_measures': measures})


def humidity_measures(request):
    humidity_measures_list = HumidityMeasures.objects.all().order_by('-created_at')

    paginator = Paginator(humidity_measures_list, 30)
    page = request.GET.get('page')
    measures = paginator.get_page(page)

    return render(request, 'webApp/humidity_measures.html', {'humidity_measures': measures})


def temperature_chart(request):
    temperature_measures = TemperatureMeasures.objects.all().order_by('-created_at')[:50]

    temperatures = [float(temperature_measure.measure) for temperature_measure in temperature_measures]
    times = [temperature_measure.created_at.strftime('%Y-%m-%d %H:%M:%S') for temperature_measure in
             temperature_measures]

    context = {
        'temperatures': dumps(temperatures),
        'times': dumps(times)
    }

    return render(request, 'webApp/temperature_chart.html', context)


def humidity_chart(request):
    humidity_measures = HumidityMeasures.objects.all().order_by('-created_at')[:50]

    humidities = [float(humidity_measure.measure) for humidity_measure in humidity_measures]
    times = [humidity_measure.created_at.strftime('%Y-%m-%d %H:%M:%S') for humidity_measure in
             humidity_measures]

    context = {
        'humidities': dumps(humidities),
        'times': dumps(times)
    }

    return render(request, 'webApp/humidity_chart.html', context)
