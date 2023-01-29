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

queue_id = None
queue_channel_id = None
general_channel_id = None
bot_channel_id = None
guild = None
server_name = 'Koffee'

queue_text = 'Select the game you want to queue for: \n\n'
games = ['Valorant', 'League']
game_emojis = {}
queue = {}

async def clear_queues(message):
    global queue
    queue = {}
    for game in games:
        queue[game] = []
    await message.edit(content=queue_text)
    await message.clear_reactions()
    for game, emoji in game_emojis.items():
        await message.add_reaction(emoji)

async def clear_bot_commands():
    channel = client.get_channel(bot_channel_id)
    await channel.purge(limit=None, bulk=True)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    #variables
    global guild
    guild = get(client.guilds, name=server_name)
    channel = get(client.get_all_channels(), guild__name=server_name, name='general')
    global general_channel_id
    general_channel_id = channel.id
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
    scheduler.add_job(clear_bot_commands, 'interval', days=1, start_date='2022-01-01 7:00:00', timezone=pacific)
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

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if reaction.message.id == queue_id:
        for game, emoji in game_emojis.items():
            if str(reaction.emoji) == emoji:
                global queue

                if len(queue[game]) == 0:
                    msg = str(user) + f' has started a {game} queue!'
                    channel = client.get_channel(general_channel_id)
                    role_name = 'LFG-' + game.title()
                    role = get(guild.roles, name=role_name)
                    await channel.send(f'{role.mention} ' + msg)

                for i in queue[game]:
                    msg = str(user) + f' has joined the {game} queue!'
                    await i.send(msg)

                queue[game].append(user)
                await user.send(f'You have been added to the {game} queue!')

                msg = f'Current members in {game} queue: '
                msg += ', '.join([str(i) for i in queue[game]])
                await user.send(msg)

                channel = client.get_channel(queue_channel_id)
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
                
                channel = client.get_channel(queue_channel_id)
                message = await channel.fetch_message(queue_id)
                content = queue_text
                for game in games:
                    content += '\n' + game + ' Queue (' + str(len(queue[game])) + ' persons): ' + ', '.join([str(i) for i in queue[game]])
                await message.edit(content=content)
                break
        return

client.run(TOKEN)
