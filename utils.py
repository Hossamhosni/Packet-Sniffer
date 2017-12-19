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

def hexdump2(x, dump=False):
	s=""
	x=bytes(x)
	l=len(x)
	i=0
	while i<l:
		s+=("%04x "%i)
		for j in range(16):
			if (i + j < 1):
				s += ("%02X " % orb(x[i+j]))
			else:
				s += " "
			if j%16==7:
				s+=" "
		s+=" "
		s+=sane_color(x[i:i+16])
		i+=16
		s+="\n"
	if s.endswith("\n"):
		s=s[:-1]
	if dump:
		return s
	else:
		print (s)

def hexdump3(x, dump = False):
	s = ""
	if type(x) is not str and type(x) is not bytes:
		try:
			x = bytes(x)
		except:
			x = str(x)
	l = len(x)
	i = 0
	while i < l:
		s += ("%04x  \t" % i)
		for j in range(16):
			if i+j < l:
				s += ("%02X " % orb(x[i+j]))
			else:
				s += ("  ")
			if j%16 == 7:
				s += (" ")
		s += ("\t\t")
		s +=(sane_color(x[i:i+16]) + '\n')
		i += 16
	return s