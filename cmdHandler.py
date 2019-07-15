import dournBotIRC

def handle(msgName, msgHostname, msgIP, msgChannel, msgContent, fromAdmin):
	dournBotIRC.sendmsg("Message received!")
	print(msgName, msgHostname, msgIP, msgChannel, msgContent, fromAdmin)
	pass