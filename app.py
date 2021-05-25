import os
from termcolor import colored
from flask import Flask, request, render_template, redirect, url_for
import telegram

# Declare tele vars
TBOT_TOKEN = os.getenv('TBOT_TOKEN')
TCHANNEL_ID = os.getenv('TCHANNEL_ID')
DEV_TCHANNEL_ID = os.getenv('DEV_TCHANNEL_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID', TCHANNEL_ID) # Channel to route posts to, defaults to main channel if no existing vars found
bot = telegram.Bot(token=TBOT_TOKEN) # Run telebot

# Other vars
H_URL = os.getenv('H_URL')
ACCESS_CODE = os.getenv('ACCESS_CODE')
is_authorised = False

# start the flask app
app = Flask(__name__)
if __name__ == '__main__':
    # threaded arg which allows app to have more than one thread
    app.run(threaded=True)

# Print welcome and state messages
print(colored('SYS:  Welcome :3', 'grey'))
print(colored('SYS:  1) telebot and server is now live!', 'grey'))

######### TELE BOT END POINTS ##########
@app.route('/', methods=['GET', 'POST'])
def index():
    global CHANNEL_ID
    global is_authorised

    # If an access code is entered
    if request.method == 'POST': 
        if 'submit_code' in request.form:
            code = request.form.get('code') 
            if code == ACCESS_CODE:
                is_authorised = True
            else:
                is_authorised = False
        elif 'cc_pls' in request.form:
            # Toggle CHANNEL_ID
            CHANNEL_ID = TCHANNEL_ID if CHANNEL_ID == DEV_TCHANNEL_ID else DEV_TCHANNEL_ID
            # Set to .env such that it persists across application startups
            os.environ['CHANNEL_ID'] = CHANNEL_ID

        # Re-render page
        return redirect(url_for('index'))

    # Check which channel is live
    if CHANNEL_ID == TCHANNEL_ID:
        channel_name = '[LIVE] MapleSea Announcements (Unofficial)'
    else:
        channel_name = '[DEV] Dev Channel'

    # Render template
    return render_template('index.html', channel_name=channel_name, is_authorised=is_authorised)

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

# @app.route('/toggle_channel', methods=['GET'])
# def toggle_channel():


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

@app.route('/{}/post_to_channel'.format(TBOT_TOKEN), methods=['POST'])
def post_to_channel():
    # content format:
    # {
    #   'title': '',
    #   'body': ''
    # }
    content = request.get_json(force=True)
    new_post = '*NEW ANNOUNCEMENT 🍄*\n{}'.format(content.get('body'))
    bot.sendMessage(chat_id=CHANNEL_ID, text=new_post, parse_mode='MarkdownV2')
    return 'post_to_channel() done running'


