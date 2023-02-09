msg = '''**__Commands__**

!help - bot instructions

!gun - random Valorant gun
!pistol - random Valorant pistol
!map - random Valorant map
!agent {x} - {x} # of random Valorant agents, defaults to 1
!strat - random Valorant strategy

!adopt - become Anju son
!fan - become Anju fanboy

**__Reactions__**

React with game icon to be added to the game queue
Unreact to be removed from the game queue
Once queue is ready, react within 10 minutes to stay in the queue

Queues, #queue-notifications, and #bot-commands reset daily at 7 am pst
Recommended to turn notification settings for #queues, #queue-notifications, and #bot-commands to only @mentions'''

async def help(message):
    try:
        await message.author.send(msg)
        await message.channel.send(f'{message.author.mention} ' + 'Sent help to your inbox!')
    except:
        await message.channel.send(f'{message.author.mention} ' + 'Sorry, but I was unable to reach your inbox.')

async def public_help(channel):
    pre = '=========================================================\n'
    post = '\n\n*Developed by Anju and Flurry*\n=========================================================\n\n\n.'
    await channel.send(pre + msg + post)
