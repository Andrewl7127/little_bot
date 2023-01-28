import discord
from discord.utils import get
from dotenv import load_dotenv
import os
from anju import *
from help import *
from randomize import *

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)

queue_id = None
channel_id = None

queue_text = 'Select the game you want to queue for: \n\n'
games = ['Valorant', 'League']
game_emojis = {}
queue = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    channel = get(client.get_all_channels(), guild__name="Koffee", name='queues')
    global channel_id
    channel_id = channel.id
    await channel.purge(limit=None, bulk=True)
    await public_help(channel)
    
    # make individual queues and identify emojis for each game
    global queue_text
    global queue
    global game_emojis
    for game in games:
        queue[game] = []
        queue_text += '**' + str(game) + '** '
        for emoji in client.emojis:
            if emoji.name == game.lower():
                game_emojis[game] = str(emoji)
                queue_text += str(emoji) + '\n'
                break

    # display bot message with emojis
    msg = await channel.send(queue_text)
    global queue_id 
    queue_id = msg.id

    # react to bot message with emojis
    for game, emoji in game_emojis.items():
        await msg.add_reaction(emoji)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!adopt':
        await adopt(message)
        return

    if message.content == '!fan':
        await fan(message)
        return

    if message.content == '!help':
        await help(message)
        return

    if message.content == '!map':
        await randomMap(message)
        return

    if message.content.startswith('!agent'):
        await randomAgent(message)
        return

    if message.content == '!gun':
        await randomGun(message)
        return

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if reaction.message.id == queue_id:
        for game, emoji in game_emojis.items():
            if str(reaction.emoji) == emoji:
                global queue
                for i in queue[game]:
                    msg = str(user) + f' has joined the {game} queue!'
                    await i.send(msg)

                queue[game].append(user)
                await user.send(f'You have been added to the {game} queue!')

                msg = f'Current members in {game} queue: '
                msg += ', '.join([str(i) for i in queue[game]])
                await user.send(msg)

                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(queue_id)
                content = queue_text
                for game in games:
                    content += '\n' + game + ' Queue (' + str(len(queue[game])) + ' persons): ' + ', '.join([str(i) for i in queue[game]])
                await message.edit(content=content)
                break
        return
            

@client.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == client.user.id:
        return

    if payload.message_id == queue_id:
        for game, emoji in game_emojis.items():
            if str(payload.emoji) == emoji:
                user = await client.fetch_user(payload.user_id)
                global queue
                if user in queue[game]:
                    queue[game].remove(user)
                    await user.send(f'You have been removed from the {game} queue!')
                    for i in queue[game]:
                        msg = str(user) + f' has left the {game} queue!'
                        await i.send(msg)
                
                channel = client.get_channel(channel_id)
                message = await channel.fetch_message(queue_id)
                content = queue_text
                for game in games:
                    content += '\n' + game + ' Queue (' + str(len(queue[game])) + ' persons): ' + ', '.join([str(i) for i in queue[game]])
                await message.edit(content=content)
                break
        return

client.run(TOKEN)
