from threading import Thread
from gpiozero import DistanceSensor, LED
from time import sleep
from signal import pause
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

# Declaración variables de hardware y constantes
API_TOKEN = os.getenv('TELEGRAM_LOSCHAMBEADORESBOT_API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
led = LED(17)
sensor = DistanceSensor(echo=27, trigger=22,
                        max_distance=1, threshold_distance=0.2)
chat_id = ""
subscribed_users = set()


@bot.message_handler(commands=['alerta'])
def subscribe_to_alerts(message):
    global chat_id
    chat_id = message.chat.id
    subscribed_users.add(chat_id)
    bot.send_message(
        chat_id, "¡Te has suscrito a las alertas de sensor de distancia!")


def distance_sensor_alert():
    while True:
        if sensor.distance * 100 < 5 and subscribed_users:
            led.on()
            for user_id in subscribed_users:
                bot.send_message(
                    user_id, "ALERTA: Se ha detectado movimiento a menos de 10cm")
        else:
            led.off()
        print(sensor.distance * 100)


if __name__ == "__main__":
    distance_sensor_thread = Thread(target=distance_sensor_alert)
    distance_sensor_thread.start()

    # Se inicia el bot de telegram
    bot.polling()

    distance_sensor_thread.join()
