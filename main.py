import discord
from discord.utils import get
from dotenv import load_dotenv
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from anju import *
from help import *
from randomize import *
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)

server_name = 'CocoLand'
games = ['Valorant', 'League']
game_emojis = {}
queue = {}
queue_text = 'Select the game you want to queue for: \n\n'

queue_id = None
queue_channel_id = None
queue_notifications_channel_id = None
bot_channel_id = None
guild = None

scheduler = AsyncIOScheduler()

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

async def remove_queue(user, game, type):
    global queue
    for i in range(len(queue[game])):
        if user in queue[game][i]:
            queue[game][i].remove(user)
            channel = client.get_channel(queue_notifications_channel_id)
            if type == 'inactive':
                msg = f'<@{user.id}>' + f' you have been removed from {game} (' + str(i + 1) + ') due to inactivity.'
            else:
                msg = str(user) + f' has left {game} (' + str(i + 1) + ').'
            await channel.send(msg)
            break
    
    if sum([len(i) for i in queue[game]]) >= 5:
        for i in range(len(queue[game])):
            if i > 0:
                while len(queue[game][i]) >= 1 and len(queue[game][i-1]) < 5:
                    temp = queue[game][i].pop(0)
                    queue[game][i-1].append(temp)
        if len(queue[game][-1]) == 0:
            queue[game].pop(-1)
    
    channel = client.get_channel(queue_channel_id)
    message = await channel.fetch_message(queue_id)
    content = queue_text
    for game in games:
        for i in range(len(queue[game])):
            content += '\n' + game + ' (' + str(i + 1) + '): ' + ', '.join([str(j) for j in queue[game][i]])
        content += '\n'
    await message.edit(content=content)

async def delete_queue(users, game):
    global queue
    for i in queue[game]:
        if i == users:
            queue[game].remove(i)

    channel = client.get_channel(queue_channel_id)
    message = await channel.fetch_message(queue_id)
    content = queue_text
    for game in games:
        for i in range(len(queue[game])):
            content += '\n' + game + ' (' + str(i + 1) + '): ' + ', '.join([str(j) for j in queue[game][i]])
        content += '\n'
    await message.edit(content=content)

async def check_queue(message, users, game):
    channel = client.get_channel(queue_notifications_channel_id)
    message = await message.channel.fetch_message(message.id)
    reacted = []
    async for i in message.reactions[0].users():
        reacted.append(i)
    if len(list(set(users).difference(set(reacted)))) == 0:
        run_at = datetime.now() + timedelta(minutes = 10)
        global scheduler
        scheduler.add_job(delete_queue, 'date', run_date = run_at, args = [users, game])
    else:
        channel = client.get_channel(queue_channel_id)
        message = await channel.fetch_message(queue_id)
        for reaction in message.reactions:
            if str(reaction.emoji) == game_emojis[game]:
                break
        for i in list(set(users).difference(set(reacted))):
            await remove_queue(i, game, 'inactive')
            await reaction.remove(i)


async def join_queue(user, game):
    global queue
    if len(queue[game]) == 0 or sum([1 if len(i) == 5 else 0 for i in queue[game]]) == len(queue[game]):
        queue[game].append([])
        queue[game][-1].append(user)
        msg = str(user) + f' has started {game} (' + str(len(queue[game])) + ')!'
        channel = client.get_channel(queue_notifications_channel_id)
        role_name = game.title()
        role = get(guild.roles, name=role_name)
        await channel.send(f'{role.mention} ' + msg)

    else:
        for i in range(len(queue[game])):
            if len(queue[game][i]) < 5:
                queue[game][i].append(user)
                channel = client.get_channel(queue_notifications_channel_id)
                msg = str(user) + f' has joined {game} (' + str(i + 1) + ').'
                await channel.send(msg)
                if len(queue[game][i]) == 4:
                    msg = f'{game} (' + str(i + 1) + ') needs one more player!'
                    await channel.send(msg)
                if len(queue[game][i]) == 5:
                    msg = " ".join([f'<@{user.id}>' for user in queue[game][i]]) + ' Your queue is ready! React within 10 minutes to stay in the queue.'
                    msg = await channel.send(msg)
                    await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                    run_at = datetime.now() + timedelta(minutes = 10)
                    global scheduler
                    scheduler.add_job(check_queue, 'date', run_date = run_at, args = [msg, queue[game][i], game])
                break

    channel = client.get_channel(queue_channel_id)
    message = await channel.fetch_message(queue_id)
    content = queue_text
    for game in games:
        for i in range(len(queue[game])):
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
    await channel.purge(limit=None, bulk=True)
    channel = get(client.get_all_channels(), guild__name=server_name, name='bot-commands')
    global bot_channel_id
    bot_channel_id = channel.id
    await channel.purge(limit=None, bulk=True)
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
    global scheduler
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

    #testing purposes
    if message.content == '!join':
        await join_queue(client.user, 'Valorant')
        return

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if reaction.message.id == queue_id:
        for game, emoji in game_emojis.items():
            if str(reaction.emoji) == emoji:
                await join_queue(user, game)
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
                await remove_queue(user, game, 'left')
                break
        return

client.run(TOKEN)
