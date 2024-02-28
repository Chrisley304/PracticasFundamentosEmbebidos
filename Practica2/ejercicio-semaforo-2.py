from gpiozero import LED, Button
from time import sleep

# Definición de los pines asociados a cada LED del semáforo y al botón.
rojo = LED(26)
amarillo = LED(13)
verde = LED(5)
boton = Button(17)


def esperar(tiempo):
    """
        Chequeo del estado del botón cada 0.1 segundos
    """
    for _ in range(int(tiempo * 10)):
        if boton.is_pressed:
            return True
        sleep(0.1)
        return False


while True:
    # Verde
    verde.on()
    if esperar(5):
        verde.off()
        rojo.on()
        sleep(3)
        rojo.off()
        continue
    verde.off()

    # Amarillo
    amarillo.on()
    if esperar(2):
        amarillo.off()
        rojo.on()
        sleep(3)
        rojo.off()
        continue
    amarillo.off()

    # Rojo
    rojo.on()
    if esperar(5):
        rojo.off()
        continue
    rojo.off()
