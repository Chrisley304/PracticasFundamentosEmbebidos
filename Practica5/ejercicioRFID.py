import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Coloca tu tag")
    uid, text = reader.read()
    print(f"UID: {uid}")
    print(text)
finally:
    GPIO.cleanup()