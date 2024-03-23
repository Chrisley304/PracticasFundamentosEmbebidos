from gpiozero import DistanceSensor, LED
from signal import pause

#trig = 4
# Echo = 17
sensor = DistanceSensor(echo=17, trigger=4, max_distance=1,
threshold_distance=0.2)
led = LED(22)

sensor.when_in_range = led.on
sensor.when_out_of_range = led.off

pause()