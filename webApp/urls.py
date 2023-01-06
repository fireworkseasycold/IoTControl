from django.urls import path

from . import views

urlpatterns = [
    path('', views.actuators, name='actuators'),
    path('blink_led_on', views.blink_led_on, name="blink_led_on"),
    path('blink_led_off', views.blink_led_off, name="blink_led_off"),
    path('temperature_measures', views.temperature_measures, name='temperature_measures'),
    path('humidity_measures', views.humidity_measures, name='humidity_measures'),
    path('temperature_chart', views.temperature_chart, name='temperature_chart'),
    path('humidity_chart', views.humidity_chart, name='humidity_chart'),
]
