# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TdxAudTool.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(QtWidgets.QWidget):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1205, 688)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(1040, 660, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1191, 651))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_data = QtWidgets.QWidget()
        self.tab_data.setObjectName("tab_data")
        self.groupBox = QtWidgets.QGroupBox(self.tab_data)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 831, 291))
        self.groupBox.setObjectName("groupBox")
        self.tv_lhb = QtWidgets.QTableView(self.groupBox)
        self.tv_lhb.setGeometry(QtCore.QRect(10, 51, 811, 231))
        self.tv_lhb.setObjectName("tv_lhb")
        self.rb_5day = QtWidgets.QRadioButton(self.groupBox)
        self.rb_5day.setGeometry(QtCore.QRect(10, 20, 41, 16))
        self.rb_5day.setObjectName("rb_5day")
        self.rb_10day = QtWidgets.QRadioButton(self.groupBox)
        self.rb_10day.setGeometry(QtCore.QRect(60, 20, 47, 16))
        self.rb_10day.setObjectName("rb_10day")
        self.rb_30day = QtWidgets.QRadioButton(self.groupBox)
        self.rb_30day.setGeometry(QtCore.QRect(110, 20, 47, 16))
        self.rb_30day.setObjectName("rb_30day")
        self.rb_60day = QtWidgets.QRadioButton(self.groupBox)
        self.rb_60day.setGeometry(QtCore.QRect(160, 20, 47, 16))
        self.rb_60day.setObjectName("rb_60day")
        self.btn_lhb = QtWidgets.QPushButton(self.groupBox)
        self.btn_lhb.setGeometry(QtCore.QRect(220, 20, 75, 23))
        self.btn_lhb.setObjectName("btn_lhb")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_data)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 310, 831, 281))
        self.groupBox_2.setObjectName("groupBox_2")
        self.rb_lhb = QtWidgets.QRadioButton(self.groupBox_2)
        self.rb_lhb.setGeometry(QtCore.QRect(20, 50, 89, 16))
        self.rb_lhb.setObjectName("rb_lhb")
        self.rb_all = QtWidgets.QRadioButton(self.groupBox_2)
        self.rb_all.setGeometry(QtCore.QRect(120, 50, 111, 16))
        self.rb_all.setObjectName("rb_all")
        self.btn_read_stock = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_read_stock.setGeometry(QtCore.QRect(380, 50, 251, 23))
        self.btn_read_stock.setObjectName("btn_read_stock")
        self.lv_msg = QtWidgets.QListView(self.groupBox_2)
        self.lv_msg.setGeometry(QtCore.QRect(10, 80, 811, 192))
        self.lv_msg.setObjectName("lv_msg")
        self.le_tdx_path = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_tdx_path.setGeometry(QtCore.QRect(110, 20, 141, 20))
        self.le_tdx_path.setObjectName("le_tdx_path")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(20, 20, 91, 16))
        self.label.setObjectName("label")
        self.btn_tdx_path = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_tdx_path.setGeometry(QtCore.QRect(260, 20, 75, 23))
        self.btn_tdx_path.setObjectName("btn_tdx_path")
        self.le_read_path = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_read_path.setGeometry(QtCore.QRect(460, 20, 171, 20))
        self.le_read_path.setObjectName("le_read_path")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(380, 20, 81, 16))
        self.label_2.setObjectName("label_2")
        self.btn_clearMsg = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_clearMsg.setGeometry(QtCore.QRect(730, 50, 75, 23))
        self.btn_clearMsg.setObjectName("btn_clearMsg")
        self.rb_set_stock = QtWidgets.QRadioButton(self.groupBox_2)
        self.rb_set_stock.setGeometry(QtCore.QRect(240, 50, 111, 16))
        self.rb_set_stock.setObjectName("rb_set_stock")
        self.progressBar = QtWidgets.QProgressBar(self.tab_data)
        self.progressBar.setGeometry(QtCore.QRect(340, 600, 261, 21))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.le_outpath = QtWidgets.QLineEdit(self.tab_data)
        self.le_outpath.setGeometry(QtCore.QRect(100, 600, 231, 20))
        self.le_outpath.setObjectName("le_outpath")
        self.label_3 = QtWidgets.QLabel(self.tab_data)
        self.label_3.setGeometry(QtCore.QRect(20, 600, 81, 16))
        self.label_3.setObjectName("label_3")
        self.tabWidget.addTab(self.tab_data, "")
        self.tab_view = QtWidgets.QWidget()
        self.tab_view.setObjectName("tab_view")
        self.groupBox_pic = QtWidgets.QGroupBox(self.tab_view)
        self.groupBox_pic.setGeometry(QtCore.QRect(210, 10, 1041, 561))
        self.groupBox_pic.setObjectName("groupBox_pic")
        self.tabWidget.addTab(self.tab_view, "")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "龙虎榜"))
        self.rb_5day.setText(_translate("Dialog", "5日"))
        self.rb_10day.setText(_translate("Dialog", "10日"))
        self.rb_30day.setText(_translate("Dialog", "30日"))
        self.rb_60day.setText(_translate("Dialog", "60日"))
        self.btn_lhb.setText(_translate("Dialog", "获取龙虎榜"))
        self.groupBox_2.setTitle(_translate("Dialog", "获取通达信数据"))
        self.rb_lhb.setText(_translate("Dialog", "路径龙虎榜股票"))
        self.rb_all.setText(_translate("Dialog", "路径下所有股票"))
        self.btn_read_stock.setText(_translate("Dialog", "从通达信读取股票数据"))
        self.label.setText(_translate("Dialog", "通达信安装路径"))
        self.btn_tdx_path.setText(_translate("Dialog", "查找"))
        self.label_2.setText(_translate("Dialog", "数据读取路径"))
        self.btn_clearMsg.setText(_translate("Dialog", "清除信息"))
        self.rb_set_stock.setText(_translate("Dialog", "路径下指定股票"))
        self.label_3.setText(_translate("Dialog", "数据输出路径"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_data), _translate("Dialog", "提取数据"))
        self.groupBox_pic.setTitle(_translate("Dialog", "绘图区"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_view), _translate("Dialog", "查看图形"))
