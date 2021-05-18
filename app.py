from flask import Flask, request
import telegram
from telegram_bot.credentials import bot_token, bot_user_name,URL

# Declare global vars
global bot
global TOKEN
global channel_handle
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)
channel_handle = 'MapleSeaAnnouncements'

# start the flask app
app = Flask(__name__)

if __name__ == '__main__':
  # threaded arg which allows app to have more than one thread
  app.run(threaded=True)

@app.route('/')
def index():
    return '.'

# Only run this end point when the tele bot has changed
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    # Use the bot object to link the bot to the heroku app which lives in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    
    # Feedback text (prints on page)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

# When a message is sent to the telebot
@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
  # retrieve the message in JSON and then transform it to Telegram object
  update = telegram.Update.de_json(request.get_json(force=True), bot)
  chat_id = update.message.chat.id
  msg_id = update.message.message_id
  # Telegram understands UTF-8, so encode text for unicode compatibility
  text = update.message.text.encode('utf-8').decode()
  # for debugging purposes only
  print("got text message :", text)
  
  # First time a user chats with the bot, send the welcoming message
  if text == "/start":
    bot_welcome = """
    Welcome to MapleSea Bot!\nThis bot feeds server announcements from MapleSea's discord server to our associated Telegram Channel, https://t.me/MapleSeaAnnouncements.\nBeyond that, there's nothing more to see here!
    """
    # Send the welcoming message
    bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
  # Any other message sent by user
  else:
    reply = 'There is really nothing else I can offer here </3. Go to our channel! https://t.me/MapleSeaAnnouncements <3'
    bot.sendMessage(chat_id=chat_id, text=reply, reply_to_message_id=msg_id)
  return 'ok'