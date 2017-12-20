# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWidget(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(824, 592)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filterLabel = QtWidgets.QLabel(Form)
        self.filterLabel.setObjectName("filterLabel")
        self.horizontalLayout.addWidget(self.filterLabel)
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.filterButton = QtWidgets.QPushButton("Filter")
        self.horizontalLayout.addWidget(self.filterButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.packetTable = QtWidgets.QTableWidget(Form)
        self.packetTable.setRowCount(0)
        self.packetTable.setColumnCount(6)
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
        self.verticalLayout.addWidget(self.packetTable)
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.packetInfo = QtWidgets.QListView(Form)
        self.packetInfo.setObjectName("packetInfo")
        self.verticalLayout.addWidget(self.packetInfo)
        self.hexView = QtWidgets.QListWidget(Form)
        self.hexView.setObjectName("hexView")
        self.verticalLayout.addWidget(self.hexView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.filterLabel.setText(_translate("Form", "Choose a filter:"))
        self.lineEdit.setPlaceholderText(_translate("Form", "example: tcp, ip.addr == 192.168.1.1"))
        item = self.packetTable.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Time"))
        item = self.packetTable.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Source"))
        item = self.packetTable.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Destination"))
        item = self.packetTable.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Protocol"))
        item = self.packetTable.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Length"))
        item = self.packetTable.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Info"))
