from pyrogram import Client, Filters
import configparser
import requests

def get_args(msg):
	text = msg.text
	textSP = text.split(' ')
	return textSP

# Get Bot API Key
config = configparser.ConfigParser()
config.read('config.ini')
botid = config['tg_info']['bot_api']

#Initial
app = Client(botid)

@app.on_message(Filters.command("start"))
def start_command(client, message):
    message.reply("Selamat datang di AyamKripto\nGunakan /help untuk mendapatkan bantuan")

@app.on_message(Filters.command("ping"))
def ping_command(client, message):
    message.reply("🏓 Pong!")


app.run()