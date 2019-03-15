# pyuic5 MinDataUi.ui -o MinDataUiBase.py
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from MinDataUiBase import Ui_dialog
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QDate
import time
from MinData import StockMinuteData
from datetime import datetime, date, timedelta
import threading
class MinDataUi_Dialog(Ui_dialog):#QtWidgets.QWidget
    def setupUi(self,Dialog):
        Dialog.setObjectName("分时数据提取")
        self.Main =StockMinuteData(uiDlg=self)
        super().setupUi(Dialog)
        self.dqljwj.clicked.connect(self.on_dqljwj_click)#self.myButton.clicked.connect(self.msg)  
        self.dqljwj_2.clicked.connect(self.on_dqljwj_2_click)
        self.listView.clicked.connect(self.on_listview_click)
        self.ljxz.clicked.connect(self.on_ljxz_click)
        #
        now_time = datetime.now()#现在
        end = now_time.strftime("%Y-%m-%d")
        yesterday =now_time +timedelta(days = -1) 
        start =yesterday.strftime('%Y-%m-%d')
        self.dateEdit.setDate(QDate.fromString(start, 'yyyy-MM-dd'))#start time
        self.dateEdit_2.setDate(QDate.fromString(end, 'yyyy-MM-dd'))#end time
        # 
        self.xzlsFs.clicked.connect(self.on_xzlsFs_click)
        # 
        # self.listView_2 = QtWidgets.QListView(self.groupBox)
        #实例化列表模型，添加数据
        self.qsL=QStringListModel()
        self.Test=[]

        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)

        #设置列表视图的模型
        self.listView_2.setModel(self.qsL)
        self.progressBar.setValue(0)

    
    def on_xzlsFs_click(self):
        startDay =self.dateEdit.dateTime()
        start =startDay.toString('yyyy-MM-dd')
        endDay = self.dateEdit_2.dateTime()
        end =endDay.toString('yyyy-MM-dd')
        code =self.gpdmEdit.text()
        if(len(code)==8):
            t = threading.Thread(target=getDataWithDay, args=(code,start,end,self), name='funciton')
            t.start()

            # self.getDataWithDay(code,start,end)
        


    def on_listview_click(self,qModelIndex):
        txtN =self.strlist[qModelIndex.row()]
        txtN =txtN[0:8]
        self.gpdmHb.setText(txtN)

    def on_ljxz_click(self):
        self.savePath = QtWidgets.QFileDialog.getExistingDirectory(self,  
                            "浏览",  
                            ".\\")
        self.Main.destPath =self.savePath+'/'
        self.bclj_2.setText(self.Main.destPath)



    def on_dqljwj_click(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self,  
                            "浏览",  
                            ".\\")
        self.dqlj.setText(download_path)


    def on_dqljwj_2_click(self):
        path =self.dqlj.text()
        files = os.listdir(path)
        self.strlist=[]
        for fi in files:
            fi_d = os.path.join(path,fi) 
            if os.path.isdir(fi_d):
                continue
            else:
                fi_d =fi_d.replace(path+'\\','')
                self.strlist.append(fi_d)
        #实例化列表模型，添加数据
        slm=QStringListModel()
        
        

        #设置模型列表视图，加载数据列表
        slm.setStringList(self.strlist)

        #设置列表视图的模型
        self.listView.setModel(slm)

 
    def addListViewMessage(self,msg):
        # self.item_1=QStandardItem(QIcon("./image/save.ico"), "普通员工A");
        #  self.item_2 = QStandardItem(QIcon("./image/save.ico"), "普通员工B");
 
        #  model=QStandardItemModel()
        #  model.appendRow(self.item_1)
        #  model.appendRow(self.item_2)
        #  listView.setModel(model)
        self.Test.append(msg)
        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)
        
        pass
    def setProcessBarPos(self,processBar):
        self.progressBar.setValue(processBar)
def getDataWithDay(code,start,end,uiL):
    startDay =datetime.strptime(start,"%Y-%m-%d")
    endDay =datetime.strptime(end,"%Y-%m-%d")
    dayDelay = endDay -startDay
    k=0
    readDay =startDay
    while(k<=dayDelay.days):
        day =readDay.strftime('%Y-%m-%d')
        readDay =readDay + timedelta(days=1)
        uiL.Main.getStockLoopHistory(code,day)
        k =k+1 
    # def start_login(self):
    #     # 创建线程
    #     self.thread = Runthread()
    #     # 连接信号
    #     self.thread._signal.connect(self.callbacklog)
    #     # 开始线程
    #     self.thread.start()

    # def callbacklog(self, msg):
    #     # 奖回调数据输出到文本框
    #     self.textEdit_log.setText(self.textEdit_log.toPlainText()+ "\n"+ msg+ "   "+
    #                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()));

# class Runthread(QtCore.QThread):
#     # python3,pyqt5与之前的版本有些不一样
#     #  通过类成员对象定义信号对象
#     _signal = pyqtSignal(str)

#     def __init__(self, parent=None):
#         super(Runthread, self).__init__()

#     def __del__(self):
#         self.wait()

#     def run(self):
#         # 处理你要做的业务逻辑，这里是通过一个回调来处理数据，这里的逻辑处理写自己的方法
#         # wechat.start_auto(self.callback)
#         # self._signal.emit(msg);  可以在这里写信号焕发

#     def callback(self, msg):
#         # 信号焕发，我是通过我封装类的回调来发起的
#         # self._signal.emit(msg);

        
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MinDataUi_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
