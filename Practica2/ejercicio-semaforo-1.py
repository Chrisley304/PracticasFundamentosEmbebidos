from gpiozero import LED
from time import sleep

# Definición de los pines asociados a cada LED del semáforo.
rojo = LED(22)
amarillo = LED(27)
verde = LED(17)

while True:
    # Verde
    verde.on()
    print("prendio verde")
    sleep(5)
    verde.off()

    # Amarillo
    amarillo.on()
    print("prendio amarillo")
    sleep(2)
    amarillo.off()

    # Rojo
    rojo.on()
    print("prendio rojo")
    sleep(5)
    rojo.off()
