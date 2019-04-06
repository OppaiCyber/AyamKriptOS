from pyrogram import Client, Filters
import configparser

# Get Bot API Key
config = configparser.ConfigParser()
config.read('config.ini')
botid = config['tg_info']['bot_api']

#Initial
app = Client(botid)

@app.on_message(Filters.command("start"))
def start_command(client, message):
    message.reply("Selamat datang di AyamKripto\nGunakan /help untuk mendapatkan bantuan")

app.run()