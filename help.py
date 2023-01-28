msg = '''
**__Commands__**

!help - bot instructions

!adopt - become Anju Son
!fan - become Anju Fanboy

!gun - random Valorant gun
!map - random Valorant map
!agent {X} - {X} random Valorant agents, default = 1
!strat - random Valorant strategy

**__Reactions__**

React with game icon to be added to game queue.
Unreact to be removed from game queue
    '''

async def help(message):
    await message.author.send(msg)

async def public_help(channel):
    pre = '=========================================================\n'
    post = '\n=========================================================\n\n\n.'
    await channel.send(pre + msg + post)
