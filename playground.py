def showPacket(x):
	print(x.show())
	print('\n')
	if (x.payload.name == "IP" or x.payload.name == "IPv6"):
		ip = x.payload
		print("Source MAC: " + x.src)
		print("Destination MAC: " + x.dst)
		print("Source IP: " + ip.src)
		print("Destination IP: " + ip.dst)
		print("Source Port: " + str(ip.sport))
		print("Destination Port: " + str(ip.dport))
		print("Protocol: " + ip.payload.name)
		print("Length: " + str(ip.len))
		print("IP Version: " + str(ip.version))
	elif (x.payload.name == "ARP"):
		print("Source MAC: " + x.src)
		print("Destination MAC: " + x.dst)
	else:
		print("Source MAC:" + x.src)
		print("Destination MAC: " + x.dst)
		print("Packet: " + x.summary())
	print('\n')
	hexdumps.append(hexdump(x))
	capturedPackets.append(x)
	ui2.addPacketToList(getPacketInfoDict(x), x)