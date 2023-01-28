async def help(message):
    msg = '''
**__Commands__**

!adopt - become Anju Son
!fan - become Anju Fanboy

!gun - random Valorant gun
!map - random Valorant map
!agent X - X random Valorant agents, default = 1

**__Reactions__**

React with game icon to be added to game queue.
Unreact to be removed from game queue
    '''
    await message.author.send(msg)
