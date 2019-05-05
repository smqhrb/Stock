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
from PyQt5.QtWidgets import QMessageBox

class MinDataUi_Dialog(Ui_dialog):#QtWidgets.QWidget
    def setupUi(self,Dialog):

        super().setupUi(Dialog)
        Dialog.setObjectName("dlg")

        self.dqljwj_2.clicked.connect(self.on_dqljwj_2_click)#查询
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

        self.xzlsFs_2.clicked.connect(self.on_xzlsFs_2_click)
        self.xzdtfs.clicked.connect(self.on_xzdtfs_click)
        self.hbbb.clicked.connect(self.on_hbbb_click)
        self.xzlsFs_3.clicked.connect(self.on_xzlsFs_3_click)#提示打开股票代码文件 填加代码
        # 
        #实例化列表模型，添加数据
        self.qsL=QStringListModel()
        self.Test=[]

        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)

        #设置列表视图的模型
        self.listView_2.setModel(self.qsL)
        self.progressBar.setValue(0)
        self.progressBar_2.setValue(0)


        #
        self.savePath =None
        self.Main =StockMinuteData()
        if(self.savePath is None):
            self.savePath =self.Main.destPath
        self.bclj_2.setText(self.savePath)
        # self.dqlj.setText(self.savePath)
        self.Main.signal.connect(self.callbacklog)
        self.th1 =None#合并xls
        self.th2 =None#下载数据
        

    def on_xzlsFs_3_click(self):
        reply = QMessageBox.information(self,"标题",
                                "请打开文件stockList.txt,填加股票代码。股票代码例如：sz000651",
                                QMessageBox.Yes)
                
    def on_hbbb_click(self):
        code =self.gpdmHb.text()
        if(self.th1 is None):
            self.th1 = threading.Thread(target=self.Main.MergeMinData, args=(code,), name='hbbb')
            self.th1.start() 
        else:
            if(self.th1.is_alive() ==False):
                self.th1 = threading.Thread(target=self.Main.MergeMinData, args=(code,), name='hbbb')
                self.th1.start() 

           
    def on_xzdtfs_click(self):
        '''
        当天分时
        '''
        self.downData('1')


    def on_xzlsFs_2_click(self):
        '''
        多个股票下载历史分时
        '''
        self.downData('2')

    def downData(self,typeL):
        '''
        股票下载
        '''
        startDay =self.dateEdit.dateTime()
        startTime =startDay.toString('yyyy-MM-dd')
        endDay = self.dateEdit_2.dateTime()
        endTime =endDay.toString('yyyy-MM-dd')
       
        if(self.th2 is None):
            self.Main.setPara('',startTime,endTime,typeL,self.savePath,"stockList.txt")
            self.th2 = threading.Thread(target=self.Main.getDataWithTimeSpan, args=(startTime,endTime), name='funciton')
            self.th2.start()
        else:
            if(self.th2.is_alive()==False):
                self.Main.setPara('',startTime,endTime,typeL,self.savePath,"stockList.txt")
                self.th2 = threading.Thread(target=self.Main.getDataWithTimeSpan, args=(
                    startTime, endTime), name='funciton')
                self.th2.start()

    def callbacklog(self, msg,processInt,processHb):
        # 奖回调数据输出到文本框
        listText =msg.replace('------','')
        now_time = datetime.now()
        dateL =now_time.strftime('%H:%M:%S')
        if(len(listText)>0):
            self.addListViewMessage("[%s]:%s"%(dateL,listText))
        self.setProcessBarPos(processInt,processHb)        


    def on_listview_click(self,qModelIndex):
        txtN =self.strlist[qModelIndex.row()]
        txtN =txtN[0:8]
        self.gpdmHb.setText(txtN)

    def on_ljxz_click(self): 
        '''
        判断线程是否在运行，如果运行不进行路径设置
        '''
        fLag =True
        if(self.th2 is None):
            pass
        else:
            if(self.th2.is_alive()==True):
                fLag =False
        if(self.th1 is None):
            pass
        else:
            if(self.th1.is_alive()==True):
                fLag =False        
        if(fLag == False):
            return
        self.savePath = QtWidgets.QFileDialog.getExistingDirectory(self,  
                            "浏览",  
                            ".\\")
        if(len(self.savePath)>0):
            self.Main.destPath=self.savePath+'/'
            self.bclj_2.setText(self.Main.destPath)


    def on_dqljwj_2_click(self):
        '''
        查询指定文件路径下的文件合并
        '''
        path =self.bclj_2.text()
        files = os.listdir(path)
        self.strlist=[]
        for fi in files:
            fi_d = os.path.join(path,fi) 
            if os.path.isdir(fi_d):
                continue
            else:
                fi_d =fi_d.replace(path+'/','')
                if(fi_d.find('.xls')>0):
                    self.strlist.append(fi)
        #实例化列表模型，添加数据
        slm=QStringListModel()

        #设置模型列表视图，加载数据列表
        slm.setStringList(self.strlist)

        #设置列表视图的模型
        self.listView.setModel(slm)

 
    def addListViewMessage(self,msg):
        self.Test.append(msg)
        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)
        
        pass
    def setProcessBarPos(self,processBar,processHb):
        self.progressBar.setValue(processBar)
        self.progressBar_2.setValue(processHb)

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MinDataUi_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
