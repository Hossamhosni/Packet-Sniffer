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
		#self.Quit()
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
		infoItem = QtWidgets.QTreeWidgetItem(self.packetInfo)
		infoItem.setText(0,self.packetList[rowNum].mysummary())
		#infoItem2 = QtWidgets.QTreeWidgetItem(self.packetInfo)
		#infoItem2.setText(0,"hello there!")
		#infoItem3 = QtWidgets.QTreeWidgetItem(self.packetInfo)
		#infoItem3.setText(0,"hello there!")
		#children
		childItem = QtWidgets.QTreeWidgetItem(infoItem)
		childItem.setText(0,self.packetList[rowNum].summary())
		#childItem2 = QtWidgets.QTreeWidgetItem(infoItem2)
		#childItem2.setText(0,"hello!!!")
		#childItem3 = QtWidgets.QTreeWidgetItem(infoItem3)
		#childItem3.setText(0,"hello!!!")
		
        #try
		#print(self.packetList[rowNum].mysummary())

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
						if (dictPacket['srcIP'].lower() != value.lower() and dictPacket['dstIP'] != value.lower()):
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
