from pyrogram import Client, Filters
import configparser
import requests
import requests_cache
import sys, os
from googletrans import Translator
# Define Function
# get_args :: Get Argument after Command
def get_args(msg):
	text = msg.text
	textSP = text.split(' ')
	return textSP

# rupiah_format :: Change Numeric into IDR Format
def formatrupiah(uang):
    y = str(uang)
    if len(y) <= 3 :
        return 'Rp ' + y
    else :
        p = y[-3:]
        q = y[:-3]
        return   formatrupiah(q) + '.' + p

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
    except (ValueError, IndexError):
    	text = "Command Usage : /p coin"
    await message.reply(text)

# Calculate Command :: Check Cryptocurrency Price & Calculate Amount of Crypto via CryptoCompare API
@app.on_message(Filters.command("calc"))
async def calc_command(client, message):
    coinF = get_args(message)
    try:
        coinS = coinF[1].upper()
        coinAM = coinF[2]
        requests_cache.install_cache('price_cache', backend='sqlite', expire_after=300)
        get = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms='+coinS+'&tsyms=BTC,USD,IDR')
        data = get.json()
        btc = data['RAW'][coinS]['BTC']['PRICE'] * float(coinAM)
        btc = "{:.8f}".format(float(btc)) # Special for BTC to Change Scientific Notation to Decimal
        idr = data['RAW'][coinS]['IDR']['PRICE'] * float(coinAM)
        usd = data['RAW'][coinS]['USD']['PRICE'] * float(coinAM)
        text = "CALC : "+coinS+"\n`USD : $"+ str(round(usd, 3)) + "\nIDR : "+ str(formatrupiah(idr)) + "\nBTC : " + str(btc) + "`"
    except (ValueError, IndexError):
        text = "Command Usage : /calc coin amount"
    await message.reply(text)

# Indodax Command :: Check Cryptocurrency Price via Indodax API
@app.on_message(Filters.command("indodax"))
async def indodax_command(client, message):
    coinF = get_args(message)
    try:
    	coinS = coinF[1].lower()
    	requests_cache.install_cache('price_cache', backend='sqlite', expire_after=300)
    	get = requests.get('https://indodax.com/api/'+coinS+'_idr/ticker')
    	data = get.json()
    	last = data['ticker']['last']
    	text = "`"+coinS.upper()+" : "+str(formatrupiah(last))+"`"
    except (ValueError, IndexError):
    	text = "Command Usage : /indodax coin"
    await message.reply(text)

# Translate Command :: Automatically Translate Language via GTranslate
@app.on_message(Filters.command("tr"))
async def translate_command(client, message):
    lang = get_args(message)
    transText = message.reply_to_message.text
    translator = Translator() #init translation
    print(lang)
    try:
        doTr = translator.translate(transText, dest=lang[1])
        text = doTr.text
    except (ValueError, IndexError):
        text = "Command Usage : /tr destLang "
    await message.reply(text)

# Restart Command :: Restart bot to get new edited things
@app.on_message(Filters.command("restart"))
async def restart_command(client, message):
    await message.reply("[ INFO ] BOT RESTARTING")
    python = sys.executable
    os.execl(python, python, *sys.argv)
app.run()