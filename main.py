from PyQt5 import QtCore, QtGui, QtWidgets
from scapy.all import *
import sys
import threading
from utils import getPacketInfoDict
from Gui import MainWindow
import globals


# Thread for Sniffing 
class SnifferThread(threading.Thread):
	def __init__(self, name, interface):
		threading.Thread.__init__(self)
		self.name = name
		self.interface = interface

	def run(self):
		global stop
		packets = sniff(iface=self.interface, prn=lambda x:showPacket(x), stop_callback= stop_callback)
		#packets = rdpcap("F:\Programming and Development\Python\scapy-http\example_network_traffic.pcap")
		#MainInterface.addListOfPackets(packets)

# Callback Function to stop Sniffing
def stop_callback():
	return globals.stop

# Adds Packet to Table in MainInterface
def showPacket(x):
	#print(x.show())
	#capturedPackets.append(x)
	mainWindow.addPacketToList(getPacketInfoDict(x), x)

### Action Handlers ###



# Handler for pressing the Stop Button in the MainWindow
def stopHandler():
	globals.stop = True

def startHandler():
	globals.stop = False
	try:
		mainWindow.setWidget("Main")
		mainWindow.clearPacketsList()
		thread = SnifferThread("Sniffer", mainWindow.getCurrentInterface())
		thread.start()
	except(AttributeError):
		mainWindow.setWidget("Other")



# Get interfaces list to be shown in the interfaces window
def getInterfacesList():
	ifList = []
	for i in ifaces.data.keys():
		ifList.append(i)
	return ifList

if __name__ == "__main__":

	global ui
	app = QtWidgets.QApplication(sys.argv)
	globals.init()
	mainWindow = MainWindow()
	mainWindow.connectStart(startHandler)
	mainWindow.connectRestart(startHandler)
	mainWindow.connectStop(stopHandler)
	mainWindow.addInterfaces(getInterfacesList())
	mainWindow.show()
	sys.exit(app.exec_())