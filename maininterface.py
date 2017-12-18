# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from scapy.all import *
import threading

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(711, 586)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.filterLabel = QtWidgets.QLabel(self.centralwidget)
        self.filterLabel.setObjectName("filterLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.filterLabel)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.packetTable = QtWidgets.QTableWidget(self.centralwidget)
        self.packetTable.setRowCount(0)
        self.packetTable.setColumnCount(7)
        self.countPacket = 0
        self.packetList = []
        

        self.packetTable.setObjectName("packetTable")
        item = QtWidgets.QTableWidgetItem()
        self.packetTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.packetTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.packetTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.packetTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.packetTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.packetTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.packetTable.setHorizontalHeaderItem(6, item)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.packetTable)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.line_3)
        self.packetInfo = QtWidgets.QListView(self.centralwidget)
        self.packetInfo.setObjectName("packetInfo")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.packetInfo)
        self.hexView = QtWidgets.QListView(self.centralwidget)
        self.hexView.setObjectName("hexView")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.hexView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 711, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuCapture = QtWidgets.QMenu(self.menubar)
        self.menuCapture.setObjectName("menuCapture")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Packet = QtWidgets.QAction(MainWindow)
        self.actionOpen_Packet.setObjectName("actionOpen_Packet")
        self.actionSave_Packet = QtWidgets.QAction(MainWindow)
        self.actionSave_Packet.setObjectName("actionSave_Packet")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        self.actionRestart = QtWidgets.QAction(MainWindow)
        self.actionRestart.setObjectName("actionRestart")
        self.menuFile.addAction(self.actionOpen_Packet)
        self.menuFile.addAction(self.actionSave_Packet)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuCapture.addAction(self.actionStart)
        self.menuCapture.addAction(self.actionStop)
        self.menuCapture.addAction(self.actionRestart)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCapture.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.filterLabel.setText(_translate("MainWindow", "Choose a filter:"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "example: tcp"))
        item = self.packetTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "No."))
        item = self.packetTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Time"))
        item = self.packetTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Source"))
        item = self.packetTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Destination"))
        item = self.packetTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Protocol"))
        item = self.packetTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Length"))
        item = self.packetTable.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Info"))
        item = self.packetTable.horizontalHeaderItem(1)
        self.packetTable.setColumnWidth(0, 20)
        self.packetTable.horizontalHeader().setStretchLastSection(True)
        item = QtWidgets.QTableWidgetItem()
        item.setText(_translate("MainWindow", "Packet Name"))
        self.packetTable.setItem(1, 2, item)
        
        # Menu Actions
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuCapture.setTitle(_translate("MainWindow", "Capture"))
        self.actionOpen_Packet.setText(_translate("MainWindow", "Open Packet"))
        self.actionSave_Packet.setText(_translate("MainWindow", "Save Packet"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.actionRestart.setText(_translate("MainWindow", "Restart"))

        # Connect to functions
        self.actionSave_Packet.triggered.connect(self.savePacket)
        self.actionOpen_Packet.triggered.connect(self.openPacket)
        self.packetTable.itemClicked.connect(self.rowClicked)

    def rowClicked(self):
        # print(self.packetTable.currentRow())
        pass

    def savePacket(self):
        pass

    def openPacket(self):
        pass

    def addPacketToList(self, packetDict, originalPacket):
        _translate = QtCore.QCoreApplication.translate
        self.packetTable.setRowCount(self.packetTable.rowCount() + 1)
        for i in range(self.packetTable.rowCount() + 2):
            self.packetTable.setRowHeight(i, 20)
        
        time = QtWidgets.QTableWidgetItem()
        srcIP = QtWidgets.QTableWidgetItem()
        dstIP = QtWidgets.QTableWidgetItem()
        protocol = QtWidgets.QTableWidgetItem()
        length = QtWidgets.QTableWidgetItem()
        info = QtWidgets.QTableWidgetItem()

        time.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        srcIP.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        dstIP.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        length.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        protocol.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
        info.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)

        time.setText(_translate("MainWindow", originalPacket.sprintf("%.time%")))
        srcIP.setText(_translate("MainWindow", packetDict["srcIP"]))
        dstIP.setText(_translate("MainWindow", packetDict["dstIP"]))
        length.setText(_translate("MainWindow", str(packetDict["len"])))
        protocol.setText(_translate("MainWindow", packetDict["proto"]))
        info.setText(_translate("MainWindow", packetDict["srcPort"] + " -> " + packetDict["dstPort"]))

        self.packetTable.setItem(self.countPacket, 1, time)
        self.packetTable.setItem(self.countPacket, 2, srcIP)
        self.packetTable.setItem(self.countPacket, 3, dstIP)
        self.packetTable.setItem(self.countPacket, 4, protocol)
        self.packetTable.setItem(self.countPacket, 5, length)
        self.packetTable.setItem(self.countPacket, 6, info)


        self.packetList.append(originalPacket)
        self.countPacket += 1

