


cmdList = ['help']
adminCmdList = ['reload', 'quit']

def cmdHelp(fromAdmin, sendmsg, msgName, args):
	print('\'' + args + '\'')
	if fromAdmin == 0:
		sendmsg(msgName + "'s available commands: " + ', '.join(cmdList))
	else:
		sendmsg(msgName + "'s available commands: " + ', '.join(cmdList + adminCmdList))

def handle(msgName, msgHostname, msgIdent, msgChannel, msgContent, fromAdmin, sendmsg, channel):
	
	if msgContent[:2] == "d?":
	
		cmdID = msgContent.split('d?', 1)[1].split(' ', 1)[0]
		args = msgContent.split('d?', 1)[1].split(cmdID, 1)[1][1:]
		
		if cmdID in cmdList:
	
			if cmdID == cmdList[0]:
				cmdHelp(fromAdmin, sendmsg, msgName, args)
		
		else:
		
			if cmdID in adminCmdList:
			
				if fromAdmin == 1:
					pass
				
				else:
					print("\n!!!---[ALERT]---!!!\nUnauthorized user " + msgHostname + " attempted to run " + cmdID + " " + args + ". ")
					sendmsg("Sorry, " + msgName + ". You are not authorized to use d?" + cmdID + "! Please contact a channel administrator if you believe this is in error.")
			
			else:
				sendmsg("d?" + cmdID + " is not a recognized command! Use d?help to see a list of valid commands.")