import os
import discord
import random
import ranking.py
#Get API key from API.env (This is not the safest way to do this)
try:
    f = open("API.env", "r")
    TOKEN = f.read()
    f.close()
except:
    print("Could not load TOKEN file. Shutting down...")
    exit()

try:
    f = open("guild.env", 'r')
    GUILD = f.read()
    f.close
except:
    print("Could not load GUILD file. Shutting down...")
    exit()

try:
    f = open("channels.env", 'r')
    CHANS = []
    for line in f:
        CHANS.append(int(line))
    f.close()
except:
    print("Could not load CHANNELS file. Shutting down...")
    exit()

async def PinGrab(message):
    ExtPins = []
    #Put all existing pins into array:
    reader = open("PinList.txt", 'r')
    for line in reader:
        ExtPins.append(line)
    reader.close()
    for channel in message.guild.channels:
        if "general" in channel.name:
            AllPins = await channel.pins()
            writer = open("PinList.txt", 'a')
            print(AllPins[0])
            for i in range(len(AllPins)):
                if AllPins[i] not in ExtPins:
                    print(str(AllPins[i].id))
                    writer.write(str(AllPins[i].id))
                    writer.write("\n")
            writer.close()
    
def PinSani(message):
    attachments = message.attachments
    ImgCount = len(attachments)
    content = message.author.name + ": " + message.content
    for i in range(ImgCount):
        content = content + " " + str(attachments[i])
    return content

async def GetMsg(GenChans, ID):
    for channel in GenChans:
        try:
            message = await channel.fetch_message(id=ID)
            return message
        except:
            pass
    raise MsgNotFound

async def PrintList(channel, GenChans):
    reader = open("PinList.txt", 'r')
    found = 0
    notfound = 0
    for line in reader:
        try: 
            message = await GetMsg(GenChans, line)
            found += 1
            print(str(found) + " messages found!")
            message = PinSani(message)
            await channel.send(message)
        except:
            notfound += 1
            print(str(notfound) + " messages not found.")
            LostIDs.append(line)


client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content[0] != "!":
        return
    parsed_message = message.content.lower().split()
    print(message.author.name + ": " + " ".join(parsed_message))
    if (parsed_message[0] == "!get"):
        await PinGrab(message)
    if (parsed_message[0] == "!print"):
        Gen1 = await client.fetch_channel(CHANS[0])
        Gen2 = await client.fetch_channel(CHANS[1])
        Gen3 = await client.fetch_channel(CHANS[2])
        Gen4 = await client.fetch_channel(CHANS[3])
        Gen5 = await client.fetch_channel(CHANS[4])
        GenChans = [Gen1, Gen2, Gen3, Gen4, Gen5]
        await PrintList(message.channel, GenChans)
        print(LostIDs)


#**************************************
#RUN BOT:
try:
    client.run(TOKEN)
except:
    client.close()