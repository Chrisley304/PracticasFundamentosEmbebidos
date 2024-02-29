from gpiozero import PWMLED
from bluedot import BlueDot
from signal import pause

# Definición de los pines asociados a cada LED del semáforo y definición de bluedot.
rojo = PWMLED(22)
amarillo = PWMLED(27)
verde = PWMLED(17)

def dpad(pos):
    if pos.top:
        amarillo.off()
        verde.off()
        print("prendio rojo")
        rojo.on()
    elif pos.middle:
        rojo.off()
        verde.off()
        print("prendio amarillo")
        amarillo.on()
    elif pos.bottom:
        amarillo.off()
        rojo.off()
        print("prendio verde")
        verde.on()

def set_brightness(pos):
    brightness = (pos.y + 1)/2
    print("Brillo: {0:.4f} | ".format(brightness))
    rojo.value = brightness
    amarillo.value = brightness
    verde.value = brightness

# Se crean 2 botones de bluedot
bd = BlueDot(cols = 2)
bd[0,0].when_pressed = dpad
bd[1,0].when_moved = set_brightness

pause()

