import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pandas import DataFrame

import matplotlib.dates as dates
import mpl_finance as mpf
import matplotlib as mpl 
from matplotlib.ticker import Formatter
from matplotlib.font_manager import FontProperties 
import matplotlib.dates as mdate
import matplotlib.ticker as ticker 
#创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，211表示子图编号
        self.axes0 = self.fig.add_subplot(211)#上图的
        self.axes1 = self.fig.add_subplot(212,sharex=self.axes0)#下图的
        self.axes0.grid(True)#设置网格显示
        self.axes1.grid(True)#设置网格显示
        self.barWidth =0.4#bar width
        self.title_font=FontProperties(family='YouYuan',size=18) 
        self.xSplice =50
        self.title =""
        self.handles=[]#legend显示
        self.labels=[]#legend显示

    def setCodeY(self,codeU,codeD):
        '''
        设置股票代码在图像上
        '''
        self.codeU =codeU
        self.codeD =codeD
        self.axes0.set_ylabel(codeU)
        self.axes1.set_ylabel(codeD)
    def prepare_data(self,data):
        '''
        为图形显示准备数据
        '''
        tmpT =data.t.values#交易日期
        data[data['volume']==0]=np.nan #将0 值清除
        data.dropna() #删除nan数据
        #
        data['t'] =tmpT
        data.sort_values(by='t',ascending=True,inplace=True) 
        # 注意，data.index 必须是升序 
        # 如果由于对 date 排序后，index变成了降序
        # 要单独把index的顺序反过来 
        # data.index=data.index[::-1] 
        data['t']=pd.to_datetime(data['t'], format = "%Y-%m-%d", errors = 'coerce')#将字符串日期变成datetime
        mpl.rcParams['axes.unicode_minus']=False
        return data

    def format_date(self,x,pos=None): 
        '''
        数轴上日期的显示格式
        '''
        if x<0 or x>len(self.date_tickers)-1: 
            return '' 
        tmp =self.date_tickers[int(x)]
        strTmp =(tmp.astype('M8[D]').astype('O')).strftime("%Y%m%d")

        return strTmp

    def drawKline(self,fig,ax,tmpData):
        '''
        draw K-line using mpf.candlestick_ohlc
        '''
        self.date_tickers =tmpData.t.values
        rdata=pd.DataFrame()
        rdata['t']=tmpData['t']# t, open, high, low, close 
        rdata['open']=tmpData['open']
        rdata['high']=tmpData['high']
        rdata['low']=tmpData['low']
        rdata['close']=tmpData['close']
        mpfData=[tuple([i]+list(quote[1:])) for i,quote in enumerate(rdata.values)] #将数据转换为list

        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 
        #绘制k线图
        mpf.candlestick_ohlc(ax,mpfData,colordown='#53c156', colorup='#ff1717',width=self.barWidth,alpha=1)

    def calcMacd(self,data,fast_period=12,slow_period=26,signal_period=9): 
        # data['close'] -- 收盘价 
        # 收盘价按照日期升序( data['date'] )排列 
        # 返回值都是 Series 
        fast_ewm=data['close'].ewm(span=fast_period).mean() 
        slow_ewm=data['close'].ewm(span=slow_period).mean() 
        dif=fast_ewm-slow_ewm 
        dea=dif.ewm(span=signal_period).mean() 
        # 一般概念里，macd柱是 (dif-dea)*2，实际上只是为了扩大显示效果 
        # # 实测后发现，也可以不乘以2，效果也足够清楚了 
        bar=(dif-dea)*2 
        # 将bar 分成红绿柱分别导出数据， 
        # #目的是后续用matplotlib绘图时，能够分色绘制 
        red_bar=bar[bar>=0] 
        green_bar=bar[bar<0] 
        return dif,dea,red_bar,green_bar

    def drawMacd(self,ax,data):
        '''
        画MACD图
        '''
        dif,dea,red_bar,green_bar=self.calcMacd(data) 
        macdMax =np.array([dif.max(), dea.max(), red_bar.max(), green_bar.max()]).max()
        macdMin =np.array([dif.min(), dea.min(), red_bar.min(), green_bar.min()]).min()
        crossUp,crossDn =self.getMacdCrossPoint(dif,dea)#calc dif dea cross pt
        p_dif,p_dea =self.drawMacdRaw(ax,dif,dea,red_bar,green_bar,macdMax,macdMin,crossUp,crossDn)
        return p_dif,p_dea

    def drawMacdRaw(self,ax, dif, dea, red_bar, green_bar, macdMax,macdMin,crossUp,crossDn,
                      canvas_w=1000, canvas_h=480, xtick_period=20): 
        '''
        •df_raw - 原始的从 csv 导出数据后生成的DataFrame，目的是用在生成major_xticks时定位使用
        •dif, dea, red_bar, green_bar 是使用 get_macd_data 方法计算出的MACD指标
        •canvas_w, canvas_h 为期望绘制出的图形宽度和高度，单位是像素
        •xtick_period 为生成x 方向刻度时，每间隔多少个数值，取一个值作为刻度显示出来——如果将全部日期显示出来，x方向的刻度将会是密密麻麻一片黑
        '''
        p_dif=ax.plot(dif.index,dif.values) 
        p_dea=ax.plot(dea.index,dea.values) 
        #draw MACD 
        ax.bar(red_bar.index, red_bar.values,width = self.barWidth ,color='#d62728',alpha=1.0,edgecolor='r' ) 
        ax.bar(green_bar.index, green_bar.values,width = self.barWidth ,color='#889966') 

        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 

        dist_max =(macdMax - macdMin)*0.05#set y axis offset
        for x,y in zip(crossUp,dif[crossUp]):#up cross flag
             ax.annotate(u"", xy = (x,y), xytext = (x,y+dist_max),
                        arrowprops = dict(facecolor = "r",ec='r',headwidth = 4,headlength = 4, width = 4,shrink =0.4))
        for x,y in zip(crossDn,dif[crossDn]):#down cross flag
            ax.annotate(u"", xy = (x,y), xytext = (x,y+dist_max),
                        arrowprops = dict(facecolor = "g",ec='g', headwidth = 4,headlength = 4,width = 4,shrink =0.4))
        return p_dif,p_dea

    def drawColume(self,ax,colData):
        '''
        draw volume 
        '''
        self.date_tickers =colData.t.values

        red_bar=colData[colData['close']>=colData['open']] #red pillar
        green_bar=colData[colData['close']<colData['open']] #green pillar
        ax.bar(red_bar.index,red_bar['volume'].values,width = self.barWidth,color='r',label="2nd",alpha=1.0,edgecolor='r')
        ax.bar(green_bar.index,green_bar['volume'].values,width = self.barWidth,color='g',label="2nd")
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 
        
    def getMacdCrossPoint(self,diff,dea):
        '''
        get the cross point,
        parameter:
            diff is diff
            dea is dea
        return : retU is diff up corss dea
                 retD is diff down cross dea
        '''
        crossPoint =diff - dea
        iCount = len(crossPoint)
        retU =[]
        retD =[]
        i=1
        while i<iCount:
            flag =crossPoint[i]*crossPoint[i-1]
            if flag<0:
                if crossPoint[i]>0:
                    retU.append(i)
                else:
                    retD.append(i)
            i=i+1
        return np.array(retU),np.array(retD)

    def drawBOLL(self,ax,data):
        '''
        '''
        self.date_tickers =data.t.values
        
        p0 =ax.plot(data.index,data.BOLL.values)
        p1 =ax.plot(data.index,data.UB.values)
        p2 =ax.plot(data.index,data.LB.values)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 
        return p0,p1,p2

    def drawCurveNormal(self,ax,data,colName):
        '''
        绘制曲线图
        '''
        self.date_tickers =data.t.values
        p1 =ax.plot(data.index,data[colName].values) 
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 
        return p1
 
    def drawAll(self,select,data0,data1):
        '''
        draw K-line,Volume,MACD in here
        select is dict
        '''
        if len(data0)>0:#绘制上图
            self.axes0.clear()
            self.axes0.set_ylabel(self.codeU)
            self.axes0.set_title(self.title,fontsize=12,color='r')
            self.drawAxis(select,self.axes0,data0)
    
        if len(data1)>0:#绘制下图
            self.axes1.clear()
            self.axes1.set_ylabel(self.codeD)
            self.axes0.set_title(self.title,fontsize=12,color='r')
            self.drawAxis(select,self.axes1,data1)
        self.axes0.grid(True)
        self.axes1.grid(True)
        self.fig.subplots_adjust(bottom=.05, top=.95, left=.05, right=.99,
                        wspace=0.01, hspace=0.04)#设置图像边界
        self.draw()
        # pass
    def drawAxis(self,select,ax,data):
        '''
        根据选择的不同，进行绘制
        '''
        self.handles.clear()
        self.labels.clear()
        if(select['kLine']):

            self.drawKline(self.fig,ax,data)
        if(select['volume']):
            self.drawColume(ax,data)
        if(select['MACD']==1):
            p_dif,p_dea =self.drawMacd(ax,data)
            self.handles.append(p_dif[0])
            self.labels.append('DIF')
            self.handles.append(p_dea[0])
            self.labels.append('DEA')

        if(select['BOLL']==1):
            p0,p1,p2 =self.drawBOLL(ax,data)
            self.handles.append(p0[0])
            self.labels.append('BOLL')      
            self.handles.append(p1[0])
            self.labels.append('UL')    
            self.handles.append(p2[0])
            self.labels.append('BL') 
        curveList =['Glue20_31_60','Glue31_60_120','MA_5','MA_10','MA_20','MA_31','MA_60','MA_120','Slope_M5','Slope_M10','Slope_M20','Slope_M31','Slope_M60','Slope_M120'] 
        curveLen =len(curveList)
        for  i in range(curveLen):
            if(select[curveList[i]]==True):
                self.date_tickers =data.t.values
                p1 =self.drawCurveNormal(ax,data,curveList[i])
                self.handles.append(p1[0])
                self.labels.append(curveList[i])  
        ax.legend(self.handles,self.labels)
     



    
