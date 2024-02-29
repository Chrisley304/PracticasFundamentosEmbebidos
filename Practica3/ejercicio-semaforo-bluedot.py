from bluedot import BlueDot
from gpiozero import LED
from gpiozero import LED
from time import sleep

# Definición de los pines asociados a cada LED del semáforo y definición de bluedot.
rojo = LED(22)
amarillo = LED(27)
verde = LED(17)
bd = BlueDot()

while True:
    # Verde
    verde.on()
    print("prendio verde")

    # Amarillo
    bd.wait_for_press()
    verde.off()
    amarillo.on()
    print("prendio amarillo")

    # Rojo
    bd.wait_for_press()
    amarillo.off()
    rojo.on()
    print("prendio rojo")

    # Reinicio
    bd.wait_for_press()
    rojo.off()