import os
from gpiozero import LED
import telebot

API_TOKEN='7101565997:AAGXOGFAmZ8s6EOxp_mFys-moEdRYjakPjs'
led= LED(17)
bot=telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['apaga'])
def turn_off(message):
    led.off()
    bot.reply_to(message,"se apago el led")

@bot.message_handler(commands=['enciende'])
def turn_on(message):
    led.on()
    bot.reply_to(message,"se encendio")

bot.infinity_polling()