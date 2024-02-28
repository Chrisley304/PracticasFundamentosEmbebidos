from gpiozero import LED
from time import sleep

# Definición de los pines asociados a cada LED del semáforo.
rojo = LED(26)
amarillo = LED(13)
verde = LED(5)

while True:
    # Verde
    verde.on()
    sleep(5)
    verde.off()

    # Amarillo
    amarillo.on()
    sleep(2)
    amarillo.off()

    # Rojo
    rojo.on()
    sleep(5)
    rojo.off()
