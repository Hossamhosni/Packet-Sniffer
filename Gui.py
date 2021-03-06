from mainWidget import Ui_MainWidget
from interfacesWidget import Ui_InterfacesWidget
from mainWindow import Ui_MainWindow
from utils import *
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
		self.parentWidget = QtWidgets.QStackedWidget(self)
		self.parentWidget.addWidget(self.mainWidget)
		self.parentWidget.addWidget(self.interfacesWidget)
		self.setCentralWidget(self.parentWidget)
		self.parentWidget.setCurrentWidget(self.interfacesWidget)
		self.actionSave_Packet.setEnabled(False)
		self.actionSave_Packet.triggered.connect(self.savePacket)
		self.actionOpen_Packet.triggered.connect(self.openPacket)
		self.actionQuit.triggered.connect(self.Quit)


	def savePacket(self):
		name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
		wrpcap(name[0] + ".pcap", self.mainWidget.getPacketList())

	def openPacket(self):
		name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
		self.mainWidget.clearPacketList()
		selectedPackets = rdpcap(name[0])
		self.mainWidget.addListOfPackets(selectedPackets)
		self.parentWidget.setCurrentWidget(self.mainWidget)
		self.actionSave_Packet.setEnabled(True)
		globals.stop = True

	def Quit(self):
		if (self.parentWidget.currentWidget() == self.mainWidget):
			buttonReply = QtWidgets.QMessageBox.question(self,
			 'Unsaved packets...', "Do you want to stop the capture and save the captured packets before quitting?",
			  QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel)
			if buttonReply == QtWidgets.QMessageBox.Save:
				globals.stop = True
				name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
				wrpcap(name[0] + ".pcap", self.mainWidget.getPacketList())
				sys.exit()
			elif buttonReply == QtWidgets.QMessageBox.Discard:
				globals.stop = True
				sys.exit()
			else:
				pass
		else:
			globals.stop = True
			sys.exit()

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
			self.parentWidget.setCurrentWidget(self.mainWidget)
			self.actionSave_Packet.setEnabled(True)
		else:
			self.parentWidget.setCurrentWidget(self.interfacesWidget)

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
		self.hexView.setStyleSheet("font: 9pt Consolas")
		self.packetTable.setStyleSheet("font: 9pt Consolas")
		self.packetInfo.setStyleSheet("font: 9pt Consolas")
		self.packetTable.horizontalHeader().setStretchLastSection(True)
		self.filterButton.clicked.connect(self.filterFunction)

	def clearPacketList(self):
		self.packetTable.setRowCount(0)
		self.packetList = []
		self.countPacket = 0

	def addListOfPackets(self, packetList):
		for packet in packetList:
			self.addPacketToList(getPacketInfoDict(packet), packet)


	def getPacketList(self):
		return self.packetList

	def rowClicked(self):
		#hex part
		rowNum = self.packetTable.currentRow()
		hexItem = QtWidgets.QListWidgetItem()
		hexItem.setText(hexdump3(self.packetList[rowNum], True))
		self.hexView.clear()
		self.hexView.addItem(hexItem)
		print(self.packetList[rowNum].show())
		print(len(self.packetList[rowNum]))

		#packet info part
		self.packetInfo.setHeaderLabel("Packet Information:")
		self.packetInfo.clear()
		#parents
		infoDict = getPacketInfoDict(self.packetList[rowNum])
		proto = infoDict["proto"]

		FirstLayer = QtWidgets.QTreeWidgetItem(self.packetInfo)
		FirstLayer.setText(0,"Ethernet")
		childItem = QtWidgets.QTreeWidgetItem(FirstLayer)
		childItem.setText(0,"Source MAC: "+infoDict["srcMac"] + ", "+"Destination MAC: "+infoDict["dstMac"])

		if (proto == "ARP"):
			try:
				SecondLayer = QtWidgets.QTreeWidgetItem(self.packetInfo)
				SecondLayer.setText(0,"Address Resolution Protocol (ARP)")
				childItem2 = QtWidgets.QTreeWidgetItem(SecondLayer)
				childItem2.setText(0,"Source IP: " + infoDict["ARPSrc"]+ ", "+"Destination IP: "+infoDict["ARPDst"])
				if (infoDict['ARPop'] == 'who has' or infoDict['ARPop'] == 'is at'):
					childItem23 = QtWidgets.QTreeWidgetItem(SecondLayer)
					childItem23.setText(0, "Source Mac:" + infoDict['ARPMacSrc'])
					childItem23 = QtWidgets.QTreeWidgetItem(SecondLayer)
					childItem23.setText(0, "Target Mac:" + infoDict['ARPMacDst'])
			except(KeyError):
				pass

		else:
			try:
				SecondLayer = QtWidgets.QTreeWidgetItem(self.packetInfo)
				SecondLayer.setText(0,"Internet Protocol (IP)"+" Version: "+infoDict["IPVersion"])
				childItem2 = QtWidgets.QTreeWidgetItem(SecondLayer)
				childItem2.setText(0,"Source IP: "+infoDict["IPsrc"]+ ", "+"Destination IP: "+infoDict["IPdst"])
				childItem23 = QtWidgets.QTreeWidgetItem(SecondLayer)
				childItem23.setText(0,"Length: "+infoDict["IPlen"])
				if (infoDict["IPVersion"] == '4'):
					childItem22 = QtWidgets.QTreeWidgetItem(SecondLayer)
					childItem22.setText(0,"Time to live: "+infoDict["IPttl"])
					childItem24 = QtWidgets.QTreeWidgetItem(SecondLayer)
					childItem24.setText(0,"Checksum: " + str(infoDict["IPcheckSum"]))
			except(KeyError):
				pass

			try:
				if proto == "UDP":
					ThirdLayer = QtWidgets.QTreeWidgetItem(self.packetInfo)
					ThirdLayer.setText(0,"User Datagram Protocol (UDP)")
					childItem3 = QtWidgets.QTreeWidgetItem(ThirdLayer)
					childItem3.setText(0,"Source Port: "+infoDict["srcPort"] + ", Destination Port: "+infoDict["dstPort"])
					childItem32 = QtWidgets.QTreeWidgetItem(ThirdLayer)
					childItem32.setText(0,"Checksum: "+str(infoDict["UDPcheckSum"]))
					childItem33 = QtWidgets.QTreeWidgetItem(ThirdLayer)
					childItem33.setText(0,"Length: "+infoDict["UDPlen"])

				elif proto == "TCP":
					ThirdLayer = QtWidgets.QTreeWidgetItem(self.packetInfo)
					ThirdLayer.setText(0,"Transmission Control Protocol (TCP)")
					childItem3 = QtWidgets.QTreeWidgetItem(ThirdLayer)
					childItem3.setText(0,"Source Port: " + infoDict["srcPort"] + ", Destination Port: " + infoDict["dstPort"])
					childItem32 = QtWidgets.QTreeWidgetItem(ThirdLayer)
					childItem32.setText(0,"Checksum: " + str(infoDict["TCPcheckSum"]))
				elif proto == "ICMP":
					ThirdLayer = QtWidgets.QTreeWidgetItem(self.packetInfo)
					ThirdLayer.setText(0, "Internet Control Message Protocol (ICMP)")
					childType = QtWidgets.QTreeWidgetItem(ThirdLayer)
					childType.setText(0, "Type: " + infoDict['ICMPtype'])
					childCode = QtWidgets.QTreeWidgetItem(ThirdLayer)
					childCode.setText(0, "Code: " + infoDict['ICMPcode'])
					childCheckSum = QtWidgets.QTreeWidgetItem(ThirdLayer)
					childCheckSum.setText(0, "Checksum: " + infoDict['ICMPcheckSum'])
			except(KeyError):
				pass

	def filterFunction(self):
		query = self.lineEdit.text()
		filteredList = []
		protocols = ['udp', 'tcp', 'http', 'icmp', 'arp']
		if (query.strip() == "" or (query.lower() not in protocols and "==" not in query)):
			for i in range (0, len(self.packetList)):
				self.packetTable.setRowHidden(i, False)
		elif "==" not in query:
			for i in range (0, len(self.packetList)):
				self.packetTable.setRowHidden(i, False)
			if (query.lower() in protocols):
				for i in range(0, len(self.packetList)):
					dictPacket = getPacketInfoDict(self.packetList[i])
					if (dictPacket['proto'].lower() != query.lower()):
						self.packetTable.setRowHidden(i, True)
		else:
			for i in range (0, len(self.packetList)):
				self.packetTable.setRowHidden(i, False)
			column, value = query.split('==')
			column = column.strip()
			value = value.strip()
			if (column.lower() == "ip.addr"):
				for i in range(0, len(self.packetList)):
					dictPacket = getPacketInfoDict(self.packetList[i])
					try:
						if (dictPacket['IPsrc'].lower() != value.lower() and dictPacket['IPdst'] != value.lower()):
							self.packetTable.setRowHidden(i, True)
					except(AttributeError):
						self.packetTable.setRowHidden(i, True)

	def addPacketToList(self, packetDict, originalPacket):
		self.packetTable.setRowCount(self.packetTable.rowCount() + 1)
		time = QtWidgets.QTableWidgetItem()
		src = QtWidgets.QTableWidgetItem()
		dst = QtWidgets.QTableWidgetItem()
		protocol = QtWidgets.QTableWidgetItem()
		length = QtWidgets.QTableWidgetItem()
		info = QtWidgets.QTableWidgetItem()

		# Set flags for each Widget
		time.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		src.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		dst.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		length.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		protocol.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
		info.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)

		time.setText(originalPacket.sprintf("%.time%"))
		protocol.setText( packetDict["proto"])
		length.setText(packetDict['len'])
		try:
			if (packetDict["proto"] == "UDP" or packetDict["proto"] == "TCP"):
				src.setText( packetDict["IPsrc"])
				dst.setText( packetDict["IPdst"])
				length.setText( str(packetDict["len"]))
				info.setText( packetDict["srcPort"] + " -> " + packetDict["dstPort"])
			elif (packetDict['proto'] == 'ARP'):
				src.setText( packetDict["srcMac"])
				dst.setText( packetDict["dstMac"])
				info.setText(packetDict["info"])
			elif (packetDict['proto'] == 'ICMP'):
				src.setText(packetDict['IPsrc'])
				dst.setText(packetDict['IPdst'])
			else:
				if ('IPsrc' in packetDict):
					src.setText(packetDict['IPsrc'])
					dst.setText(packetDict['IPdst'])
				else:
					src.setText(packetDict['srcMac'])
					dst.setText(packetDict['dstMac'])
		except(KeyError):
			print("Problem with Packet:")
			print(originalPacket.show())

		self.packetTable.setItem(self.countPacket, 0, time)
		self.packetTable.setItem(self.countPacket, 1, src)
		self.packetTable.setItem(self.countPacket, 2, dst)
		self.packetTable.setItem(self.countPacket, 3, protocol)
		self.packetTable.setItem(self.countPacket, 4, length)
		self.packetTable.setItem(self.countPacket, 5, info)
		for i in range(self.packetTable.rowCount() + 2):
			self.packetTable.setRowHeight(i, 20)

		self.packetList.append(originalPacket)
		#print (len(self.packetList)) # add packet to packet list
		self.countPacket += 1 # increment packet count
