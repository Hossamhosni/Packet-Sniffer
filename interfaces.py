# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfaces.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InterfacesWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(368, 183)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(30, 20, 321, 121))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.interfacesList = QtWidgets.QComboBox(self.widget)
        self.interfacesList.setObjectName("interfacesList")
        self.horizontalLayout.addWidget(self.interfacesList)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 368, 21))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
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
        self.actionStart = QtWidgets.QAction(MainWindow)
        self.actionStart.setObjectName("actionStart")
        
        self.actionStop = QtWidgets.QAction(MainWindow)
        self.actionStop.setObjectName("actionStop")
        self.actionRestart = QtWidgets.QAction(MainWindow)
        self.actionRestart.setObjectName("actionRestart")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menufile.addAction(self.actionOpen_Packet)
        self.menufile.addAction(self.actionSave_Packet)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionQuit)
        self.menuCapture.addAction(self.actionStart)
        self.menuCapture.addAction(self.actionStop)
        self.menuCapture.addAction(self.actionRestart)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menuCapture.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Select the interface:"))
        self.menufile.setTitle(_translate("MainWindow", "File"))
        self.menuCapture.setTitle(_translate("MainWindow", "Capture"))
        self.actionOpen_Packet.setText(_translate("MainWindow", "Open Packet"))
        self.actionSave_Packet.setText(_translate("MainWindow", "Save Packet"))
        self.actionStart.setText(_translate("MainWindow", "Start"))
        self.actionStop.setText(_translate("MainWindow", "Stop"))
        self.actionRestart.setText(_translate("MainWindow", "Restart"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
