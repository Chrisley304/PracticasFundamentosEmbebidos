import time
import adafruit_fingerprint
import serial
from gpiozero import LED
import I2C_LCD_driver

# Inicializar los leds
red = LED(17)
green = LED(27)

# Inicilaizar LCD
mylcd = I2C_LCD_driver.lcd()

# Inicializa el sensor.
uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# Estructura para comprobar si el sensor esta listo y funcionando.
while finger.get_image() == adafruit_fingerprint.OK:
    pass

print('Coloca tu dedo en el sensor...')
time.sleep(2)

while True:
    # Intenta escanear la huella.
    result = finger.get_image()

    # Acciones a realizar en caso de que se detecte una huella en el sensor.
    if result == adafruit_fingerprint.OK:
        print('Imagen escaneada con éxito. Verificando huella...')
        # time.sleep(1)

        # Procesar la huella leida.
        result = finger.image_2_tz(1)

        # Huella procesa con exito
        if result == adafruit_fingerprint.OK:
            # Intenta buscar la huella en la base de datos
            result = finger.finger_fast_search()
            mylcd.lcd_clear()
            # Huella encontrada en la base
            if result == adafruit_fingerprint.OK:
                print('¡Huella reconocida!')
                green.on()
                mylcd.lcd_display_string("Acceso Permitido", 1)
                time.sleep(5)
                green.off()
                mylcd.lcd_clear()
            # Huella no encontrada en la base.
            else:
                print('Huella no encontrada')
                red.on()
                mylcd.lcd_display_string("Acceso Denegado", 1)
                time.sleep(5)
                red.off()
                mylcd.lcd_clear()
        else:
            # Huella no reconocida.
            print('No se pudo leer la huella')
            mylcd.lcd_display_string("No se pudo leer la huella", 1)
            time.sleep(2)
    # No se ha leido una huella en el sensor.
    else:
        print('No se detectó ningún dedo en el sensor')
        mylcd.lcd_display_string("Esperando huella", 1)
