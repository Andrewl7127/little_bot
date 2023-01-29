msg = '''**__Commands__**

!help - bot instructions

!gun - random Valorant gun
!pistol - random Valorant pistol
!map - random Valorant map
!agent {X} - {X} random Valorant agents, default to 1
!strat - random Valorant strategy

!adopt - become Anju son
!fan - become Anju fanboy

**__Reactions__**

React with game icon to be added to the game queue
Unreact to be removed from the game queue

Queues, #queue-notifications, and #bot-commands reset daily at 7 am pst'''

async def help(message):
    await message.channel.send(f'{message.author.mention} ' + 'Sending help to your inbox!')
    await message.author.send(msg)

async def public_help(channel):
    pre = '=========================================================\n'
    post = '\n*Developed by Anju and Flurry*\n=========================================================\n\n\n.'
    await channel.send(pre + msg + post)
