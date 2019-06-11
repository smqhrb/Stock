# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_UseWeChat.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(499, 568)
        self.pBtn_Start = QtWidgets.QPushButton(Dialog)
        self.pBtn_Start.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.pBtn_Start.setObjectName("pBtn_Start")
        self.pBtn_Stop = QtWidgets.QPushButton(Dialog)
        self.pBtn_Stop.setGeometry(QtCore.QRect(90, 10, 75, 23))
        self.pBtn_Stop.setObjectName("pBtn_Stop")
        self.listView = QtWidgets.QListView(Dialog)
        self.listView.setGeometry(QtCore.QRect(10, 40, 481, 521))
        self.listView.setObjectName("listView")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "UseWeChat"))
        self.pBtn_Start.setText(_translate("Dialog", "开始发送"))
        self.pBtn_Stop.setText(_translate("Dialog", "停止发送"))

