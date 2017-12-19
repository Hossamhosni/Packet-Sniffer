from scapy.all import *
# Returns Packet's most important info in a dictionary to be used in the maininterface packettable
def getPacketInfoDict(packet):
	p = {}
	p['srcMac'] = packet.src
	p['dstMac'] = packet.dst
	p["time"] = str(packet.time)
	try:
		proto = packet.proto
		if (proto == 1):
			p["proto"] = "ICMP"
			p["srcIP"] = packet[IP].src
			p["dstIP"] = packet[IP].dst
			p["len"] = str(packet[IP].len)
			p["ipv"] = str(packet[IP].version)
		elif (proto == 6):
			p["proto"] = "TCP"
			p["len"] = str(packet[IP].len)
			p["ipv"] = str(packet[IP].version)
			p["srcPort"] = str(packet[IP].sport)
			p["dstPort" ]= str(packet[IP].dport)
			p["ipv"] = str(packet[IP].version)
		elif (proto == 17):
			p["proto"] = "UDP"
			p["len"] = str(packet.len)
			p["ipv"] = str(packet[IP].version)
			p["srcPort"] = str(packet[IP].sport)
			p["dstPort" ]= str(packet[IP].dport)
			p["ipv"] = str(packet[IP].version)
		else:
			pass#print("Unknown Protocol " + proto)
		if (p["srcPort"] == "80" or p["dstPort"] == "80"):
			if (p["srcPort"] == "80"):
				pass
			p["proto"] = "HTTP"
		p["srcIP"] = packet[IP].src
		p["dstIP"] = packet[IP].dst
	except(AttributeError):
		p["proto"] = packet.lastlayer().name
	return p