# pyuic5 MinDataUi.ui -o MinDataUiBase.py
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from MinDataUiBase import Ui_dialog
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QDate
import time
from useWeChat import WxSms
from datetime import datetime, date, timedelta
import threading
from PyQt5.QtWidgets import QMessageBox
class UI_UserWeChatUser(Ui_dialog):#QtWidgets.QWidget
    def setupUi(self,Dialog):

        super().setupUi(Dialog)
        Dialog.setObjectName("dlg")

        self.pBtn_Start.clicked.connect(self.on_start_click)#查询
        self.pBtn_Stop.clicked.connect(self.on_stop_click)#查询
 
        # 
        #实例化列表模型，添加数据
        self.qsL=QStringListModel()
        self.Test=[]

        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)

        #设置列表视图的模型
        self.listView.setModel(self.qsL)



        #
        self.savePath =None
        self.Main =WxSms()
        self.Main.signal.connect(self.callbacklog)
        self.th1 =None#合并xls

        

    def on_start_click(self):
        reply = QMessageBox.information(self,"标题",
                                "请打开文件stockList.txt,填加股票代码。股票代码例如：sz000651",
                                QMessageBox.Yes)
                
    def on_stop_click(self):
        code =self.gpdmHb.text()
        if(self.th1 is None):
            self.th1 = threading.Thread(target=self.Main.MergeMinData, args=(code,), name='hbbb')
            self.th1.start() 
        else:
            if(self.th1.is_alive() ==False):
                self.th1 = threading.Thread(target=self.Main.MergeMinData, args=(code,), name='hbbb')
                self.th1.start() 


    def callbacklog(self, msg,processInt,processHb):
        # 奖回调数据输出到文本框
        listText =msg.replace('------','')
        now_time = datetime.now()
        dateL =now_time.strftime('%H:%M:%S')
        if(len(listText)>0):
            self.addListViewMessage("[%s]:%s"%(dateL,listText))
        self.setProcessBarPos(processInt,processHb)        

    def addListViewMessage(self,msg):
        self.Test.append(msg)
        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)
      
        pass
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = UI_UserWeChatUser()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
