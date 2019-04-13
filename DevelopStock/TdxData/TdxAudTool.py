# pyuic5 MinDataUi.ui -o MinDataUiBase.py
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from TdxAudToolBase import Ui_Dialog
#from PyQt5.QtCore import QStringListModel
#from PyQt5.QtCore import QDate
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
import datetime
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from  Qt5WithMatplot import *
from datetime import datetime, date, timedelta
import threading
from PyQt5.QtWidgets import QMessageBox
from processTdxDay import *

from multiprocessing import Process,Queue
# str_msg =[]
str_msgQ = Queue()
class TdxAudTool_Dialog(Ui_Dialog):#QtWidgets.QWidget
    signal = pyqtSignal(str,int)
    def __init__(self):
        super(TdxAudTool_Dialog,self).__init__()
        super().setupUi(Dialog)
    def setupUi(self,Dialog):

        # super().setupUi(Dialog)
        Dialog.setObjectName("dlg")
        #QStandardItemModel model = new QStandardItemModel()
        # self.tv_lhb.setModel(model)
        # model.setColumnCount(2)
        # model.setHeaderData(0,Qt::Horizontal,"卡号")
        # model.setHeaderData(1,Qt::Horizontal,"姓名")
            #实例化列表模型，添加数据
        self.qsL=QStringListModel()
        self.Test=[]
        self.processInt =0
        self.setProcessBarPos(0)
        self.MAX_THREAD_NUM =5#最多并发数
        #设置模型列表视图，加载数据列表

        self.qsL.setStringList(self.Test)

        #设置列表视图的模型
        self.lv_msg.setModel(self.qsL)    
        self.signal.connect(self.callbacklog)
        self.th2 =None
        self.threadList =[]
        #设置数据层次结构，4行4列
        self.model=QStandardItemModel()

        self.btn_lhb.clicked.connect(self.on_btn_lhb_click)
        self.btn_tdx_path.clicked.connect(self.on_btn_tdx_path_click)
        self.btn_read_stock.clicked.connect(self.on_btn_read_stock_click)
        self.btn_clearMsg.clicked.connect(self.on_btn_clearMsg_click)
        self.btn_getValue.clicked.connect(self.on_btn_getValue_click)
        self.btn_drawPic.clicked.connect(self.on_btn_drawPic_click)
        # 
        now_time = datetime.datetime.now()#现在
        end = now_time.strftime("%Y-%m-%d")
        yesterday =now_time +timedelta(days = -1) 
        start =yesterday.strftime('%Y-%m-%d')
        self.dateEdit_Start.setDate(QDate.fromString(start, 'yyyy-MM-dd'))#start time
        self.dateEdit_End.setDate(QDate.fromString(end, 'yyyy-MM-dd'))#end time
        # 
        self.comboBox.addItem('日')
        self.comboBox.addItem('周')
        self.comboBox.addItem('月')
        self.comboBox.currentIndexChanged.connect(self.comb_selectionchange)
        # 

        self.timer=QTimer()
        self.timer.timeout.connect(self.currTime)
        self.timer.start(2000)

        # quit = QAction("Quit", self)
        # quit.triggered.connect(self.closeEvent)
        # menubar = self.menuBar()
        # fmenu = menubar.addMenu("File")
        # fmenu.addAction(quit)  
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject) 
        # self.closed.connect(self.accept)   
        #####draw pic
                #第五步：定义MyFigure类的一个实例
        self.Myfig = MyFigure(width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.Myfig, self)
        # self.Myfig.axesU = self.Myfig.fig.add_subplot(211)
        # self.Myfig.axesD = self.Myfig.fig.add_subplot(212)
        # F1 = MyFigure(width=5, height=4, dpi=100)
        # F1.fig.suptitle("Figuer_4")
        # F1.axes1 = F1.fig.add_subplot(221)
        
        #self.F.plotsin()
        
        #第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        self.gridlayout = QGridLayout(self.groupBox_pic)  # 继承容器groupBox
        self.gridlayout.addWidget(self.Myfig,0,1)

        self.gridlayout.addWidget(self.toolbar,1,1)

        # self.plotcos()
        # self.plotother()
        #####
        ##############
    
    def plotcos(self):
        # t = np.arange(0.0, 5.0, 0.01)
        # s = np.cos(2 * np.pi * t)
        # self.Myfig.axes0.plot(t, s)
        self.Myfig.fig.suptitle("cos")
        self.Myfig.plotcostest()
    # def plotother(self):
    #     F1 = MyFigure(width=5, height=4, dpi=100)
    #     F1.fig.suptitle("Figuer_4")
    #     F1.axes1 = F1.fig.add_subplot(221)
    #     x = np.arange(0, 50)
    #     y = np.random.rand(50)
    #     F1.axes1.hist(y, bins=50)
    #     F1.axes1.plot(x, y)
    #     F1.axes1.bar(x, y)
    #     F1.axes1.set_title("hist")
    #     F1.axes2 = F1.fig.add_subplot(222)

    #     ## 调用figure下面的add_subplot方法，类似于matplotlib.pyplot下面的subplot方法
    #     x = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    #     y = [23, 21, 32, 13, 3, 132, 13, 3, 1]
    #     F1.axes2.plot(x, y)
    #     F1.axes2.set_title("line")
    #     # 散点图
    #     F1.axes3 = F1.fig.add_subplot(223)
    #     F1.axes3.scatter(np.random.rand(20), np.random.rand(20))
    #     F1.axes3.set_title("scatter")
    #     # 折线图
    #     F1.axes4 = F1.fig.add_subplot(224)
    #     x = np.arange(0, 5, 0.1)
    #     F1.axes4.plot(x, np.sin(x), x, np.cos(x))
    #     F1.axes4.set_title("sincos")
    #     self.gridlayout.addWidget(F1, 0, 2)
    #     ##############
    def comb_selectionchange(self):
        print(self.comboBox.currentText())

    def on_btn_drawPic_click(self):
        codeU =self.lineEdit_CodeUp.text()
        codeD =self.lineEdit_CodeDn.text()
        self.Myfig.setCodeY(codeU,codeD)
        self.Myfig.drawAll(self.getSelect(),self.d0,self.d1)
    def on_btn_getValue_click(self):
        # self.plotcos()
        startDay =self.dateEdit_Start.dateTime()
        startTime =startDay.toString('yyyy-MM-dd')
        endDay = self.dateEdit_End.dateTime()
        endTime =endDay.toString('yyyy-MM-dd')
        curSel =self.comboBox.currentText()
        codeU =self.lineEdit_CodeUp.text()
        codeD =self.lineEdit_CodeDn.text()
        td =TdxData()

        if(curSel =="日"):
            tb_name='day_k'
        if(curSel =="周"):
            tb_name='week_k'
        if(curSel =="月"):
            tb_name='month_k'
        if(len(codeU)>0):
            sql ="select * from %s where code ='%s' and date between '%s' and '%s'  order by date asc"%(tb_name,codeU,startTime,endTime)
            data0 =td.mydb.read_sql_query(sql)
            data0.rename(columns={'date':'t'}, inplace = True)
        if(len(codeD)>0):
            sql ="select * from %s where code ='%s' and date between '%s' and '%s'  order by date asc"%(tb_name,codeD,startTime,endTime)
            data1 =td.mydb.read_sql_query(sql)
            data1.rename(columns={'date':'t'}, inplace = True)
        
        self.d0 =self.Myfig.prepare_data(data0)
        self.d1 =self.Myfig.prepare_data(data1)
        

    def getSelect(self):
            cb =[]
            cbv =[]
            kLine =self.cb_kLine.isChecked()
            cbv.append(kLine)
            cb.append('kLine')

            volume =self.cb_volume.isChecked()
            cbv.append(volume)
            cb.append('volume')

            macd =self.cb_MACD.isChecked()
            cbv.append(macd)
            cb.append('MACD')

            BOLL =self.cb_BOLL.isChecked()
            cbv.append(BOLL)
            cb.append('BOLL')
            
            nhd_20_31_60 =self.cb_nhd_20_31_60.isChecked()
            cbv.append(nhd_20_31_60)
            cb.append('Glue20_31_60')

            nhd31_60_120 =self.cb_nhd31_60_120.isChecked()
            cbv.append(nhd31_60_120)
            cb.append('Glue31_60_120')

            MA5 =self.cb_MA5.isChecked()
            cbv.append(MA5)
            cb.append('MA_5')

            MA10 =self.cb_MA10.isChecked()
            cbv.append(MA10)
            cb.append('MA_10')

            MA20 =self.cb_MA20.isChecked()
            cbv.append(MA20)
            cb.append('MA_20')

            MA31 =self.cb_MA31.isChecked()
            cbv.append(MA31)
            cb.append('MA_31')

            MA60 =self.cb_MA60.isChecked()
            cbv.append(MA60)
            cb.append('MA_60')

            MA120 =self.cb_MA120.isChecked()
            cbv.append(MA120)
            cb.append('MA_120')

            slopeMA5 =self.cb_slopeMA5.isChecked()
            cbv.append(slopeMA5)
            cb.append('Slope_M5')

            slopeMA10 =self.cb_slopeMA10.isChecked()
            cbv.append(slopeMA10)
            cb.append('Slope_M10')

            slopeMA20 =self.cb_slopeMA20.isChecked()
            cbv.append(slopeMA20)
            cb.append('Slope_M20')

            slopeMA31 =self.cb_slopeMA31.isChecked()
            cbv.append(slopeMA31)
            cb.append('Slope_M31')

            slopeMA60 =self.cb_slopeMA60.isChecked()
            cbv.append(slopeMA60)
            cb.append('Slope_M60')

            slopeMA120 =self.cb_slopeMA120.isChecked()
            cbv.append(slopeMA120)
            cb.append('Slope_M120')

            select =dict(zip(cb,cbv))
            return select
            ###
    def accept(self):
        print("accept")
        self.close()
    def reject(self):
        print("reject")
        self.close()

    def currTime(self):
        self.setProcessBarPos(self.processInt)     
        if(str_msgQ.qsize()>0):
            str_msg =str_msgQ.get()
            self.addListViewMessage(str_msg)
               


    # def closeEvent(self, QCloseEvent):#重写关闭窗口事件
    #     print("重写关闭窗口事件closeEvent")
    def closeEvent(self,event):
        reply =QMessageBox.question(self,"提示","后台还有进程运行，你确认退出么？",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if reply==QMessageBox.Yes:
            Dialog.accept()
        else:
            Dialog.ignore()

    def on_btn_clearMsg_click(self):
        self.Test.clear()
        # global str_msg
        self.qsL.setStringList(self.Test)

        pass

    def on_btn_tdx_path_click(self):
        '''
        判断线程是否在运行，如果运行不进行路径设置
        '''
        self.savePath = QtWidgets.QFileDialog.getExistingDirectory(self,  
                            "浏览",  
                            "./")
        if(len(self.savePath)>0):
            self.le_tdx_path.setText(self.savePath+'/')  
            self.le_read_path.setText(self.savePath+'/vipdoc/sz/lday')  

    def on_btn_read_stock_click(self):
        '''
        读取通达信/vipdoc/sz/lday目录下的日线数据
        '''
        if(self.th2 is None):
            self.addListViewMessage("线程启动")
            self.th2 = threading.Thread(target=self.processData, args=(), name='funciton')
            self.th2.setDaemon(True)
            self.th2.start()
        else:
            if(self.th2.is_alive()==False):
                self.addListViewMessage("线程启动")
                self.th2 = threading.Thread(target=self.processData, args=(), name='funciton')
                self.th2.setDaemon(True)
                self.th2.start()
            else:
                self.addListViewMessage("线程正在运行")
        #self.processData()


    def processData(self):
        source =self.le_read_path.text()
        
        file_list = os.listdir(source)
        td =""
        self.processInt =0
        if(self.rb_lhb.isChecked()):
            target ="./lhb" #数据存储目录
            self.le_outpath.setText(target)
            self.ifPathExist(target)
            if self.dataLhb is None:
                self.EmitMsgToUi('')
                return
            else:
                self.EmitMsgToUi("开始读取龙虎榜上的股票数据")
                self.walkThroughtLhb(td,source,target)#遍历龙虎榜数据
                self.EmitMsgToUi("结束读取龙虎榜上的股票数据")

        
        if(self.rb_all.isChecked()):
            global str_msgQ
            target="./lday"
            self.le_outpath.setText(target)
            self.ifPathExist(target)
            self.EmitMsgToUi("开始通信达目录%s下的所有股票数据"%source)
            total =len(file_list)
            i =0
            for f in file_list:
                i =i+1
                self.processInt =round(1.0 * i/ total * 100,2)
                # self.setProcessBarPos(self.processInt)
                target_prefix ="tdx_"
    ##########
                # th =threading.Thread(target=thread_day2csv_all, args=(td,source,tdxCode,target,target_prefix), name='funciton')
                th =Process(target=thread_day2csv_all, args=(str_msgQ,td,source,f,target,target_prefix))
                self.threadList.append(th)
                if((total -i)>=self.MAX_THREAD_NUM):
                    if(len(self.threadList)>=self.MAX_THREAD_NUM):
                        for x in self.threadList:
                            x.daemon=True
                            x.start()
                        x.join()
                        self.threadList.clear()
                else:
                    for x in self.threadList:
                        x.daemon=True
                        x.start()
                    x.join()
                    self.threadList.clear()        
    ##########
                # self.EmitMsgToUi("开始读取%s的数据"%f)
                # td.day2csv(source, f, target)  
            self.EmitMsgToUi("结束通信达目录%s下的所有股票数据"%source)      

        # if(self.rb_set_stock.isChecked()):
        #     df =lhb.getStockLHB(30)
    def EmitMsgToUi(self,msg):
        '''
        向界面发送信息
        '''
        self.signal.emit(msg,self.processInt)

    def walkThroughtLhb(self,td,source,target):
        global str_msgQ
        if (self.dataLhb is None):
            return 
        total =len(self.dataLhb)
        target_prefix ='lhb_'
        for i in range(0, total):
            self.processInt =round(1.0 * i/ total * 100,2)
            # self.setProcessBarPos(self.processInt)
            code = self.dataLhb.iloc[i]['code']
            if(code >='600000'):
                tdxCode ="sh%s.day"%code
            else:
                tdxCode ="sz%s.day"%code
            tfName =target + os.sep + target_prefix +tdxCode + '.xls'
            if(self.ifFileExist(tfName)==False):
                # if(td.day2csv(source, tdxCode, target,target_prefix)==True):
                #     self.EmitMsgToUi("成功读取龙虎榜上股票 %s/%s 的数据"%(source,tdxCode))
                # else:
                #     self.EmitMsgToUi("在通达信的目录中不存在 %s/%s 的数据"%(source,tdxCode))
                # th =threading.Thread(target=self.thread_day2csv_lhb, args=(td,source,tdxCode,target,target_prefix), name='funciton')
                th =Process(target=thread_day2csv_lhb, args=(str_msgQ,td,source,tdxCode,target,target_prefix))
                self.threadList.append(th)
                if((total -i)>=self.MAX_THREAD_NUM):
                    if(len(self.threadList)>=self.MAX_THREAD_NUM):
                        for x in self.threadList:
                            x.daemon=True
                            x.start()
                        x.join()
                        self.threadList.clear()
                else:
                    for x in self.threadList:
                        x.daemon=True
                        x.start()
                    x.join()
                    self.threadList.clear()                    
                        
            else:
                self.EmitMsgToUi("龙虎榜上股票 %s 的数据已经存在"%(tfName))

    # def thread_day2csv_all(self,td,source,fn,target,target_prefix):
    #     self.EmitMsgToUi("开始读取%s的数据"%f)
    #     td.day2csv(source, fn, target,target_prefix)  

    # def thread_day2csv_lhb(self,td,source,fn,target,target_prefix):
    #     if(td.day2csv(source, fn, target,target_prefix)==True):
    #         self.EmitMsgToUi("成功读取龙虎榜上股票 %s/%s 的数据"%(source,fn))
    #     else:
    #         self.EmitMsgToUi("在通达信的目录中不存在 %s/%s 的数据"%(source,fn))

    def ifPathExist(self,path):
        '''
        检测路径是否存在 如果存在跳过，如果不存在生成
        '''
        if(os.path.exists(path)==False):
            os.mkdir(path)
        else:
            pass

    def ifFileExist(self,fn):
        '''
        检测路径是否存在 如果存在跳过，如果不存在生成
        '''
        if(os.path.exists(fn)==False):
            return False
        else:
            return True         

    def on_btn_lhb_click(self):
        '''
        龙虎榜数据
        '''
        lhb =LHB_LT()
        dayType ="None"
        if(self.rb_5day.isChecked()):
            dayType ="5日"
            df =lhb.getStockLHB(5)
        if(self.rb_10day.isChecked()):
            dayType ="10日"
            df =lhb.getStockLHB(10)
        if(self.rb_30day.isChecked()):
            dayType ="30日"
            df =lhb.getStockLHB(30)
        if(self.rb_60day.isChecked()):
            dayType ="60日"
            df =lhb.getStockLHB(60)
        self.dataLhb =df

        self.model.setHorizontalHeaderLabels(['代码','名称','上榜次数','累积购买额(万)','累积卖出额(万)','净额(万)','买入席位数','卖出席位数'])
        row =0
        if (df is None):
            self.addListViewMessage("读取龙虎榜 %s 没有数据返回"%(dayType))
            return 
        for i in range(0, len(df)):
            # print df.iloc[i]['c1'], df.iloc[i]['c2']
            rowContent =df.iloc[i]
            item=QStandardItem(rowContent['code'])
            self.model.setItem(row,0,item)
            item=QStandardItem(rowContent['name'])
            self.model.setItem(row,1,item)
            item=QStandardItem(str(rowContent['count']))
            self.model.setItem(row,2,item)
            item=QStandardItem(str(rowContent['bamount']))
            self.model.setItem(row,3,item)
            item=QStandardItem(str(rowContent['samount']))
            self.model.setItem(row,4,item)
            item=QStandardItem(str(rowContent['net']))
            self.model.setItem(row,5,item)
            item=QStandardItem(str(rowContent['bcount']))
            self.model.setItem(row,6,item)
            item=QStandardItem(str(rowContent['scount']))
            self.model.setItem(row,7,item)
            row =row +1
        self.tv_lhb.setModel(self.model)                
        self.addListViewMessage("读取龙虎榜 %s 成功"%(dayType))
  
    def callbacklog(self, msg,processInt):
        '''
        # 回调数据输出到信息列表
        '''
        if(len(msg)>0):
            self.addListViewMessage(msg)
        self.setProcessBarPos(processInt)        

 
    def addListViewMessage(self,msg):
        '''
        向信息列表填加信息msg
        '''
        now_time = datetime.datetime.now()
        dateL =now_time.strftime('%H:%M:%S')
        global str_msg
        if(len(msg)>0):
            nMsg ="[%s]:%s"%(dateL,msg)
            self.Test.append(nMsg)
            #设置模型列表视图，加载数据列表
            self.qsL.setStringList(self.Test)
        
    def setProcessBarPos(self,processBar):
        '''
        设置进度条位置
        '''
        self.progressBar.setValue(processBar)

def thread_day2csv_lhb(q,td,source,fn,target,target_prefix):
    td =TdxData() 
    if(td.day2csv(source, fn, target,target_prefix)==True):
        q.put("成功读取龙虎榜上股票 %s/%s 的数据"%(source,fn))
        
    else:
        
        q.put("在通达信的目录中不存在 %s/%s 的数据"%(source,fn))
def thread_day2csv_all(q,td,source,fn,target,target_prefix):
    td =TdxData() 
    td.day2csv(source, fn, target,target_prefix) 
    q.put("成功读取%s的数据"%fn)

if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = TdxAudTool_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
