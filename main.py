from PyQt5 import QtCore, QtGui, QtWidgets
from scapy.all import *

import sys
import threading

import interfaces
import maininterface


# Global Variables
hexdumps = []
capturedPackets = []
ui = interfaces.Ui_InterfacesWindow()
ui2 = maininterface.Ui_MainWindow()


def getPacketInfoDict(packet):
	print(packet)
	p = {}
	p['srcMac'] = packet.src
	p['dstMac'] = packet.dst
	ip = packet.payload
	if (packet.payload.name != 'ARP'):
		p["srcIP"] = ip.src
		p["dstIP"] = ip.dst
		p["srcPort"] = str(ip.sport)
		p["dstPort" ]= str(ip.dport)
		p["proto"] = ip.payload.name
	else:
		p["proto"] = packet.payload.name
	p["len"] = str(ip.len)
	p["time"] = str(packet.time)
	p["ipv"] = str(ip.version)
	return p

def getInterfacesList():
	ifList = []
	for i in ifaces.data.keys():
		ifList.append(i)
	return ifList

def startSniffing(interface):
	packets = sniff(iface=interface, prn=lambda x:showPacket(x))

def startHandlerOnInterfacesWindow():
	interface = ui.currentInterface()
	ui2.setupUi(MainWindow)
	thread = threading.Thread(target=startSniffing, args=(interface,))
	thread.start()
    

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



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui.setupUi(MainWindow)
    ui.addInterfaces(getInterfacesList())
    ui.connectStart(startHandlerOnInterfacesWindow)
    MainWindow.show()
    sys.exit(app.exec_())