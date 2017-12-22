from scapy.all import *

# Returns Packet's most important info in a dictionary to be used in the maininterface packettable
def getPacketInfoDict(packet):
	p = {}
	p['srcMac'] = packet[Ether].src
	p['dstMac'] = packet[Ether].dst
	p['time'] = str(packet.time)
	p['len'] = str(len(packet))

	# ARP Support
	if (packet.haslayer(ARP)):
		p['proto'] = 'ARP'
		p['ARPSrc'] = packet[ARP].psrc
		p['ARPDst'] = packet[ARP].pdst
		p['ARPMacDst'] = packet[ARP].hwdst
		p['ARPMacSrc'] = packet[ARP].hwsrc
		print(packet[ARP].op)
		if (packet[ARP].op == 1):
			p['ARPop'] = 'who has'
		elif (packet[ARP].op == 2):
			p['ARPop'] = 'is at'
		try:
			if (p['ARPop'] == 'who has'):
				p['info'] = p['ARPop'] + ' ' + packet[ARP].pdst + '? tell ' + packet[ARP].psrc
			elif (p['ARPop'] == 'is at'):
				p['info'] = packet[ARP].psrc + ' is at ' + p['srcMac']
		except(TypeError):
			p['info'] = ""
		return p
	if (packet.haslayer(IP)):
		p['IPsrc'] = packet[IP].src
		p['IPdst'] = packet[IP].dst
		p['IPVersion'] = str(packet[IP].version)
		p['IPttl'] = str(packet[IP].ttl)
		p['IPcheckSum'] = packet[IP].chksum
		p['IPlen'] = str(packet[IP].len)
	if (packet.haslayer(IPv6)):
		p['IPsrc'] = packet[IPv6].src
		p['IPdst'] = packet[IPv6].dst
		p['IPVersion'] = '6'
		p['IPlen'] = packet[IPv6].plen
	# TCP and UDP
	if (packet.haslayer(UDP) or packet.haslayer(TCP)):
		if (packet.haslayer(UDP)):
			p['proto'] = 'UDP'
			p['srcPort'] = str(packet[UDP].sport)
			p['dstPort'] = str(packet[UDP].dport)
			p['UDPcheckSum'] = packet[UDP].chksum
			p['UDPlen'] = str(packet[UDP].len)
		elif(packet.haslayer(TCP)):
			p['proto'] = 'TCP'
			p['srcPort'] = str(packet[TCP].sport)
			p['dstPort'] = str(packet[TCP].dport)
			p['TCPcheckSum'] = packet[TCP].chksum
		return p
	# ICMP
	if (packet.haslayer(ICMP)):
		p['proto'] = 'ICMP'
		p['IPsrc'] = packet[IP].src
		p['IPdst'] = packet[IP].dst
		p['IPVersion'] = str(packet[IP].version)
		return p
	else:
		p['proto'] = packet.lastlayer().name
		return p

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
