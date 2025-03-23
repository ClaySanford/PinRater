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



#**************************************
#RUN BOT:
try:
    clinet.run(TOKEN)
except:
    client.close()