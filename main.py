import discord
from discord.utils import get
from dotenv import load_dotenv
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz
from misc import *
from help import *
from randomize import *
import datetime

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=intents)

games = ['Valorant', 'League', 'Minecraft', 'Rocket', 'Csgo']
game_n = {'Valorant':5, 'League':5, 'Minecraft':9999, 'Rocket':3, 'Csgo':5}

server_variables = {}

pacific = pytz.timezone("US/Pacific")
scheduler = AsyncIOScheduler()

async def clear_queues(message, guild_id):
    global server_variables
    queue = server_variables[guild_id]['queue']
    queue.clear()
    for game in games:
        queue[game] = []
    await message.edit(content=server_variables[guild_id]['queue_text'])
    await message.clear_reactions()
    for game, emoji in server_variables[guild_id]['game_emojis'].items():
        await message.add_reaction(emoji)

async def clear_channels(ids):
    for id in ids:
        channel = client.get_channel(id)
        await channel.purge(limit=None, bulk=True)

async def remove_queue(user, game, type, guild_id):
    global server_variables
    n = game_n[game]
    queue = server_variables[guild_id]['queue']
    for i in range(len(queue[game])):
        if user in queue[game][i]:
            queue[game][i].remove(user)
            channel = client.get_channel(server_variables[guild_id]['queue_notifications_channel_id'])
            if type == 'inactive':
                msg = f'<@{user.id}>' + f' you have been removed from {game} (' + str(i + 1) + ') due to inactivity.'
            else:
                msg = str(user) + f' has left {game} (' + str(i + 1) + ').'
            await channel.send(msg)
            break
    
    channel = client.get_channel(server_variables[guild_id]['queue_channel_id'])
    message = await channel.fetch_message(server_variables[guild_id]['queue_id'])
    content = server_variables[guild_id]['queue_text']
    for game in games:
        for i in range(len(queue[game])):
            content += '\n' + game + ' (' + str(i + 1) + '): ' + ', '.join([str(j) for j in queue[game][i]])
        content += '\n'
    await message.edit(content=content)

async def delete_queue(users, game, guild_id):
    global server_variables
    queue = server_variables[guild_id]['queue']
    for i in queue[game]:
        if i == users:
            queue[game].remove(i)

    channel = client.get_channel(server_variables[guild_id]['queue_channel_id'])
    message = await channel.fetch_message(server_variables[guild_id]['queue_id'])
    content = server_variables[guild_id]['queue_text']
    for game in games:
        for i in range(len(queue[game])):
            content += '\n' + game + ' (' + str(i + 1) + '): ' + ', '.join([str(j) for j in queue[game][i]])
        content += '\n'
    await message.edit(content=content)

async def check_queue(message, users, game, guild_id):
    channel = client.get_channel(server_variables[guild_id]['queue_notifications_channel_id'])
    message = await message.channel.fetch_message(message.id)
    reacted = []
    async for i in message.reactions[0].users():
        reacted.append(i)
    if len(list(set(users).difference(set(reacted)))) == 0:
        await delete_queue(users, game, guild_id)
    else:
        channel = client.get_channel(server_variables[guild_id]['queue_channel_id'])
        message = await channel.fetch_message(server_variables[guild_id]['queue_id'])
        for reaction in message.reactions:
            if str(reaction.emoji) == server_variables[guild_id]['game_emojis'][game]:
                break
        for i in list(set(users).difference(set(reacted))):
            await remove_queue(i, game, 'inactive', guild_id)
            await reaction.remove(i)

async def join_queue(user, game, guild_id):
    global server_variables
    n = game_n[game]
    queue = server_variables[guild_id]['queue']
    if len(queue[game]) == 0:
        queue[game].append([])
        queue[game][-1].append(user)
        msg = str(user) + f' has started {game} (' + str(len(queue[game])) + ')!'
        channel = client.get_channel(server_variables[guild_id]['queue_notifications_channel_id'])
        role_name = game.lower().title()
        guild = await client.fetch_guild(guild_id)
        role = get(guild.roles, name=role_name)
        await channel.send(f'{role.mention} ' + msg)

    else:
        found = False
        for i in range(len(queue[game])):
            if len(queue[game][i]) < n:
                queue[game][i].append(user)
                channel = client.get_channel(server_variables[guild_id]['queue_notifications_channel_id'])
                msg = str(user) + f' has joined {game} (' + str(i + 1) + ').'
                await channel.send(msg)
                if len(queue[game][i]) == n - 1:
                    msg = f'{game} (' + str(i + 1) + ') needs one more player!'
                    await channel.send(msg)
                if len(queue[game][i]) == n:
                    msg = " ".join([f'<@{user.id}>' for user in queue[game][i]]) + ' Your queue is ready! React within 10 minutes to stay in the queue.'
                    msg = await channel.send(msg)
                    await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
                    run_at = datetime.datetime.now() + datetime.timedelta(minutes = 10)
                    global scheduler
                    scheduler.add_job(check_queue, 'date', run_date = run_at, args = [msg, queue[game][i], game, guild_id], timezone=pacific)
                found = True
                break
        if not found:
            queue[game].append([])
            queue[game][-1].append(user)
            msg = str(user) + f' has started {game} (' + str(len(queue[game])) + ')!'
            channel = client.get_channel(server_variables[guild_id]['queue_notifications_channel_id'])
            role_name = game.lower().title()
            guild = await client.fetch_guild(guild_id)
            role = get(guild.roles, name=role_name)
            await channel.send(f'{role.mention} ' + msg)

    channel = client.get_channel(server_variables[guild_id]['queue_channel_id'])
    message = await channel.fetch_message(server_variables[guild_id]['queue_id'])
    content = server_variables[guild_id]['queue_text']
    for game in games:
        for i in range(len(queue[game])):
            content += '\n' + game + ' (' + str(i + 1) + '): ' + ', '.join([str(j) for j in queue[game][i]])
        content += '\n'
    await message.edit(content=content)

async def create_event(message):
    guild_id = message.guild.id
    user = message.author
    content = message.content.split(' ')
    try:
        if len(content) < 4:
            msg = 'Please make sure your command structure is correct: !schedule game time(hour[req]:minute[opt][PST]) notify(Y/N) desc[opt]'
            await message.channel.send(f'{message.author.mention} ' + msg)
            return
        if content[1].lower().title() not in games:
            msg = 'Please double check the game spelling.'
            await message.channel.send(f'{message.author.mention} ' + msg)
            return
        if not content[2].replace(':', '').isdigit() or int(content[2].replace(':', '')) > 2359:
            msg = 'Please double check the time format: hour[req]:minute[opt][PST]'
            await message.channel.send(f'{message.author.mention} ' + msg)
            return
        if content[3].lower() not in ('y', 'n'):
            msg = 'Please choose either Y or N for the notify argument.'
            await message.channel.send(f'{message.author.mention} ' + msg)
            return
        desc = None
        if len(content) > 4:
            desc = ' '.join(content[4:])
        game = content[1]
        hour = int(content[2].split(':')[0])
        if len(content[2].split(':')) > 1:
            minute = int(content[2].split(':')[1])
        else:
            minute = 0
        run_at = datetime.time(hour=hour, minute=minute)
        notify = content[3].lower()
        channel = client.get_channel(server_variables[guild_id]['event_channel_id'])
        if notify == 'y':
            msg = str(user) + ' will be playing ' + f'{game.lower().title()}' + ' at ' + str(run_at)[:-3] + '. React to join!'
            role_name = game.lower().title()
            guild = await client.fetch_guild(guild_id)
            role = get(guild.roles, name=role_name)
            if desc is not None:
                msg += '\n\n Description: ' + desc
            msg = await channel.send(f'{role.mention} ' + msg)
        else:
            msg = str(user) + ' will be playing ' + f'{game.lower().title()}' + ' at ' + str(run_at)[:-3] + '. React to join!'
            if desc is not None:
                msg += '\n\n Description: ' + desc
            msg = await channel.send(msg)
        await msg.add_reaction('\N{WHITE HEAVY CHECK MARK}')
        global scheduler
        now = datetime.datetime.now(pacific)
        run_at = datetime.datetime.combine(now.date(), run_at)
        scheduled_datetime = datetime.datetime.combine(now.date(), now.time())
        if scheduled_datetime >= run_at:
            run_at += datetime.timedelta(days=1)
        scheduler.add_job(remind_event, 'date', run_date = run_at, args = [msg, user, game, channel, desc], timezone=pacific)
    except:
        msg = 'Error scheduling your event. \n\nPlease make sure your command structure is correct: \n!schedule game time(hour[req]:minute[opt][PST]) notify(Y/N) desc[opt]'
        await message.channel.send(f'{message.author.mention} ' + msg)

async def remind_event(message, user, game, channel, desc = None):
    reacted = []
    message = await message.channel.fetch_message(message.id)
    async for i in message.reactions[0].users():
        if i != client.user:
            reacted.append(i)
    if user not in reacted:
        reacted.append(user)
    msg = " ".join([f'<@{user.id}>' for user in reacted]) + " It's time to play " + f'{game.lower().title()}!'
    if desc is not None:
        msg += '\n\n Description: ' + desc
    await channel.send(msg)
    
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    global server_variables
    for guild in client.guilds:
        server_variables[guild.id] = {}
        channel = get(client.get_all_channels(), guild__name=guild.name, name='queue-notifications')
        server_variables[guild.id]['queue_notifications_channel_id'] = channel.id
        await channel.purge(limit=None, bulk=True)
        channel = get(client.get_all_channels(), guild__name=guild.name, name='bot-commands')
        server_variables[guild.id]['bot_channel_id'] = channel.id
        await channel.purge(limit=None, bulk=True)
        channel = get(client.get_all_channels(), guild__name=guild.name, name='events')
        server_variables[guild.id]['event_channel_id'] = channel.id
        await channel.purge(limit=None, bulk=True)
        channel = get(client.get_all_channels(), guild__name=guild.name, name='queues')
        server_variables[guild.id]['queue_channel_id'] = channel.id
        await channel.purge(limit=None, bulk=True)
        channel = get(client.get_all_channels(), guild__name=guild.name, name='help')
        await channel.purge(limit=None, bulk=True)
        await public_help(channel)

        # make individual queues and identify emojis for each game
        server_variables[guild.id]['queue'] = {}
        server_variables[guild.id]['game_emojis'] = {}
        server_variables[guild.id]['queue_text'] = 'Select the game you want to queue for: \n\n'
        for game in games:
            server_variables[guild.id]['queue'][game] = []
            server_variables[guild.id]['queue_text'] += '**' + str(game) + '** '
            for emoji in client.emojis:
                if emoji.name == game.lower():
                    server_variables[guild.id]['game_emojis'][game] = str(emoji)
                    server_variables[guild.id]['queue_text'] += str(emoji) + '\n'
                    break

        # display bot message with emojis
        channel = get(client.get_all_channels(), guild__name=guild.name, name='queues')
        msg = await channel.send(server_variables[guild.id]['queue_text'])
        server_variables[guild.id]['queue_id'] = msg.id

        # react to bot message with emojis
        for game, emoji in server_variables[guild.id]['game_emojis'].items():
            await msg.add_reaction(emoji)

        #queue clear schedule
        clear = []
        clear.append(server_variables[guild.id]['queue_notifications_channel_id'])
        clear.append(server_variables[guild.id]['bot_channel_id'])
        clear.append(server_variables[guild.id]['event_channel_id'])
        global scheduler
        scheduler.add_job(clear_queues, 'interval', args = [msg, guild.id], days=1, start_date='2022-01-01 7:00:00', timezone=pacific)
        scheduler.add_job(clear_channels, 'interval', args = [clear], days=1, start_date='2022-01-01 7:00:00', timezone=pacific)
        try:
            scheduler.start()
        except:
            pass

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
    
    if message.content == '!coin':
        await coinFlip(message)
        return
    
    if message.content.startswith('!schedule'):
        await create_event(message)

    if message.content.startswith('!server'):
        await server(message)
        
    #TESTING ONLY
#     if message.content.startswith('!test'):
#         game = message.content.split(' ')[1].lower().title()
#         await join_queue(client.user, game, list(server_variables.keys())[0])
#         return

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return
    
    guild_id = reaction.message.guild.id
    if reaction.message.id == server_variables[guild_id]['queue_id']:
        for game, emoji in server_variables[guild_id]['game_emojis'].items():
            if str(reaction.emoji) == emoji:
                await join_queue(user, game, guild_id)
                break
        return
            

@client.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == client.user.id:
        return

    guild_id = payload.guild_id
    if payload.message_id == server_variables[guild_id]['queue_id']:
        for game, emoji in server_variables[guild_id]['game_emojis'].items():
            if str(payload.emoji) == emoji:
                user = await client.fetch_user(payload.user_id)
                await remove_queue(user, game, 'left', guild_id)
                break
        return

client.run(TOKEN)
