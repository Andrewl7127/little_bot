import discord
from discord.utils import get
from dotenv import load_dotenv
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from anju import *
from help import *
from randomize import *

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)

server_name = 'CocoLand Test'
games = ['Valorant', 'League']
game_emojis = {}
queue = {}
queue_text = 'Select the game you want to queue for: \n\n'

queue_id = None
queue_channel_id = None
queue_notifications_channel_id = None
bot_channel_id = None
guild = None

async def clear_queues(message):
    global queue
    queue = {}
    for game in games:
        queue[game] = []
    await message.edit(content=queue_text)
    await message.clear_reactions()
    for game, emoji in game_emojis.items():
        await message.add_reaction(emoji)

async def clear_channels():
    channel = client.get_channel(bot_channel_id)
    await channel.purge(limit=None, bulk=True)
    channel = client.get_channel(queue_notifications_channel_id)
    await channel.purge(limit=None, bulk=True)

async def join_queue(user):
    global queue
    if len(queue[game]) == 0 or sum([len(i) for i in queue[game]]) % 5 == 0:
        queue[game].append([])
        queue[game][-1].append(user)
        msg = str(user) + f' has started {game} queue (' + str(len(queue[game])) + ')!'
        channel = client.get_channel(queue_notifications_channel_id)
        role_name = 'LFG-' + game.title()
        role = get(guild.roles, name=role_name)
        await channel.send(f'{role.mention} ' + msg)

    else:
        for i in range(len(queue[game])):
            if len(queue[game][i]) < 5:
                queue[game][i].append(user)
                break
        channel = client.get_channel(queue_notifications_channel_id)
        msg = str(user) + f' has joined {game} queue (' + str(i + 1) + ')!'
        await channel.send(msg)

    channel = client.get_channel(queue_channel_id)
    message = await channel.fetch_message(queue_id)
    content = queue_text
    for game in games:
        for i in range(len(game)):
            content += '\n' + game + ' (' + str(i + 1) + '): ' + ', '.join([str(j) for j in queue[game][i]])
        content += '\n'
    await message.edit(content=content)

async def remove_queue(payload):
    user = await client.fetch_user(payload.user_id)
    global queue
    for i in range(len(queue[game])):
        if user in i:
            i.remove(user)
            channel = client.get_channel(queue_notifications_channel_id)
            msg = str(user) + f' has left {game} queue (' + str(i + 1) + ').'
            await channel.send(msg)
    
    channel = client.get_channel(queue_channel_id)
    message = await channel.fetch_message(queue_id)
    content = queue_text
    for game in games:
        for i in range(len(game)):
            content += '\n' + game + ' (' + str(i + 1) + '): ' + ', '.join([str(j) for j in queue[game][i]])
        content += '\n'
    await message.edit(content=content)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    #variables
    global guild
    guild = get(client.guilds, name=server_name)
    channel = get(client.get_all_channels(), guild__name=server_name, name='queue-notifications')
    global queue_notifications_channel_id
    queue_notifications_channel_id = channel.id
    channel = get(client.get_all_channels(), guild__name=server_name, name='bot-commands')
    global bot_channel_id
    bot_channel_id = channel.id
    channel = get(client.get_all_channels(), guild__name=server_name, name='queues')
    global queue_channel_id
    queue_channel_id = channel.id

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

    #queue clear schedule
    pacific = pytz.timezone("US/Pacific")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clear_queues, 'interval', args = [msg], days=1, start_date='2022-01-01 7:00:00', timezone=pacific)
    scheduler.add_job(clear_channels, 'interval', days=1, start_date='2022-01-01 7:00:00', timezone=pacific)
    scheduler.start()

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

    if message.content == '!pistol':
        await randomPistol(message)
        return

    if message.content == '!strat':
        await randomStrat(message)
        return

    if message.content == '!test':
        tag = "Anju#8036"
        user = get(client.users, name=tag.split("#")[1], discriminator=tag.split("#")[0])
        await join_queue(user)
        return

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if reaction.message.id == queue_id:
        for game, emoji in game_emojis.items():
            if str(reaction.emoji) == emoji:
                join_queue(user)
                break
        return
            

@client.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == client.user.id:
        return

    if payload.message_id == queue_id:
        for game, emoji in game_emojis.items():
            if str(payload.emoji) == emoji:
                remove_queue(payload)
                break
        return

client.run(TOKEN)
