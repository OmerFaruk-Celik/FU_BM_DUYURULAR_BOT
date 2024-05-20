import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import pandas as pd

with open("./myPid2","w") as dosya:
                dosya.write(str(os.getpid()))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



def getID():
        with open("./chatID","r") as dosya:
                r=dosya.read()
        r=r.split()
        return r[1:]

def isSave(ID):
        return str(ID) in getID()


def saveID(ID):
        with open("./chatID","a") as dosya:
                dosya.write(str(ID)+"\n")

def start(update, context):
    """Send a message when the command /start is issued."""
    numara = 123456 #update.message.contact.phone_number
    ad = update.message.from_user.first_name
    chat_id = update.message.chat_id
    veri = {'Chat ID': [str(chat_id)], 'Numara': [str(numara)], 'Ad': [ad]}
    df = pd.DataFrame(veri)
    update.message.reply_text("Duyurular Botu Aktif!")
    if not isSave(chat_id):
        saveID(chat_id)
        with open("./kayit.csv", 'a') as f:
            df.to_csv(f, mode='a', index=False)
        update.message.reply_text('Duyurular Sayfasına Hoş Geldin '+ad)
            
with open("token.txt","r") as f:
    bot_token=f.read() 
def main():
    """Start the bot."""
    token = bot_token
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
