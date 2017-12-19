from interfaces import Ui_InterfacesWindow
from maininterface import Ui_MainWindow
from utils import getPacketInfoDict
from PyQt5 import QtCore, QtGui, QtWidgets
from scapy.all import *
import threading

class InterfacesWindow(QtWidgets.QMainWindow, Ui_InterfacesWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.actionSave_Packet.triggered.connect(self.savePacket)
		self.actionOpen_Packet.triggered.connect(self.openPacket)
		self.interfacesList
	def savePacket(self):
		pass
	def openPacket(self):
		pass

	def addInterfaces(self, interfacesList):
		for i in interfacesList:
			self.interfacesList.addItem(i)

	def currentInterface(self):
		return self.interfacesList.currentText()

	def connectStart(self, fn):
		self.actionStart.triggered.connect(fn)

class Main(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.actionSave_Packet.triggered.connect(self.savePacket)
		self.actionOpen_Packet.triggered.connect(self.openPacket)
		self.packetTable.itemClicked.connect(self.rowClicked)
		self.countPacket = 0
		self.packetList = []

	def closeEvent(self, event):
		pass

	def rowClicked(self):
		pass

	def savePacket(self):
		pass

	def openPacket(self):
		pass

	def clearPacketList(self):
		self.packetTable.setRowCount(0)
		self.packetList = []
		self.countPacket = 0

	def addListOfPackets(self, packetList):
		for packet in packetList:
			self.addPacketToList(getPacketInfoDict(packet), packet)

	def connectStart(self, fn):
		self.actionStart.triggered.connect(fn)

	def connectStop(self, fn):
		self.actionStop.triggered.connect(fn)

	def connectRestart(self, fn):
		self.actionRestart.triggered.connect(fn)

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

		time.setText( originalPacket.sprintf("%.time%"))
		protocol.setText( packetDict["proto"])

		if (packetDict["proto"] == "UDP" or packetDict["proto"] == "TCP"):
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

