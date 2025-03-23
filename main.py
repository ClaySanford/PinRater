import os
import discord
import random

#Get API key from API.env (This is not the safest way to do this)
try:
    f = open("API.env", "r")
    TOKEN = f.read()
    f.close()
except:
    print("Could not load TOKEN file. Shutting down...")
    sys.exit()

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
    if (parsed_message == "!get"):
        print("Get it!")



#**************************************
#RUN BOT:

try:
    client.run(TOKEN)
except:
    client.close()

