import discord
from termcolor import colored
import requests

client = discord.Client()

def start_dbot(D_TOKEN):
  client.run(D_TOKEN)

@client.event
async def on_ready():
    print(colored('SYS:  2) dbot {0.user} is now live!'.format(client), 'grey'))

@client.event
async def on_message(message):
  print(colored('DISC: message received', 'magenta'))
  # check that message is from our maplesea-announcements channel
  if message.channel.id == 844288549507170314: # TODO: Use env vars
    # Logging
    print(colored('DISC: Message from maplesea-announcements channel received:\n\t{}'.format(message.content), 'magenta'))
    # Build message object
    msg = { 
      'title': 'message from discord',
      'body': message.content
    }
    # Forward to tele api
    # r = requests.post('localhost:5000/post_to_channel', data=msg)
    # print(colored('DISC: Posted to tele: {}'.format(r.text), 'magenta'))
  

# TODO: Message edited?
# message object: <Message 
    #   id=844584112626335795 
    #   channel=<TextChannel 
    #             id=844288549507170314 
    #             name='maplesea-announcements' 
    #             position=0 
    #             nsfw=False 
    #             news=False 
    #             category_id=844286929100341290> 
    #   type=<MessageType.default: 0> 
    #   author=<Member id=392691520358055947 name='FluffDucks' discriminator='8030' bot=False nick=None guild=<Guild id=844286929100341289 name="FluffDucks' Dev Server" shard_id=None chunked=False member_count=2>> 
    #   flags=<MessageFlags value=0>>

    # if message.content.startswith('$hello'):
    #     await message.channel.send('Hello!')