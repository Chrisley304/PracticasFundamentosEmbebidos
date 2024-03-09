import os
from gpiozero import LED
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('TELEGRAM_LOSCHAMBEADORESBOT_API_TOKEN')
led = LED(17)
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['apaga'])
def turn_off(message):
    led.off()
    bot.reply_to(message, "se apago el led")


@bot.message_handler(commands=['enciende'])
def turn_on(message):
    led.on()
    bot.reply_to(message, "se encendio")


bot.infinity_polling()
