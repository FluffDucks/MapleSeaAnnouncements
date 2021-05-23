import os
from termcolor import colored
from flask import Flask, request
import telegram
from functools import partial
from threading import Thread

# Declare tele vars
TBOT_TOKEN = os.getenv('TBOT_TOKEN')
TCHANNEL_ID = os.getenv('TCHANNEL_ID')
bot = telegram.Bot(token=TBOT_TOKEN) # Run telebot

# Declare heroku vars
H_URL = os.getenv('H_URL')

# start the flask app
app = Flask(__name__)
if __name__ == '__main__':
    # threaded arg which allows app to have more than one thread
    app.run(threaded=True)

# Print welcome and state messages
print(colored('SYS:  Welcome :3', 'grey'))
print(colored('SYS:  1) telebot and server is now live!', 'grey'))

######### TELE BOT END POINTS ##########
@app.route('/')
def index():
    return 'annyeong'

# Only run this end point when the tele bot has changed
@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    # Use the bot object to link the bot to the heroku app which lives in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=H_URL, HOOK=TBOT_TOKEN))

    # Feedback text (prints on page)
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

# When a message is sent to the telebot, telegram calls this endpoint with a request object
@app.route('/{}'.format(TBOT_TOKEN), methods=['POST'])
def respond():
    # Retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    # If the received update is a message 
    if update.message is not None:
        chat_id = update.message.chat.id
        msg_id = update.message.message_id
        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8').decode()
        # Debugging
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
    else:
        # Debugging
        print('non-message update received from telebot')
    
    # Debugging, End of method call
    return 'respond() done running'

# TODO: Check for auth before allowing to post
@app.route('/post_to_channel', methods=['POST'])
def post_to_channel():
    # content format:
    # {
    #   'title': '',
    #   'body': ''
    # }
    content = request.get_json(force=True)
    new_post = '_NEW ANNOUNCEMENT_\n*{}*\n\n{}'.format(content.get('title'), content.get('body'))
    bot.sendMessage(chat_id=TCHANNEL_ID, text=new_post, parse_mode = 'Markdown')
    return 'post_to_channel() done running'