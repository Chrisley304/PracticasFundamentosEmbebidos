import os
from dotenv import load_dotenv
from telebot import telebot, types
import speech_recognition as sr
import subprocess 
from gpiozero import LED
from datetime import datetime

# Carga de token API para bot de telegram desde archivo .env
load_dotenv()
TOKEN = os.getenv('TELEGRAM_LOSCHAMBEADORESBOT_API_TOKEN')
bot = telebot.TeleBot(TOKEN)  # Crea una instancia del bot con el token
# Inicialización de hardware (GPIO)
led = LED(17)
# Inicialización del engine de text to speech

def get_voice_file(message):
    """
        Descarga el mensaje de voz, conviertiendolo a formato WAV.
        @returns: wav_filename (str)
    """
    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)

    voice_note_date = datetime.today().strftime('%d-%m-%Y_%H:%M:%S')
    start_filename = f"voice-note_{voice_note_date}"
    with open(start_filename + ".ogg", 'wb') as w:
        w.write(file)
    
    subprocess.call(['ffmpeg', '-i', start_filename + ".ogg", start_filename + ".wav"])

    return start_filename

def get_text_from_voice_note(filename):
    """
        Transcribe una nota de voz a texto.
        @returns: text (str)
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")  # Se utiliza la API de google para el speech to text
            print(f"Usuario: {text}")
            return text
        except sr.UnknownValueError:
            print("Error: No se reconocio speech")
            return ""
        except sr.RequestError:
            print("Error: Conexión fallida a la API de speech to text")
            return ""

def assistant_speak(phrase:str):
    """
        Make the assistant speak using the given phrase.
    """
    # Se remplazan los espacios por "_" debido a un bug con espeak que evita que termine la oración 
    # fuente: https://stackoverflow.com/questions/37244892/espeak-phrase-stops-on-the-first-word-with-os
    if phrase != "":
        formatted_phrase = phrase.replace(" ", "_") 
        print("Asistente: ", phrase)
        os.system(f"espeak {formatted_phrase} -v es-la")

def exec_command(command, user_first_name):
    """
        Ejecuta el comando solicitado por el usuario.
        @returns: response (str)
    """
    if command == "hola":
        return f"Hola {user_first_name}! ¿Cómo estás?"
    elif command == "enciende el led":
        if led.is_active:
            return f"Lo siento {user_first_name}, el LED ya esta encendido"
        else:
            led.on()
            return f"Claro {user_first_name}, estoy encendiendo el LED"
    elif command == "apaga el led":
        if led.is_active:
            led.off()
            return f"Claro {user_first_name}, estoy apagando el LED"
        else:
            led.on()
            return f"Lo siento {user_first_name}, el LED ya esta apagado"
    elif command == "parpadea el led":
        led.blink(on_time=0.5, off_time=0.5, n=5, background=False)  # Hace parpadear el LED
    elif command == "cuentame un chiste" or command == "cuéntame un chiste":
        return f"Claro {user_first_name}... ¿Qué le dijo un cable a otro cable?... ¡Somos los intocables! jajaja"
    else:
        return None  # Si el comando no es reconocido, se regresa None

@bot.message_handler(commands=['start'])
def send_welcome(message:types.Message):
    bot.reply_to(message, f"Hola {message.from_user.first_name}! Bienvenido al asistente virtual.\nRecuerda que solo se maneja por *notas de voz*\nEscribe /help para ver los comandos disponibles.")

@bot.message_handler(commands=['help'])
def send_welcome(message:types.Message):
    bot.reply_to(message, """
    Los comandos disponibles son:
    - enciende el led
    - apaga el led
    - cuentame un chiste
    - parpadea el led
""")

@bot.message_handler(content_types=['voice'])
def handle_voice(message:types.Message):
    """
        Maneja los mensajes de voz recibidos, haciendo el speech to text para ejecutar los comandos solicitados, además de hacer el text to speech en el altavoz.
    """
    user_first_name = message.from_user.first_name
    voice_note_filename = get_voice_file(message)
    speech_transcript = get_text_from_voice_note(voice_note_filename + ".wav")

    if speech_transcript:
        response = exec_command(speech_transcript.lower(), user_first_name)
        if response:
            assistant_speak(response)
            bot.reply_to(message, f"{response}")
        else:
            bot.reply_to(message, f"Comando '{speech_transcript.lower()}' no encontrado. Intenta enviar /help para ver la lista de comandos disponibles.")

    os.remove(voice_note_filename + ".wav")  # Elimina el archivo WAV después de su uso
    os.remove(voice_note_filename + ".ogg")  # Elimina el archivo OGG después de su uso

bot.polling()  # Inicia el bot para que escuche mensajes
