
#Atom text editor - GitHub??

print("Firing up the ol' exception logger...")
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

try:
	import socket
	import time
	import cmdHandler
	import login
	import imp

except Exception as e:
	print("Oopsie woopsie!")
	logger.exception(e)

#Setting variables. Probably will move this to a config file later.
botAuthName = login.username
botAuthPass = login.password
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cmdChar = "d?"
server = "chat.freenode.net" # Server
channel = "#powder-bots" # Channel
botNick = "DournBot" # Your bots nick.
adminname = "Dournbrood" #Your IRC nickname.
exitcode = "Bye " + botNick #Text that we will use
authConfirmMSG = "NOTICE " + botNick + " :You are now identified for " #This basically tests for the authorization confirmation message from NickServ.


def connectAndWait():
	
	ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
	ircsock.send(bytes("USER "+ botNick +" "+ botNick +" "+ botNick + " " + botNick + "\n", "UTF-8")) # user information
	ircsock.send(bytes("NICK "+ botNick +"\n", "UTF-8")) # assign the nick to the bot
	ircmsg = ""
	connectMsg = " PRIVMSG " + botNick + " :VERSION"
	
	while 1:
		ircmsg = ircsock.recv(2048).decode("UTF-8")
		ircmsg = ircmsg.strip('\n\r')
		print(ircmsg)
		if ircmsg.find(connectMsg) == 1:
			print("No action taken.")
	print("Connected!")

def authWithNickServ(botAuthName, botAuthPass, authConfirmMSG): #Attempts to auth with nickserv. Program is stopped until this happens.
	ircsock.send(bytes("NICKSERV IDENTIFY " + botAuthName + " " + botAuthPass + "\n", "UTF-8")) #Sends message to NickServ with username and pass.
	print("Waiting for NickServ's verdict on the login attempt.")
	while 1: 
		ircmsg = ircsock.recv(2048).decode("UTF-8")
		ircmsg = ircmsg.strip('\n\r')
		print(ircmsg)
		if ircmsg.find(authConfirmMSG) == -1:
			print("No auth message yet.")
		else:
			print("Auth successful!")
			break
		
def joinchan(channel): # join channel(s).
	ircsock.send(bytes("JOIN "+ channel +"\n", "UTF-8")) 
	ircmsg = ""

	while ircmsg.find("End of /NAMES list.") == -1: 
		ircmsg = ircsock.recv(2048).decode("UTF-8")
		ircmsg = ircmsg.strip('\n\r')
		print(ircmsg)

def pong(): # respond to server Pings.
	ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target = channel): # sends messages to the target.
	ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))
	pass

def main():
	
	connectAndWait()
	authWithNickServ(botAuthName, botAuthPass, authConfirmMSG)
	joinchan(channel)
	
	
	while 1:
		ircmsg = ircsock.recv(2048).decode("UTF-8")
		ircmsg = ircmsg.strip('\n\r')
		print(ircmsg)

		# Messages come in from IRC in the format of: ":[Nick]!~[hostname]@[IP Address] PRIVMSG [channel] :[message]"
		try:
			if ircmsg.find("PRIVMSG") != -1: #if PRIVMSG is present in the message string, then go ahead and pick it apart. if not? just uh, send a ping
				msgName = ircmsg.split('!', 1)[0][1:]
				msgHostname = ircmsg.split('!', 1)[1].split('@', 1)[0]
				msgIP = ircmsg.split('@', 1)[1].split(' PRIVMSG', 1)[0]
				msgChannel = ircmsg.split('PRIVMSG ', 1)[1].split(' :', 1)[0]
				msgContent = ircmsg.split(' PRIVMSG ', 1)[1].split(':', 1)[1]
				
				if msgName != botNick:
				
					print("\n--NEW MESSAGE-- \n\nH: " + msgHostname + "\nNick: " + msgName + "\nIP: " + msgIP + "\nChannel: " + msgChannel + "\nMessage: \"" + msgContent + "\"")
					
							
					if msgName.lower() == adminname.lower():
						fromAdmin = 1
						
					if fromAdmin == 1 and msgContent[:8] == ("d?reload"):
						#cmdHandler.reloadPlugins()
						imp.reload(cmdHandler)
						sendmsg("Plugins and manager reloaded successfully!")
						
					cmdHandler.handle(msgName, msgHostname, msgIP, msgChannel, msgContent, fromAdmin) #Decided to move commands to their own file.
				
				fromAdmin = 0 #Just to be safe.
				
			else:
			
				if ircmsg.find("PING :") != -1:
					pong()

		except Exception as e:
			print("CRITICAL ERROR. MESSAGE FAILED TO BE DISSECTED.")
			sendmsg("ERROR! Tell Dournbrood to check the bot's log!")
			logger.exception(e)
main()