




def handle(msgName, msgHostname, msgIP, msgChannel, msgContent, fromAdmin, sendmsg, channel):
	sendmsg("Message received!", channel)
	print(msgName, msgHostname, msgIP, msgChannel, msgContent, fromAdmin)
	pass