async def adopt(message):
    names = []
    async for member in message.guild.fetch_members():
        if member.nick:
            names.append(member.nick)
        else:
            names.append(member.name)
    sons = []
    for i in names:
        if 'anju' in i.lower() and 'son' in i.lower():
            sons.append(i)
    if len(sons) > 0:
        sons = [int(''.join([j for j in i if j.isnumeric()])) for i in sons]
        sons = [i for i in sons if type(i) == int]
        msg = 'Congratulations, you have been assigned as #' + str(max(sons) + 1) + ' Son!'
        await message.channel.send(msg)
        next = "Anju's #" + str(max(sons) + 1) + ' Son'
        await message.author.edit(nick=next)
    else:
        msg = 'Congratulations, you have been assigned as #1 Son!'
        await message.channel.send(msg)
        next = "Anju's #1 Son"
        await message.author.edit(nick=next)

async def fan(message):
    names = []
    async for member in message.guild.fetch_members():
        if member.nick:
            names.append(member.nick)
        else:
            names.append(member.name)
    fanboys = []
    for i in names:
        if 'anju' in i.lower() and 'fanboy' in i.lower():
            fanboys.append(i)
    if len(fanboys) > 0:
        fanboys = [int(''.join([j for j in i if j.isnumeric()])) for i in fanboys]
        fanboys = [i for i in fanboys if type(i) == int]
        msg = 'Congratulations, you have been assigned as #' + str(max(fanboys) + 1) + ' Fanboy!'
        await message.channel.send(msg)
        next = "Anju's #" + str(max(fanboys) + 1) + ' Fanboy'
        await message.author.edit(nick=next)
    else:
        msg = 'Congratulations, you have been assigned as #1 Fanboy!'
        await message.channel.send(msg)
        next = "Anju's #1 Fanboy"
        await message.author.edit(nick=next)