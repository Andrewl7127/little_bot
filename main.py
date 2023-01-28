import discord
from discord.utils import get
from anju import *
from queue import *

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

queue_id = None
channel_id = None
queue_text = 'This is a test queue message\n\nCurrent members in queue: '
queue = []

valorant_emoji = None

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    channel = get(client.get_all_channels(), guild__name="Koffee", name='queues')
    global channel_id
    channel_id = channel.id
    await channel.purge(limit=None, bulk=True)
    msg = await channel.send(queue_text)
    global queue_id 
    queue_id = msg.id

    valorant = [emoji for emoji in client.emojis if emoji.name == 'valorant'][0]
    global valorant_emoji
    valorant_emoji = str(valorant)
    await msg.add_reaction(valorant_emoji)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!adopt':
        await adopt(message)

    if message.content == '!fan':
        await fan(message)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if reaction.message.id == queue_id:
        if str(reaction.emoji) == valorant_emoji:

            game = 'Valorant'
            global queue
            for i in queue:
                msg = str(user) + f' has joined the {game} queue!'
                await i.send(msg)

            queue.append(user)
            await user.send(f'You have been added to the {game} queue!')

            msg = f'Current members in {game} queue: '
            msg += ', '.join([str(i) for i in queue])
            await user.send(msg)

            channel = client.get_channel(channel_id)
            message = await channel.fetch_message(queue_id)
            content = queue_text + ', '.join([str(i) for i in queue])
            await message.edit(content=content)

@client.event
async def on_raw_reaction_remove(payload):
    if payload.user_id == client.user.id:
        return

    if payload.message_id == queue_id:
        if str(payload.emoji) == valorant_emoji:
            game = 'Valorant'
            user = await client.fetch_user(payload.user_id)
            global queue
            if user in queue:
                queue.remove(user)
                await user.send(f'You have been removed from the {game} queue!')
                for i in queue:
                    msg = str(user) + f' has left the {game} queue!'
                    await i.send(msg)
            
            channel = client.get_channel(channel_id)
            message = await channel.fetch_message(queue_id)
            content = queue_text + ', '.join([str(i) for i in queue])
            await message.edit(content=content)

client.run('MTA2ODQ0NTc0MzAyODkwMzk1Nw.Gs8pmX.QSZwpTj-Nvth9iXlWntG9ONuar7vp5K-ahwyYg')
