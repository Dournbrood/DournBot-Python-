
#Atom text editor - GitHub??

print("Firing up the ol' exception logger...")
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("Importing socket...")
try:
	import socket
	print("Socket import successful!")
except Exception as e:
	print("SOCKET IMPORT FAILED!")
	
print ("Importing time...")
try:
	import time
	print("time Imported successfully!")
except Exception as e:
	print("TIME IMPORT FAILED! CONCEPT TOO ABSTRACT AND HUMAN!")

print("Importing command manager...")
try:
	import cmdHandler
	print("Command manager imported successfully!")
except Exception as e:
	print("This one is your fault, Dourn. cmdHandler didn't import. FIX IT.")
	
print("Importing login...")
try:
	import login
	print("Login imported successfully!")
except Exception as e:
	print("LOGIN FILE FAILED TO IMPORT! BOT CANNOT FUNCTION ON SOME CHANNELS!")

#Setting variables. Probably will move this to a config file later.
botAuthName = login.username
botAuthPass = login.password
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cmdChar = "d?"
server = "chat.freenode.net" # Server
channel = "#powder-bots" # Channel
botnick = "DournBot" # Your bots nick.
adminname = "Dournbrood" #Your IRC nickname.
exitcode = "Bye " + botnick #Text that we will use
authConfirmMSG = "NOTICE " + botnick + " :You are now identified for " #This basically tests for the authorization confirmation message from NickServ.
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # user information
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # assign the nick to the bot

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
				
				if msgName != botnick:
				
					print("User " + msgHostname + " with nick " + msgName + " sent message from " + msgIP + " in channel " + msgChannel + ":\n\"" + msgContent + "\"")
					
							
					if msgName.lower() == adminname.lower():
						fromAdmin = 1
						
					cmdHandler.handle(msgName, msgHostname, msgIP, msgChannel, msgContent, fromAdmin) #Decided to move commands to their own file, and each command to its own file, subsequently. Things are bound to get messy.
				
				fromAdmin = 0 #Just to be safe.
				
			else:
			
				if ircmsg.find("PING :") != -1:
					pong()

		except Exception as e:
			print("CRITICAL ERROR. MESSAGE FAILED TO BE DISSECTED.")
			sendmsg("ERROR! Tell Dournbrood to check the bot's log!")
			logger.exception(e)
main()