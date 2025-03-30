import os
import discord
import random
import rank as rank

#global variables (kill me over it):
IDList = []
NAME_TOKEN = "general"
EMOJI1 = ":red_square:"
EMOJI2 = ":blue_square:"
EMOJI1SLASH = "🟥"
EMOJI2SLASH = "🟦"

#Get API key from API.env (This is not the safest way to do this)
try:
    f = open("environment/API.env", "r")
    TOKEN = str(f.read())
    f.close()
except:
    print("Could not load TOKEN file. Shutting down...")
    exit()

try:
    f = open("environment/guild.env", 'r')
    GUILD = int(f.read())
    f.close()
except:
    print("Could not load GUILD file. Shutting down...")
    exit()

try:
    f = open("environment/channels.env", 'r')
    CHANS = []
    for line in f:
        CHANS.append(int(line))
    f.close()
except:
    print("Could not load CHANNELS file. Shutting down...")
    exit()

try:
    f = open("environment/user.env", 'r')
    USER_TOKEN = str(f.read())
    f.close()
except:
    print("Could not load USER file. Shutting down...")
    exit()
    

async def PinGrab(message): #Grab all pins from every chat with "general" in the name
    ExtPins = []
    #Put all existing pins into array:
    reader = open("PinList.txt", 'r')
    writer = open("PinList.txt", 'w')
    for line in reader:
        ExtPins.append(line)
    reader.close()
    for channel in message.guild.channels:
        if "NAME_TOKEN" in channel.name:
            AllPins = await channel.pins()
            print(AllPins[0])
            for i in range(len(AllPins)):
                if AllPins[i] not in ExtPins:
                    print(str(AllPins[i].id))
                    writer.write(str(AllPins[i].id))
                    writer.write("\n")
    writer.close()
    
def PinSani(message): #Format discord message to be style of name: message fileurl fileurl... fileurl
    attachments = message.attachments
    ImgCount = len(attachments)
    content = message.author.name + ": " + message.content
    for i in range(ImgCount):
        content = content + " " + str(attachments[i])
    return content

async def GetMsg(ID): #Check all given general channels for the specified comment. Raise an error if message not in any channels.
    ID = int(ID)
    #print(GenChans)
    for channel in GenChans:
        try:
            #print(channel)
            message = await channel.fetch_message(id=ID)
            return message
        except:
            pass
    #print(ID)
    #print(type(ID))
    raise MsgNotFound

async def PrintList(channel): #DEBUG: print all of a list
    reader = open("PinList.txt", 'r')
    found = 0
    notfound = 0
    for line in reader:
        try: 
            message = await GetMsg(line)
            found += 1
            print(str(found) + " messages found!")
            message = PinSani(message)
            await channel.send(message)
        except:
            notfound += 1
            print(str(notfound) + " messages not found.")

async def GetVote(Pair, channel, match): #Sets up the vote
    match = str(match)
    await channel.send(EMOJI1 + "#############################################################################################" + EMOJI2)
    prologue = "Match " + match + "!"
    await channel.send(content=prologue)

    if (Pair.A == Pair.B): #If both items are the same, this isn't a vote, this is an empty round (rng do be like that)
        await channel.send(content="This is an empty round! Everybody loses!!!")
        return
    
    if (Pair.A == 0):
        try:
            await channel.send(content="This is a bye round! Does this pin deserve to live?")
            WinMsg = await GetMsg(Pair.B)
            WinMsgTxt = EMOJI2 +  PinSani(WinMsg)
            LoseMsgTxt = EMOJI1 + "Delete this pin!"
            await channel.send(content=WinMsgTxt)
            await channel.send(LoseMsgTxt)
        except:
            print("Failed to load B")
        

    elif (Pair.B == 0):
        try:
            await channel.send(content="This is a bye round! Does this pin deserve to live?")
            WinMsg = await GetMsg(Pair.A)
            WinMsgTxt = EMOJI1 + PinSani(WinMsg)
            LoseMsgTxt = EMOJI2 + "Delete this pin!"
            await channel.send(WinMsgTxt)
            await channel.send(LoseMsgTxt)

        except:
            print("Failed to load A")

    else:
        try:
            Msg1 = await(GetMsg(Pair.A))
            Msg1Txt = EMOJI1 + PinSani(Msg1)
            Msg2 = await(GetMsg(Pair.B))
            Msg2Txt = EMOJI2 + PinSani(Msg2)
            await channel.send("Which message should move forward?")
            await channel.send(Msg1Txt)
            await channel.send(Msg2Txt)
        except:
            print("failed to load one of two")
    
    VoteMsg = await channel.send("Vote here!")
    await VoteMsg.add_reaction(EMOJI1SLASH)
    await VoteMsg.add_reaction(EMOJI2SLASH)
    
    return str(VoteMsg.id) + " " + str(Pair.A) + " " + str(Pair.B) + "\n"


async def PrintWinner(winner, channel):
    print("Winner") #TODO: make the winner print

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    random.seed()
    global GenChans
    GenChans = []
    for Gen in CHANS:
        GenChan = await client.fetch_channel(Gen)
        GenChans.append(GenChan)

@client.event
async def on_message(message):
    if message.author == client.user: #Don't loop
        return
    if message.content[0] != "!": #! as command character
        return

    parsed_message = message.content.lower().split()
    print(message.author.name + ": " + " ".join(parsed_message)) #Display the message and who sent it on terminal
        
    if (parsed_message[0] == "!get"): #Get all pinned messages from all text channels with the token, store in a PinList.txt
        await PinGrab(message)
        
        
    if (parsed_message[0] == "!print"): #Debug printing
        """
        Gen1 = await client.fetch_channel(CHANS[0])
        Gen2 = await client.fetch_channel(CHANS[1])
        Gen3 = await client.fetch_channel(CHANS[2])
        Gen4 = await client.fetch_channel(CHANS[3])
        Gen5 = await client.fetch_channel(CHANS[4])
        GenChans = [Gen1, Gen2, Gen3, Gen4, Gen5]
        """
        await PrintList(message.channel)
        

    if ((parsed_message[0] == "!bracket") & (str(message.author.name) == USER_TOKEN)): #If admin says to, shuffle the bracket and fill it out to a power of 2
        reader = open("PinList.txt", 'r')
        #print("Heard Bracket")
        IDList.clear()
        for line in reader:
            IDList.append(int(line))
        #print(IDList)
        #count = len(IDList)
        #print(count)
        rank.BracketFill(IDList)
        #print(IDList)
        if (len(parsed_message) > 1):
            if (parsed_message[1] == "shuffle"):
                print("Every day I'm shuffling!")
                rank.BracketShuffle(IDList)
        #print(IDList)
        print("Messages bracketed.")

    if ((parsed_message[0] == "!rank") & (str(message.author.name) == USER_TOKEN)): #If admin says to, display the ranked options
        #print("Heard")
        PairList = []
        CurrentFile = open("CurrentMatch.txt", 'w')
        if (len(IDList) > 1):
            for i in range(int(len(IDList)/2)):
                print(i)
                PairList.append(rank.pair(IDList[i*2], IDList[i*2 + 1]))
            for i in range(len(PairList)):
                CurrMatch = await GetVote(PairList[i], message.channel, i)
                CurrentFile.write(CurrMatch)
            CurrentFile.close()
        else:
            await PrintWinner(IDList[0], message.channel)
        print("Ranking completed.")

    if ((parsed_message[0] == "!getresults") & (str(message.author.name) == USER_TOKEN)): #Separate into a win list and a lose list
        CurrentList = []
        CurrentFile = open("CurrentMatch.txt", 'r')
        WinnerList = open("WinnerList.txt", 'w')
        LoserList = open("LoserList.txt", 'w')
        for i,line in enumerate(CurrentFile):
            CurrentList.append(line.split())
            #print(CurrentList[i]) #This should be the voting message ID
            #print(CurrentList[i][0])
            ID = int(CurrentList[i][0])
            CurrVote = await message.channel.fetch_message(id=ID)
            Reacts = CurrVote.reactions
            #print(Reacts)
            if (Reacts[0].emoji == '🟥'):
                #print("Red first")
                RedReacts = Reacts[0].count
                #print(RedReacts)
                BlueReacts = Reacts[1].count
            elif (Reacts[1].emoji == '🟥'):
                print("Blue first")
                RedReacts = Reacts[1].count
                BlueReacts = Reacts[0].count
            else:
                print("Invalid read...")
            Match = rank.match(CurrentList[i][0], CurrentList[i][1], CurrentList[i][2], RedReacts, BlueReacts)
            Winner, Loser = Match.elaborate()
            WinnerList.write(str(Winner + "\n"))
            LoserList.write(str(Loser + "\n"))
        CurrentFile.close()
        WinnerList.close()
        LoserList.close()
        print("All matches evaluated. Winners in WinnerList.txt, losers in LoserList.txt.")

    if((parsed_message[0] == "!movedata") & (str(message.author.name) == USER_TOKEN)):
        WinFile = open("WinnerList.txt", 'r')
        PinFile = open("Pinlist.txt", 'w')
        for line in WinFile:
            PinFile.write(line)
        print("Data moved.")
        
        


#**************************************
#RUN BOT:
try:
    client.run(TOKEN)
except:
    client.close()