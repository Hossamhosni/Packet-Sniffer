from mainWidget import Ui_MainWidget
from interfacesWidget import Ui_InterfacesWidget
from mainWindow import Ui_MainWindow

from utils import getPacketInfoDict
from PyQt5 import QtCore, QtGui, QtWidgets
from scapy.all import *
import threading
import globals

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.interfacesWidget = InterfacesWidget()
		self.mainWidget= MainWidget()
		self.setCentralWidget(self.interfacesWidget)
		self.actionSave_Packet.triggered.connect(self.savePacket)
		self.actionOpen_Packet.triggered.connect(self.openPacket)

	def savePacket(self):
		 name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
		 wrpcap(name[0] + ".pcap", self.mainWidget.getPacketList())

	def openPacket(self):
		name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
		self.mainWidget.clearPacketList()
		selectedPackets = rdpcap(name[0])
		self.mainWidget.addListOfPackets(selectedPackets)
		self.setCentralWidget(self.mainWidget)

	def closeEvent(self, event):
		globals.stop = True

	def connectStart(self, fn):
		self.actionStart.triggered.connect(fn)

	def connectStop(self, fn):
		self.actionStop.triggered.connect(fn)

	def connectRestart(self, fn):
		self.actionRestart.triggered.connect(fn)

	def addInterfaces(self, interfacesList):
		self.interfacesWidget.addInterfaces(interfacesList)

	def getCurrentInterface(self):
		try:
			self.currentInterface = self.interfacesWidget.currentInterface()
			return self.interfacesWidget.currentInterface()
		except(RuntimeError):
			return self.currentInterface

	def addPacketToList(self, packetDict, packet):
		self.mainWidget.addPacketToList(packetDict, packet)

	def clearPacketsList(self):
		self.mainWidget.clearPacketList()

	def setWidget(self, w):
		if (w == "Main"):
			self.setCentralWidget(self.mainWidget)
		else:
			self.setCentralWidget(self.interfacesWidget)

class InterfacesWidget(QtWidgets.QWidget, Ui_InterfacesWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setupUi(self)
	def addInterfaces(self, interfacesList):
		for i in interfacesList:
			self.interfacesList.addItem(i)
	def currentInterface(self):
		return self.interfacesList.currentText()

class MainWidget(QtWidgets.QWidget, Ui_MainWidget):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		self.setupUi(self)
		self.countPacket = 0
		self.packetList = []
		self.packetTable.itemClicked.connect(self.rowClicked)

	def clearPacketList(self):
		self.packetTable.setRowCount(0)
		self.packetList = []
		self.countPacket = 0

	def addListOfPackets(self, packetList):
		for packet in packetList:
			packet.show()
			self.addPacketToList(getPacketInfoDict(packet), packet)


	def getPacketList(self):
		return self.packetList

	def rowClicked(self):
		print("Hello")
		pass

	def addPacketToList(self, packetDict, originalPacket):
		self.packetTable.setRowCount(self.packetTable.rowCount() + 1)
		time = QtWidgets.QTableWidgetItem()
		src = QtWidgets.QTableWidgetItem()
		dst = QtWidgets.QTableWidgetItem()
		protocol = QtWidgets.QTableWidgetItem()
		length = QtWidgets.QTableWidgetItem()
		info = QtWidgets.QTableWidgetItem()

		hexa = QtWidgets.QListWidgetItem()

		# Set flags for each Widget
		time.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		src.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		dst.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		length.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		protocol.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		info.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)

		time.setText(originalPacket.sprintf("%.time%"))
		protocol.setText( packetDict["proto"])

		if (packetDict["proto"] == "UDP" or packetDict["proto"] == "TCP" or packetDict["proto"] == "HTTP"):
			src.setText( packetDict["srcIP"])
			dst.setText( packetDict["dstIP"])
			length.setText( str(packetDict["len"]))
			info.setText( packetDict["srcPort"] + " -> " + packetDict["dstPort"])
		else:
			src.setText( packetDict["srcMac"])
			dst.setText( packetDict["dstMac"])
		
		self.packetTable.setItem(self.countPacket, 1, time)
		self.packetTable.setItem(self.countPacket, 2, src)
		self.packetTable.setItem(self.countPacket, 3, dst)
		self.packetTable.setItem(self.countPacket, 4, protocol)
		self.packetTable.setItem(self.countPacket, 5, length)
		self.packetTable.setItem(self.countPacket, 6, info)
		for i in range(self.packetTable.rowCount() + 2):
			self.packetTable.setRowHeight(i, 20)

		self.packetList.append(originalPacket) # add packet to packet list 
		self.countPacket += 1 # increment packet count
