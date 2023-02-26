msg = '''**__Commands__**

!help - bot instructions

**__Queues__**

React with game icon to be added to the game queue
Unreact to be removed from the game queue
Once queue is ready, react within 10 minutes to stay in the queue

**__Events__**

!schedule {game} {time} {notify} {desc} - schedule game event at certain time

**__Randomize__**

!gun - random Valorant gun
!pistol - random Valorant pistol
!map - random Valorant map
!agent {n} - random Valorant agents, defaults to 1

** __Misc__**

!adopt - become Anju son
!fan - become Anju fanboy

#queues, #queue-notifications, #events, and #bot-commands reset daily at 7 am pst
Recommended to turn notification settings to only @mentions'''

async def help(message):
    try:
        await message.author.send(msg)
        await message.channel.send(f'{message.author.mention} ' + 'Sent help to your inbox!')
    except:
        await message.channel.send(f'{message.author.mention} ' + 'Sorry, but I was unable to reach your inbox.')

async def public_help(channel):
    pre = '=========================================================\n'
    post = '\n\n*Developed by Anju and Flurry*\n========================================================='
    await channel.send(pre + msg + post)
