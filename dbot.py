import discord
from termcolor import colored

client = discord.Client()

def start_dbot(D_TOKEN):
  client.run(D_TOKEN)

@client.event
async def on_ready():
    print(colored('SYS:  2) dbot {0.user} is now live!'.format(client), 'grey'))

@client.event
async def on_message(message):
  # check that message is from our maplesea-announcements channel
  if message.channel.id == 844288549507170314: # TODO: Use env vars
    print(colored('DISC: Message from maplesea-announcements channel received:\n\t{}'.format(message.content), 'magenta'))

  

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