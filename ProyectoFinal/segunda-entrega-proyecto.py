import os
from dotenv import load_dotenv
from telebot import telebot, types
# import subprocess
# from gpiozero import LED
from datetime import datetime
from notion_client import Client
import json
import schedule
import time
import threading

# Carga de tokens API desde archivo .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_LOSCHAMBEADORESBOT_API_TOKEN')
NOTION_TOKEN = os.getenv('NOTION_API_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
# Inicialización de clientes de Telegram & Notion
telegram_bot = telebot.TeleBot(TELEGRAM_TOKEN)
notion_client = Client(auth=NOTION_TOKEN)
# Inicialización de hardware (GPIO)
# led = LED(17)

# Carga de usuarios suscritos desde archivo JSON
try:
    with open('subscribed_users.json', 'r') as file:
        subscribed_users = json.load(file)
except FileNotFoundError:
    subscribed_users = []


def start(message):
    """
    Función para manejar el comando de inicio del bot.

    Params:
        message: Objeto de mensaje de Telegram.
    """
    telegram_bot.reply_to(
        message, "¡Hola! Soy tu bot de seguridad. Usa /subscribe para recibir notificaciones de eventos.")


def subscribe(message):
    """
    Función para manejar la suscripción a las notificaciones.

    Params:
        message: Objeto de mensaje de Telegram.
    """
    user_id = message.chat.id
    if user_id not in subscribed_users:
        subscribed_users.append(user_id)
        with open('subscribed_users.json', 'w') as file:
            json.dump(subscribed_users, file)
        telegram_bot.reply_to(
            message, "¡Te has suscrito satisfactoriamente! Ahora recibirás notificaciones de eventos.")
    else:
        telegram_bot.reply_to(message, "¡Ya estás suscrito!")


def unsubscribe(message):
    """
    Función para manejar la cancelación de la suscripción a las notificaciones.

    Params:
        message: Objeto de mensaje de Telegram.
    """
    user_id = message.chat.id
    if user_id in subscribed_users:
        subscribed_users.remove(user_id)
        with open('subscribed_users.json', 'w') as file:
            json.dump(subscribed_users, file)
        telegram_bot.reply_to(
            message, "Te has desuscrito correctamente. Ya no recibirás notificaciones.")
    else:
        telegram_bot.reply_to(message, "No estás suscrito actualmente.")


def send_photo_to_subscribers(photo_path):
    """
    Función para enviar una foto a todos los usuarios suscritos.

    Params:
        photo_path: Ruta de la foto a enviar.
    """
    with open(photo_path, 'rb') as photo:
        for user_id in subscribed_users:
            telegram_bot.send_photo(user_id, photo)


def send_message_to_subscribers(message_text):
    """
    Función para enviar un mensaje a todos los usuarios suscritos.

    Params:
        message_text: Texto del mensaje a enviar.
    """
    for user_id in subscribed_users:
        telegram_bot.send_message(user_id, message_text)

# def something_happens():
    """
    Función de ejemplo para activar el envío de una foto.
    """
    # Tu lógica aquí para detectar un evento
    # Suponiendo que tienes una variable photo_path que contiene la ruta de la foto
    # send_photo_to_subscribers(photo_path)


def add_log_entry_to_notion():

    log_date = datetime.now()
    try:
        response = notion_client.pages.create(
            parent={"database_id": NOTION_DATABASE_ID},
            icon={
                "emoji": "🚨"
            },
            properties={
                "Nombre evento": {"title": [{"text": {"content": f"Prueba {log_date.strftime('%Y-%m-%d %H:%M:%S')}"}}]},
                "Tipo evento": {"multi_select": [{"name": "Prueba"}]},
                "Fecha evento": {"date": {"start": log_date.isoformat()}},
            },
        )
    except Exception as e:
        # APIResponseError
        print("Error: ", e)


def something_happens():
    """
    Función de ejemplo para enviar un mensaje a todos los usuarios suscritos.
    """
    print("Enviando mensaje a los suscritos...")
    message_text = "¡Hola! Se ha detectado un evento en la caja de seguridad."
    send_message_to_subscribers(message_text)
    add_log_entry_to_notion()

# Comandos del bot


@ telegram_bot.message_handler(commands=['start'])
def handle_start(message):
    start(message)


@ telegram_bot.message_handler(commands=['subscribe'])
def handle_subscribe(message):
    subscribe(message)


@ telegram_bot.message_handler(commands=['unsubscribe'])
def handle_unsubscribe(message):
    unsubscribe(message)

# Función para ejecutar el polling del bot en un hilo separado


def bot_polling_thread():
    while True:
        try:
            telegram_bot.polling()
        except Exception as e:
            print(f"Error en el polling del bot: {e}")
            time.sleep(5)

# Función para ejecutar el programador de tareas en un hilo separado


def scheduler_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Iniciar el bot y el programador de tareas en hilos separados
bot_polling_thread = threading.Thread(target=bot_polling_thread)
scheduler_thread = threading.Thread(target=scheduler_thread)

bot_polling_thread.start()
scheduler_thread.start()

# Programar la ejecución de something_happens() cada 10 segundos
schedule.every(2).seconds.do(something_happens)

# Esperar a que ambos hilos terminen
bot_polling_thread.join()
scheduler_thread.join()
