Discord bot designed to rank pinned messages in a server.
Your bot token needs to be stored in an otherwise empty file title "API.env" (in a folder titled environment)
Your guild ID needs to be stored in an otherwise empty file title "guild.env" (in a folder titled environment) 
Your channel IDs needs to be stored in an otherwise empty file title "channels.env" (in a folder titled environment)
Your admin username should be stored in an otherwise empty file titled "user.env" to use the actual ranking commands (in a folder titled environment)
!get pulls all pinned messages from all channels with "general" in the name and stores them in a PinList.txt file
!print prints all messages from this txt IFF supplied with a guild and channels enviroment file - This is a debug, it doesn't have any real functionality
!bracket takes the PinList.txt file and fills out the list so there are a power of 2 options. !bracket shuffle shuffles this list.
!rank prints out the vote for every item. Pulls from the item that !bracket puts out, so bracket is required after calling rank (especially if the bot resets)
!getresults prints out a list of winners and losers to separate text files, so that you can pick the best and worst posts.

This bot makes a lot of calls to discord's API, which has a pretty low rate limit. Due to this, it is very, very slow.
