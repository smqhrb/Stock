# pyuic5 MinDataUi.ui -o MinDataUiBase.py
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from UI_UseWeChatBase import Ui_Dialog
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import QDate
import time
from useWeChat import WxSms
from datetime import datetime, date, timedelta
import threading
import json
from PyQt5.QtWidgets import QMessageBox
class ReDialog(QtWidgets.QDialog):
    """对QDialog类重写，实现一些功能"""
    
    
    def showEvent(self, event):
        self.cfg_fname ="cfg.json"
        self.cfg_dict ={}
        print("窗口显示") 

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               '本程序',
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
            self.SaveCfg(self.cfg_fname)
        else:
            event.ignore()

    def SaveCfg(self,cfg_fname):
        with open(cfg_fname,'w',encoding='utf-8') as f:
            json.dump(self.cfg_dict,f)
            print("配置文件完成更新...")

    def LoadCfg(self,cfg_fname):
        try:
            with open(cfg_fname,'r',encoding='utf-8') as file:
                self.cfg_dict = json.load(file)
                #<class 'dict'>,JSON文件读入到内存以后，就是一个Python中的字典。
                # 字典是支持嵌套的，
                print(self.cfg_dict)
        except Exception as ex:
            print("load fail...")
 

       
class UI_UserWeChatUser(Ui_Dialog):#QtWidgets.QWidget
    def setupUi(self,Dialog):
        self.cfg_fname ="cfg.json"
        super().setupUi(Dialog)
        Dialog.setObjectName("dlg")
        
        self.dlg =Dialog
        self.dlg.LoadCfg(self.cfg_fname)
        self.tE_From.setDisplayFormat("hh:mm:ss")
        self.tE_End.setDisplayFormat("hh:mm:ss")
        if(len(self.dlg.cfg_dict)>0):
            timeStart =self.dlg.cfg_dict['time_start']
            # start_time = time.strftime("%H:%M:%S",timeStart)
            self.tE_From.setTime(QtCore.QTime.fromString(timeStart, 'hh:mm:ss'))
            timeEnd =self.dlg.cfg_dict['time_end']
            # end_time = time.strftime("%H:%M:%S",timeEnd)
            self.tE_End.setTime(QtCore.QTime.fromString(timeEnd, 'hh:mm:ss'))
            timeSpan =self.dlg.cfg_dict['time_span']
            self.le_minspan.setText(timeSpan)

    # #创建一个时间框
    # self.time = QtWidgets.QTimeEdit(w)
    # self.time.setGeometry(QtCore.QRect(150,65,160,30))
    # self.time.setDisplayFormat("hh:mm:ss")
    # #获取并定义当前时间
    # now_time = time.strftime("%H:%M:%S",time.localtime())
    # self.time.setTime(QtCore.QTime.fromString(now_time, 'hh:mm:ss'))

        self.pBtn_Start.clicked.connect(self.on_start_click)#查询
        self.pBtn_Stop.clicked.connect(self.on_stop_click)#查询
        self.cB_DbExport.clicked.connect(self.db_export_click)
        self.cB_DbExport.stateChanged.connect(lambda: self.btnstate_dbExport(self.cB_DbExport))
        self.cB_ipCheck.clicked.connect(self.db_ipcheck_click)
        self.cB_ipCheck.stateChanged.connect(lambda: self.btnstate_ipCheck(self.cB_ipCheck))
        self.pBtn_Save.clicked.connect(self.on_save_click)
        # 
        
        #实例化列表模型，添加数据
        self.qsL=QStringListModel()
        self.Test=[]

        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)

        #设置列表视图的模型
        self.listView.setModel(self.qsL)

        #实例化列表模型，添加数据
        self.qsL_ip=QStringListModel()
        self.Test_ip=[]

        #设置模型列表视图，加载数据列表
        self.qsL_ip.setStringList(self.Test_ip)

        #设置列表视图的模型
        self.listView_Ip.setModel(self.qsL_ip)
        #
        self.savePath =None
        self.Main =WxSms()
        self.Main.signal.connect(self.callbacklog)
        self.th1 =None#合并xls
        self.th_excel =None#合并xls
    # def resolveJson(path):
    #     file = open(path, "rb")
    #     fileJson = json.load(file)
    #     field = fileJson["field"]
    #     futures = fileJson["futures"]
    #     type = fileJson["type"]
    #     name = fileJson["name"]
    #     time = fileJson["time"]

    # return (field, futures, type, name, time)
    def on_save_click(self):
        timeStart =self.tE_From.time().toString()
        timeEnd =self.tE_End.time().toString()
        timeSpan =self.le_minspan.text()
        self.dlg.cfg_dict['time_start'] =timeStart
        self.dlg.cfg_dict['time_end'] =timeEnd
        self.dlg.cfg_dict['time_span'] =timeSpan   
        self.dlg.SaveCfg(self.cfg_fname)    


    def on_start_click(self):
        # reply = QMessageBox.information(self,"标题",
        #                         "请打开文件stockList.txt,填加股票代码。股票代码例如：sz000651",
        #                         QMessageBox.Yes)
        timeStart =self.tE_From.time().toString()
        timeEnd =self.tE_End.time().toString()
        timeSpan =self.le_minspan.text()
        self.dlg.cfg_dict['time_start'] =timeStart
        self.dlg.cfg_dict['time_end'] =timeEnd
        self.dlg.cfg_dict['time_span'] =timeSpan

        self.cB_ipCheck.setChecked(True)
        self.cB_DbExport.setChecked(True)

        now_time = datetime.now()
        dayL =now_time.strftime('%Y-%m-%d')
        #
        if(self.th1 is None):
            self.th1 = threading.Thread(target=self.Main.sendLoop, args=(timeStart,timeEnd,timeSpan), name='sendMsg')
            self.th1.start()
        else:
            if(self.th1.is_alive() ==False):
                self.th1 = threading.Thread(target=self.Main.sendLoop, args=(timeStart,timeEnd,timeSpan), name='sendMsg')
                self.th1.start()   
        #
        if(self.th_excel is None):
            self.th_excel = threading.Thread(target=self.Main.exportDataFromDB, args=(timeStart,timeEnd,dayL), name='export')
            self.th_excel.start()
        else:
            if(self.th_excel.is_alive() ==False):
                self.th_excel = threading.Thread(target=self.Main.exportDataFromDB, args=(timeStart,timeEnd,dayL), name='export')
                self.th_excel.start()    
                  
    def on_stop_click(self):
        self.cB_ipCheck.setChecked(False)
        self.cB_DbExport.setChecked(False)
        if(self.th1 is None):
            pass
        else:
            if(self.th1.is_alive() ==True):
                self.Main.runCntl =0
                self.Main.EnableCheckIP =False
                
                # self.th1.stop() 
                # self.th1.terminate() 
                self.th1.join()

        if(self.th_excel is None):
            pass
        else:
            if(self.th_excel.is_alive() ==True):
                self.Main.EnableExport =False
                # self.th_excel.stop() 
                # self.th_excel.terminate() 
                self.th_excel.join()

    def db_export_click(self):
        self.Main.EnableExport =self.cB_DbExport.isChecked();  

    def db_ipcheck_click(self):
        self.Main.EnableCheckIP =self.cB_ipCheck.isChecked();   

    def btnstate_dbExport(self, btn):
        self.Main.EnableExport =self.cB_DbExport.isChecked();  
        print("cB_DbExport = "+ str(self.Main.EnableExport))
        if(self.Main.EnableExport):
            self.cB_DbExport.setText("运行")
        else:
            self.cB_DbExport.setText("停止")

    def btnstate_ipCheck(self, btn):

        self.Main.EnableCheckIP =self.cB_ipCheck.isChecked();  
        print("cB_ipCheck = "+ str(self.Main.EnableCheckIP))
        if(self.Main.EnableCheckIP):
            self.cB_ipCheck.setText("运行")
        else:
            self.cB_ipCheck.setText("停止")
    def callbacklog(self, lx,msg):
        # 奖回调数据输出到文本框
        listText =msg.replace('------','')
        now_time = datetime.now()
        dateL =now_time.strftime('%H:%M:%S')
        if(len(listText)>0):
            if(lx != "IP"):
                self.addListViewMessage("[%s]:%s"%(dateL,listText))
            else:
                self.addListViewIPMessage("[%s]:%s"%(dateL,listText))
            # write log file
    def addListViewIPMessage(self,msg):
        self.Test_ip.append(msg)
        #设置模型列表视图，加载数据列表
        self.qsL_ip.setStringList(self.Test_ip)
      

    def addListViewMessage(self,msg):
        self.Test.append(msg)
        #设置模型列表视图，加载数据列表
        self.qsL.setStringList(self.Test)
      
        pass
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # Dialog = QtWidgets.QDialog()
    Dialog =ReDialog()
    ui = UI_UserWeChatUser()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
