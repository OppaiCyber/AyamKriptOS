from pyrogram import Client, Filters
import configparser
import requests
import json
import locale

# Define Function
# get_args :: Get Argument after Command
def get_args(msg):
	text = msg.text
	textSP = text.split(' ')
	return textSP

# rupiah_format :: Change Numeric into IDR Format
def rupiah_format(angka, with_prefix=False, desimal=2):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format("%.*f", (desimal, angka), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah

# Get Bot API Key
config = configparser.ConfigParser()
config.read('config.ini')
botid = config['tg_info']['bot_api']

#Initial
app = Client(botid)

# Start Command :: First Command to get Executed
app.on_message(Filters.command("start"))
def start_command(client, message):
    message.reply("Selamat datang di AyamKripto\nGunakan /help untuk mendapatkan bantuan")

# Ping Command :: Test Bot Connection
app.on_message(Filters.command("ping"))
def ping_command(client, message):
    message.reply("🏓 Pong!")

# Price Command :: Check Cryptocurrency Price via CryptoCompare API 
app.on_message(Filters.command("p"))
def price_command(client, message):
    coinF = get_args(message)
    coinS = coinF[1].upper()
    get = requests.get('https://min-api.cryptocompare.com/data/price?fsym='+coinS+'&tsyms=BTC,USD,IDR')
    data = get.json()
    idrF = rupiah_format(data['idr'])
    message.reply(idrF)
    
app.run()