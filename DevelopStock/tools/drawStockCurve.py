# 
import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import mpl_finance as mpf
import matplotlib as mpl 
from matplotlib.ticker import Formatter
from matplotlib.font_manager import FontProperties 
import matplotlib.dates as mdate
import matplotlib.ticker as ticker 

class stockCurve:
    def __init__(self,data):
        tmpT =data.t.values
        data[data['volume']==0]=np.nan 
        data.dropna() 
        data['t'] =tmpT
        data.sort_values(by='t',ascending=True,inplace=True) 
        # 注意，data.index 必须是升序 
        # 如果由于对 date 排序后，index变成了降序
        # 要单独把index的顺序反过来 
        data.index=data.index[::-1] 
        # data['t']=pd.to_datetime(data['t'],format="%Y%m%d")
        data['t']=pd.to_datetime(data['t'], format = "%Y%m%d", errors = 'coerce')
        # print(data.head(10))
        self.data =data
        self.title_font=FontProperties(family='YouYuan',size=18) 
        mpl.rcParams['axes.unicode_minus']=False
        self.xSplice =50
        self.barWidth =0.4
        self.crossUp =0
        self.crossDn =0

    def format_date(self,x,pos=None): 
        if x<0 or x>len(self.date_tickers)-1: 
            return '' 
        tmp =self.date_tickers[int(x)]
        strTmp =(tmp.astype('M8[D]').astype('O')).strftime("%Y%m%d")

        return strTmp

    def drawKline(self,fig,ax):
        fig.subplots_adjust(bottom=0.1)
        tmpData =self.data
        self.date_tickers =tmpData.t.values
        
        mpfData=[tuple([i]+list(quote[1:])) for i,quote in enumerate(tmpData.values)] 

        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 

        mpf.candlestick_ohlc(ax,mpfData,colordown='#53c156', colorup='#ff1717',width=self.barWidth,alpha=1)
        plt.grid(True)

    def drawMacd(self,ax, dif, dea, red_bar, green_bar, 
                      canvas_w=1000, canvas_h=480, xtick_period=20): 
        '''
        •df_raw - 原始的从 csv 导出数据后生成的DataFrame，目的是用在生成major_xticks时定位使用
        •dif, dea, red_bar, green_bar 是使用 get_macd_data 方法计算出的MACD指标
        •canvas_w, canvas_h 为期望绘制出的图形宽度和高度，单位是像素
        •xtick_period 为生成x 方向刻度时，每间隔多少个数值，取一个值作为刻度显示出来——如果将全部日期显示出来，x方向的刻度将会是密密麻麻一片黑
        '''
        p_dif=ax.plot(dif.index,dif.values) 
        p_dea=ax.plot(dea.index,dea.values) 
        ax.bar(red_bar.index, red_bar.values,width = self.barWidth ,color='#d62728',alpha=1.0,edgecolor='r' ) 
        ax.bar(green_bar.index, green_bar.values,width = self.barWidth ,color='#889966') 

        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

        ax.legend((p_dif[0],p_dea[0]),[u'DIF',u'DEA']) 

        dist_max =(self.macdMax - self.macdMin)*0.05
        for x,y in zip(self.crossUp,dif[self.crossUp]):
             ax.annotate(u"", xy = (x,y), xytext = (x,y+dist_max),
                        arrowprops = dict(facecolor = "r",ec='r',headwidth = 4,headlength = 4, width = 4,shrink =0.4))
        for x,y in zip(self.crossDn,dif[self.crossDn]):
            ax.annotate(u"", xy = (x,y), xytext = (x,y+dist_max),
                        arrowprops = dict(facecolor = "g",ec='g', headwidth = 4,headlength = 4,width = 4,shrink =0.4))

        plt.grid(True)
        

    def drawColume(self,ax):
        
        # ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y%m%d'))
        colData =self.data
        self.date_tickers =colData.t.values

        red_bar=colData[colData['close']>=colData['open']] 
        green_bar=colData[colData['close']<colData['open']] 

        # ax.bar(colData.index,colData['volume'].values,width = self.barWidth,color='g',label="2nd")  # 直方图的画法
        ax.bar(red_bar.index,red_bar['volume'].values,width = self.barWidth,color='r',label="2nd",alpha=1.0,edgecolor='r')
        ax.bar(green_bar.index,green_bar['volume'].values,width = self.barWidth,color='g',label="2nd")
        ax.xaxis.set_major_locator(ticker.MultipleLocator(self.xSplice)) 
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_date)) 
        plt.grid(True)
       
    def drawAll(self):

        dif,dea,red_bar,green_bar=self.calcMacd()
        self.macdMax =np.array([dif.max(), dea.max(), red_bar.max(), green_bar.max()]).max()
        self.macdMin =np.array([dif.min(), dea.min(), red_bar.min(), green_bar.min()]).min()
        self.crossUp,self.crossDn =self.getMacdCrossPoint(dif,dea)

        canvas_w =1024
        canvas_h =768
        dpi=72 
        figsize=canvas_w/dpi,canvas_h/dpi 
        
        fig = plt.figure(figsize=figsize)

        # ax0figsize =figsize[0]/2,figsize[1]/2
        ax0 = fig.add_subplot(311)
        
        # ax0.rcParams['figure.figsize']=(canvas_w,canvas_h/2)
        self.drawKline(fig,ax0)

        ax1 = fig.add_subplot(312,sharex=ax0)
        self.drawColume(ax1)

        ax2 = fig.add_subplot(313,sharex=ax0)
        
        self.drawMacd(ax2,dif=dif, dea=dea, 
                    red_bar=red_bar, green_bar=green_bar, xtick_period=25) 

        plt.subplots_adjust(bottom=.12, top=.95, left=.10, right=.95,
                        wspace=0.1, hspace=0.04)
        plt.show()
        pass

    def calcMacd(self,fast_period=12,slow_period=26,signal_period=9): 
        # data['close'] -- 收盘价 
        # 收盘价按照日期升序( data['date'] )排列 
        # 返回值都是 Series 
        fast_ewm=self.data['close'].ewm(span=fast_period).mean() 
        slow_ewm=self.data['close'].ewm(span=slow_period).mean() 
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

if __name__ == '__main__':
    zcfzb =pd.read_excel("000882.SZ.xls")
    # df_raw = zcfzb[['交易日期',  '开盘价','最高价','最低价','收盘价','成交量 （手）']]
    df_raw =pd.DataFrame()
    df_raw['t'] =zcfzb['交易日期']
    df_raw['open']=zcfzb['开盘价']
    df_raw['high']=zcfzb['最高价']
    df_raw['low']=zcfzb['最低价']
    df_raw['close']=zcfzb['收盘价']
    df_raw['volume']=zcfzb['成交量 （手）']
    # print(df_raw)
    test =stockCurve(df_raw)
    test.drawAll()



