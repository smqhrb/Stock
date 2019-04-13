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
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes0 = self.fig.add_subplot(211)
        self.axes1 = self.fig.add_subplot(212,sharex=self.axes0)
        self.axes0.grid(True)
        self.axes1.grid(True)
        self.barWidth =0.4#bar width
        self.title_font=FontProperties(family='YouYuan',size=18) 
        self.xSplice =50
        self.title =""

    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】
    # def plotsin(self):
    #     self.axes0 = self.fig.add_subplot(111)
    #     t = np.arange(0.0, 3.0, 0.01)
    #     s = np.sin(2 * np.pi * t)
    #     self.axes0.plot(t, s)
    # def plotcos(self):
    #     t = np.arange(0.0, 3.0, 0.01)
    #     s = np.sin(2 * np.pi * t)
    #     self.axes.plot(t, s)
    def plotcostest(self):
        self.plotcos(self.axes0)
    def plotcos(self,ax):
        t = np.arange(0.0, 5.0, 0.01)
        s = np.cos(2 * np.pi * t)
        ax.plot(t, s)
        self.fig.suptitle("cos")
        # self.draw()
    def prepare_data(self,data):
        '''
        prepare data
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
        fig.subplots_adjust(bottom=0.1)
        # tmpData =self.data
        self.date_tickers =tmpData.t.values
        rdata=pd.DataFrame()
        rdata['t']=tmpData['t']# t, open, high, low, close 
        rdata['open']=tmpData['open']
        rdata['high']=tmpData['high']
        rdata['low']=tmpData['low']
        rdata['close']=tmpData['close']
   
        mpfData=[tuple([i]+list(quote[1:])) for i,quote in enumerate(rdata.values)] 

        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 

        mpf.candlestick_ohlc(ax,mpfData,colordown='#53c156', colorup='#ff1717',width=self.barWidth,alpha=1)
        # plt.grid(True)

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
        self.drawMacdRaw(ax,dif,dea,red_bar,green_bar,macdMax,macdMin,crossUp,crossDn)

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
        #note angle
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

        ax.legend((p_dif[0],p_dea[0]),[u'DIF',u'DEA']) 

        dist_max =(macdMax - macdMin)*0.05#set y axis offset
        for x,y in zip(crossUp,dif[crossUp]):#up cross flag
             ax.annotate(u"", xy = (x,y), xytext = (x,y+dist_max),
                        arrowprops = dict(facecolor = "r",ec='r',headwidth = 4,headlength = 4, width = 4,shrink =0.4))
        for x,y in zip(crossDn,dif[crossDn]):#down cross flag
            ax.annotate(u"", xy = (x,y), xytext = (x,y+dist_max),
                        arrowprops = dict(facecolor = "g",ec='g', headwidth = 4,headlength = 4,width = 4,shrink =0.4))

        # plt.grid(True)

    def drawColume(self,ax,colData):
        '''
        draw volume 
        '''
        # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y%m%d'))
        # colData =self.data
        self.date_tickers =colData.t.values

        red_bar=colData[colData['close']>=colData['open']] #red pillar
        green_bar=colData[colData['close']<colData['open']] #green pillar
        
        # ax.bar(colData.index,colData['volume'].values,width = self.barWidth,color='g',label="2nd")  # 直方图的画法
        ax.bar(red_bar.index,red_bar['volume'].values,width = self.barWidth,color='r',label="2nd",alpha=1.0,edgecolor='r')
        ax.bar(green_bar.index,green_bar['volume'].values,width = self.barWidth,color='g',label="2nd")
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 
        
        # plt.grid(True)

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
        ax.legend((p0[0],p1[0],p2[0]),[u'BOLL',u'UB',u'LB']) 
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 

    def drawCurveNormal(self,ax,data,colName):
        self.date_tickers =data.t.values
        # le =len(data) -1
        
        p1 =ax.plot(data.index,data[colName].values) 
        handles, labels = ax.get_legend_handles_labels()
        handles.append(p1[0])
        labels.append(colName)
        # ax.legend((p1[0],),[colName,])
        ax.legend(handles,labels)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 
 
    def drawAll(self,select,data0,data1):
        '''
        draw K-line,Volume,MACD in here
        select is dict
        '''
        # self.plotcos(self.axes0)
        # self.axes0 = self.fig.add_subplot(211)
        # self.axes1 = self.fig.add_subplot(212,self.axes0)
        if len(data0)>0:
            self.axes0.clear()
            self.axes0.set_title(self.title,fontsize=12,color='r')
            self.drawAxis(select,self.axes0,data0)
    
        if len(data1)>0:
            self.axes1.clear()
            self.axes0.set_title(self.title,fontsize=12,color='r')
            self.drawAxis(select,self.axes1,data1)
        self.axes0.grid(True)
        self.axes1.grid(True)
        plt.subplots_adjust(bottom=.12, top=.95, left=.10, right=.95,
                        wspace=0.1, hspace=0.04)

        self.draw()
        # pass
    def drawAxis(self,select,ax,data):
        if(select['kLine']):
            # self.plotcos(ax)
            self.drawKline(self.fig,ax,data)
        if(select['volume']):
            self.drawColume(ax,data)
        if(select['MACD']==1):
            self.drawMacd(ax,data)
        if(select['BOLL']==1):
            self.drawBOLL(ax,data)
        if(select['Glue20-31-60']==1): 
            self.date_tickers =data.t.values
            self.drawCurveNormal(ax,data,'Glue20_31_60')
        if(select['Glue31-60-120']==1): 
            self.date_tickers =data.t.values
            self.drawCurveNormal(ax,data,'Glue31_60_120')
        if(select['MA_5']==1): 
            
            self.drawCurveNormal(ax,data,'MA_5')
        if(select['MA_10']==1): 
            self.date_tickers =data.t.values
            self.drawCurveNormal(ax,data,'MA_10')
        if(select['MA_20']==1): 
            self.drawCurveNormal(ax,data,'MA_20')
        if(select['MA_31']==1): 
            self.drawCurveNormal(ax,data,'MA_31')
        if(select['MA_60']==1): 
            self.drawCurveNormal(ax,data,'MA_60')
        if(select['MA_120']==1): 
            self.drawCurveNormal(ax,data,'MA_120')
        if(select['Slope_M5']==1): 
            self.drawCurveNormal(ax,data,'Slope_M5')
        if(select['Slope_M10']==1): 
            self.drawCurveNormal(ax,data,'Slope_M10')        
        if(select['Slope_M20']==1): 
            self.drawCurveNormal(ax,data,'Slope_M20')
        if(select['Slope_M31']==1): 
            self.drawCurveNormal(ax,data,'Slope_M31')        
        if(select['Slope_M60']==1): 
            self.drawCurveNormal(ax,data,'Slope_M60')
        if(select['Slope_M120']==1): 
            self.drawCurveNormal(ax,data,'Slope_M120')        



    
