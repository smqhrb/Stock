
# 二、RSI指标的计算方法
# 相对强弱指标RSI的计算公式有两种
# 其一：
# 假设A为N日内收盘价的正数之和，B为N日内收盘价的负数之和乘以（-1）,这样，A和B均为正，将A、B代入RSI计算公式，则
# RSI（N）=A÷（A＋B）×100

# 其二：
# RS（相对强度）=N日内收盘价涨数和之均值÷N日内收盘价跌数和之均值
# RSI（相对强弱指标）=100－100÷（1+RS）

# 这两个公式虽然有些不同，但计算的结果一样。

# 以14日RSI指标为例，从当起算，倒推包括当日在内的15个收盘价，以每一日的收盘价减去上一日的收盘价，得到14个数值，这些数值有正有负。这样，RSI指标的计算公式具体如下：

# A=14个数字中正数之和
# B=14个数字中负数之和乘以（-1）
# RSI（14）=A÷（A＋B）×100

# 式中：A为14日中股价向上波动的大小
# B为14日中股价向下波动的大小
# A＋B为股价总的波动大小

# RSI的计算公式实际上就是反映了某一阶段价格上涨所产生的波动占总的波动的百分比率，百分比越大，强势越明显；百分比越小，弱势越明显。RSI的取值介于0—100之间。在计算出某一日的RSI值以后，可采用平滑运算法计算以后的RSI值，根据RSI值在坐标图上连成的曲线，即为RSI线。
# 以日为计算周期为例，计算RSI值一般是以5日、10日、14日为一周期。另外也有以6日、12日、24日为计算周期。一般而言，若采用的周期的日数短，RSI指标反应可能比较敏感；日数较长，可能反应迟钝。目前，沪深股市中RSI所选用的基准周期为6日和12日。
# 和其他指标的计算一样，由于选用的计算周期的不同，RSI指标也包括日RSI指标、周RSI指标、月RSI指标年RSI指标以及分钟RSI指标等各种类型。经常被用于股市研判的是日RSI指标和周RSI指标。虽然它们的计算时的取值有所不同，但基本的计算方法一样。另外，随着股市软件分析技术的发展，投资者只需掌握RSI形成的基本原理和计算方法，无须去计算指标的数值，更为重要的是利用RSI指标去分析、研判股票行情。

import numpy as np

def RSI(array_list, periods=14):
    length = len(array_list)
    rsies = [np.nan] * length
     #数据长度不超过周期，无法计算；
    if length <= periods:
        return rsies
    #用于快速计算；
    up_avg = 0
    down_avg = 0
    #首先计算第一个RSI，用前periods+1个数据，构成periods个价差序列;
    first_t = array_list[:periods + 1]
    for i in range(1, len(first_t)):
        #价格上涨;
        if first_t[i] >= first_t[i - 1]:
            up_avg += first_t[i] - first_t[i - 1]
        #价格下跌;
        else:
            down_avg += first_t[i - 1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsies[periods] = 100 - 100 / (1 + rs)
    #后面的将使用快速计算；
    for j in range(periods + 1, length):
        up = 0
        down = 0
        if array_list[j] >= array_list[j - 1]:
            up = array_list[j] - array_list[j - 1]
            down = 0
        else:
            up = 0
            down = array_list[j - 1] - array_list[j]
         #类似移动平均的计算公式;
        up_avg = (up_avg * (periods - 1) + up) / periods
        down_avg = (down_avg * (periods - 1) + down) / periods
        rs = up_avg / down_avg
        rsies[j] = 100 - 100 / (1 + rs)
    return rsies
# ##############
def RSI(t, periods=10):
    length = len(t)
    rsies = [np.nan]*length
    #数据长度不超过周期，无法计算；
    if length <= periods:
        return rsies
    #用于快速计算；
    up_avg = 0
    down_avg = 0

    #首先计算第一个RSI，用前periods+1个数据，构成periods个价差序列;
    first_t = t[:periods+1]
    for i in range(1, len(first_t)):
        #价格上涨;
        if first_t[i] >= first_t[i-1]:
            up_avg += first_t[i] - first_t[i-1]
        #价格下跌;
        else:
            down_avg += first_t[i-1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsies[periods] = 100 - 100/(1+rs)

    #后面的将使用快速计算；
    for j in range(periods+1, length):
        up = 0
        down = 0
        if t[j] >= t[j-1]:
            up = t[j] - t[j-1]
            down = 0
        else:
            up = 0
            down = t[j-1] - t[j]
        #类似移动平均的计算公式;
        up_avg = (up_avg*(periods - 1) + up)/periods
        down_avg = (down_avg*(periods - 1) + down)/periods
        rs = up_avg/down_avg
        rsies[j] = 100 - 100/(1+rs)
    return rsies  


delta = df.Close.diff()
window = 15
up_days = delta.copy()
up_days[delta<=0]=0.0
down_days = abs(delta.copy())
down_days[delta>0]=0.0
RS_up = up_days.rolling(window).mean()
RS_down = down_days.rolling(window).mean()
rsi= 100-100/(1+RS_up/RS_down)