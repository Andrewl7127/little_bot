import random
import requests

async def randomAgent(message):
    number = message.content.split(' ')
    if len(number) > 1: 
        if int(number[1]) > 5:
            await message.channel.send(f'{message.author.mention} HEY! THATS TOO MANY PPL')
            return
        number = int(number[1])
    else:
        number = 1

    controllers = ['Astra', 'Brimstone', 'Omen', 'Viper', 'Harbor']
    duelists = ['Jett', 'Neon', 'Phoenix', 'Raze', 'Reyna', 'Yoru']
    sentinels = ['Chamber', 'Cypher', 'Killjoy', 'Sage']
    initiators = ['Breach', 'KAY/O', 'Skye', 'Sova']

    roles = [controllers, duelists, sentinels, initiators]
    random.shuffle(roles)
    agent = []
    for n in range(number):
        if n < 4:
            agent_index = random.randint(0, len(roles[n]) - 1)
            agent.append(roles[n][agent_index])
        else:
            role_index = random.randint(0, len(roles) - 1)
            agent_index = random.randint(0, len(roles[role_index]) - 1)
            if roles[role_index][agent_index] in agent:
                agent_index -= 1
            agent.append(roles[role_index][agent_index])
    
    if number == 1:
        await message.channel.send(f'{message.author.mention} ' + agent[0])
    else:
        msg = ''
        for n in range(number):
            msg += 'Player ' + str(n+1) + ': ' + agent[n] + '\n'
        await message.channel.send(f'{message.author.mention} \n' + msg)

async def randomMap(message):
    maps = [
        'Ascent',
        'Bind',
        'Breeze',
        'Fracture',
        'Haven',
        'Icebox',
        'Lotus',
        'Pearl',
        'Split'
    ]

    await message.channel.send(f'{message.author.mention} ' + maps[random.randint(0, len(maps) - 1)])

async def randomGun(message):
    guns = [
        'Classic',
        'Shorty',
        'Frenzy',
        'Ghost',
        'Sheriff',
        'Stinger',
        'Spectre',
        'Bucky',
        'Judge',
        'Bulldog',
        'Guardian',
        'Phantom',
        'Vandal',
        'Marshall',
        'Operator',
        'Ares',
        'Odin'
    ]

    await message.channel.send(f'{message.author.mention} ' + guns[random.randint(0, len(guns) - 1)])


async def randomPistol(message):
    guns = [
        'Classic',
        'Shorty',
        'Frenzy',
        'Ghost',
        'Sheriff'
    ]

    await message.channel.send(f'{message.author.mention} ' + guns[random.randint(0, len(guns) - 1)])
