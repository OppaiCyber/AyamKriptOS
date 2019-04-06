from pyrogram import Client, Filters
import configparser
import requests
import json
import locale
import os
import sys
import requests_cache

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
@app.on_message(Filters.command("start"))
async def start_command(client, message):
    await message.reply("Selamat datang di AyamKripto\nGunakan /help untuk mendapatkan bantuan")

# Ping Command :: Test Bot Connection
@app.on_message(Filters.command("ping"))
async def ping_command(client, message):
    await message.reply("🏓 Pong!")

# Price Command :: Check Cryptocurrency Price via CryptoCompare API 
@app.on_message(Filters.command("p"))
async def price_command(client, message):
    coinF = get_args(message)
    try:
    	coinS = coinF[1].upper()
    	requests_cache.install_cache('price_cache', backend='sqlite', expire_after=300)
    	get = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms='+coinS+'&tsyms=BTC,USD,IDR')
    	data = get.json()
    	btc = data['DISPLAY'][coinS]['BTC']
    	idr = data['DISPLAY'][coinS]['IDR']
    	usd = data['DISPLAY'][coinS]['USD']
    	text = "`"+coinS+" : "+usd['PRICE']+" | "+usd['CHANGEPCTDAY']+"%\n"+idr['PRICE']+" | "+idr['CHANGEPCTDAY']+"%\n"+btc['PRICE']+" | "+btc['CHANGEPCTDAY']+"%`"
    except:
    	text = "Command Usage : /p coin"
    await message.reply(text)

# Price Command :: Check Cryptocurrency Price via CryptoCompare API 
@app.on_message(Filters.command("calc"))
async def calc_command(client, message):
    coinF = get_args(message)
    try:
    	coinS = coinF[1].upper()
    	coinAM = coinF[2]
    	requests_cache.install_cache('price_cache', backend='sqlite', expire_after=300)
    	get = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms='+coinS+'&tsyms=BTC,USD,IDR')
    	data = get.json()
    	btc = data['RAW'][coinS]['BTC']['PRICE'] * int(coinAM)
    	btc = "{:.8f}".format(float(btc)) # Special for BTC to Change Scientific Notation to Decimal 
    	idr = data['RAW'][coinS]['IDR']['PRICE'] * int(coinAM)
    	usd = data['RAW'][coinS]['USD']['PRICE'] * int(coinAM)
    	text = "CALC : "+coinS+"\n`USD : $"+ str(round(usd, 3)) + "\nIDR : "+ str(rupiah_format(idr, True, 0)) + "\nBTC : " + str(btc) + "`"
    except:
    	text = "Command Usage : /calc coin amount"
    await message.reply(text)

# Restart Command :: Restart bot to get new edited things
@app.on_message(Filters.command("restart"))
async def restart_command(client, message):
    await message.reply("[ INFO ] BOT RESTARTED")
    os.system('cls')  # For Windows
    os.system('clear')  # For Linux/OS X
    python = sys.executable
    os.execl(python, python, *sys.argv)

app.run()