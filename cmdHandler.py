cmdList = ["help"]
adminCmdList = ["reload", "quit"]

def sendAdvancedSubcommandInfo(sendmsg, helpMsg, msgName):
	sendmsg(msgName + ": " + helpMsg)
	
def backdoor(msgName, msgHostname, msgIdent, msgChannel, msgContent, fromAdmin, sendmsg, channel, args):
	sendmsg("So you want to know, do you " + msgName + "? Payments can be made in Bitcoin. DM Dournbrood when he's around for more information | Disclaimer: Backdoor payments are not real, there is no backdoor on the bot, and I do not wish to solicit funds from you or your peers.")
	msgName, msgHostname, msgIdent, msgChannel, msgContent, fromAdmin, sendmsg, channel, args

helpDict = {
	"help": "d?help <Command> | We put help in your help to help you helping yourself more. You're welcome.",
	"reload": "d?reload | Reloads everything on the bot except for the IRC connection. Only usable by admins or users who paid me enough for the back door.",
	"quit": "d?quit <Reason> | Quits the bot and murders the program. Running this generates an extensive log file documenting the time, source of the message, what channel it was in, and what the reason was. Obviously only usable by admins or backdoor patreons.",
	"backdoor": backdoor
}

def cmdHelp(msgName, msgHostname, msgIdent, msgChannel, msgContent, fromAdmin, sendmsg, channel, args):
	print('\'' + args + '\'')
	if not args:
		if fromAdmin == 0:
			sendmsg(msgName + "'s available commands: " + ', '.join(cmdList))
			return
		else:
			sendmsg(msgName + "'s available commands: " + ', '.join(cmdList + adminCmdList))
			return
	if args in helpDict:
		helpMsg = helpDict[args]
		sendAdvancedSubcommandInfo(sendmsg, helpMsg, msgName)
		return	

cmdDict = {
	"help": cmdHelp
}

def handle(msgName, msgHostname, msgIdent, msgChannel, msgContent, fromAdmin, sendmsg, channel):
	
	if msgContent[:2] == "d?":
	
		cmdID = msgContent.split('d?', 1)[1].split(' ', 1)[0]
		
		if msgContent.find(cmdID + ' ') != -1:
			args = msgContent.split('d?', 1)[1].split(cmdID, 1)[1][1:]
		else:
			args = ''
			
		if cmdID in cmdDict:
		
			doot = cmdDict[cmdID]
			doot(msgName, msgHostname, msgIdent, msgChannel, msgContent, fromAdmin, sendmsg, channel, args)
		
		else:
		
			if cmdID in adminCmdList:
			
				if fromAdmin == 1:
					pass
				
				else:
					print("\n!!!---[ALERT]---!!!\nUnauthorized user " + msgHostname + " attempted to run " + cmdID + " " + args + ". ")
					sendmsg("Sorry, " + msgName + ". You are not authorized to use d?" + cmdID + "! Please contact a channel administrator if you believe this is in error.")
			
			else:
				sendmsg("d?" + cmdID + " is not a recognized command! Use d?help to see a list of valid commands.")