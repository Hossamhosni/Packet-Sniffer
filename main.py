from PyQt5 import QtCore, QtGui, QtWidgets
from scapy.all import *
import sys
import threading
from utils import getPacketInfoDict
from Gui import Main, InterfacesWindow


# Global Variables
capturedPackets = []

global stop
stop = False


# Thread for Sniffing 
class SnifferThread(threading.Thread):
	def __init__(self, name, interface):
		threading.Thread.__init__(self)
		self.name = name
		self.interface = interface

	def run(self):
		global stop
		packets = sniff(iface=self.interface, prn=lambda x:showPacket(x), stop_callback= stop_callback)
		#packets = sniff(count = 4)
		#MainInterface.addListOfPackets(packets)

# Callback Function to stop Sniffing
def stop_callback():
	return stop

# Adds Packet to Table in MainInterface
def showPacket(x):
	#print(x.show())
	capturedPackets.append(x)
	MainInterface.addPacketToList(getPacketInfoDict(x), x)

### Action Handlers ###
# Handler for pressing the Start button in the interfaces window
def startHandlerOnInterfacesWindow():
	global interface
	interface = ui.currentInterface()
	MainInterface.show()
	ui.hide()
	MainInterface.connectStop(stopHandlerOnMainWindow)
	MainInterface.connectStart(startHandlerOnMainWindow)
	MainInterface.connectRestart(startHandlerOnMainWindow)
	thread = SnifferThread("Sniffer", interface)
	thread.start()


# Handler for pressing the Stop Button in the MainWindow
def stopHandlerOnMainWindow():
	global stop
	stop = True

def startHandlerOnMainWindow():
	global interface
	global stop
	global MainWindow
	stop = False
	MainInterface.clearPacketList()
	thread = SnifferThread("Sniffer", interface)
	thread.start()


# Get interfaces list to be shown in the interfaces window
def getInterfacesList():
	ifList = []
	for i in ifaces.data.keys():
		ifList.append(i)
	return ifList

if __name__ == "__main__":

	global ui
	global MainInterface
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	MainInterface = Main()
	ui = InterfacesWindow()
	ui.show()
	ui.addInterfaces(getInterfacesList())
	ui.connectStart(startHandlerOnInterfacesWindow)
	sys.exit(app.exec_())