'''
#1.选股
#    公司估值法、趋势法和资金法
#2.统计套利
# 有别于无风险套利，统计套利是利用证券价格的历史统计规律进行套利，
# 是一种风险套利，其风险在于这种历史统计规律在未来一段时间内是否继续存在。
# 统计套利在方法上可以分为两类，一类是利用股票的收益率序列建模，
# 目标是在组合的β值等于零的前提下实现alpha 收益，我们称之为β中性策略；
# 另一类是利用股票的价格序列的协整关系建模，我们称之为协整策略

# 7·算法交易

# 算法交易又被称为自动交易、黑盒交易或者机器交易，它指的是通过使用计算机程序来发出交易指令。
# 在交易中，程序可以决定的范围包括交易时间的选择、交易的价格、甚至可以包括最后需要成交的证券数量。
# 根据各个算法交易中算法的主动程度不同，可以把不同算法交易分为被动型算法交易、主动型算法交易、综合型算法交易三大类。

# 8·资产配置
# 资产配置是指资产类别选择，投资组合中各类资产的适当配置以及对这些混合资产进行实时管理。
# 量化投资管理将传统投资组合理论与量化分析技术的结合，极大地丰富了资产配置的内涵，形成了现代资产配置理论的基本框架。
# 它突破了传统积极型投资和指数型投资的局限，将投资方法建立在对各种资产类股票公开数据的统计分析上，
# 通过比较不同资产类的统计特征，建立数学模型，进而确定组合资产的配置目标和分配比例。
'''
import jieba
# import xlwt
import xlrd, xlwt
from xlutils.copy import copy as xl_copy
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.covariance import GraphLassoCV
from sklearn.cluster import affinity_propagation
import matplotlib.pyplot as plt
from numpy.random import randn
# encoding=utf-8
class selectStock:
    def __init__(self,data):
        '''

        '''
        self.data =data
    def getClusterCenter(self):
        '''
        1.reduce dimense of data
        2.search the best center number
        3.by eye.
        '''
        pca = PCA(0.99, whiten=True)
        data = pca.fit_transform(self.data)
        n_components = np.arange(1, 100, 1)
        models = [GaussianMixture(n, covariance_type='full', random_state=0) for n in n_components]
        aics = [model.fit(data).aic(data) for model in models]
        plt.plot(n_components, aics);
        plt.show()
              
    def stockCluster(self,centers,data,selectStock):
        '''
        data like
                     600010  600011
                 0    1.7     2.1
                 1    2.3     3.1
        
        stockList like 600010 600011
        '''
        # gmm = GaussianMixture(centers, covariance_type='full', random_state=0)
        # result =gmm.fit(self.data)
        # print(result)
        # kmeans = KMeans(n_clusters=centers)
        # kmeans.fit(self.data)
        # y_kmeans = kmeans.predict(data)
        # return y_kmeans;
        # pass

        edge_model=GraphLassoCV()
        edge_model.fit(data)

        _,labels=affinity_propagation(edge_model.covariance_)
        n_labels=max(labels) 
        # 对这41只股票进行了聚类，labels里面是每只股票对应的类别标号
        print('Stock Clusters: {}'.format(n_labels+1)) # 10，即得到10个类别
        stockList =pd.read_excel("stockList.xls")
        sz50_df2=stockList.set_index('ts_code')
        # print(sz50_df2)
        for i in range(n_labels+1):
            # print('Cluster: {}----> stocks: {}'.format(i,','.join(np.array(selected_stocks)[labels==i]))) # 这个只有股票代码而不是股票名称
            # 下面打印出股票名称，便于观察
            stocks=np.array(selectStock)[labels==i].tolist()
            names=sz50_df2.loc[stocks,:].name.tolist()
            print('Cluster: {}----> stocks: {}'.format(i,','.join(names)))

    def selectByAccount(self):
        '''
        1.五力模型
        2.缴税金额 与企业业绩 比例
        3. 资产：货币资产,交易性金融资产,应收账款
            稳健型企业：
                货币资产>负债总额
                投资收益率>利息率
            中小企业：
                货币资金+应收账款+应收票据>负载总额
                经营活动现金流>负债总额

            投资性资产：长期股权投资+交易性金融资产
            经营性资产=总资产-长期股权投资-交易性金融资产

            理性资产结构：
                投资性资产<经营性资产
            
            预收账款越大，预付账款越少，核心竞争力越强。预收款》预付款。
                应收票据+应收账款+预收账款>应付票据+应付账款+预付账款
        4.利润表：
            营业收入：
                主营业务收入，投资收入，其他业务收入
            营业成本
            营业利润=营业收入 - 营业成本
            利润总额
            净利润
            每股收益
            分析：
                收入增长速度>成本增长速度
                公司收入增长 与 利润增长 的关系
            盈利能力：
                总利润/总资产
        5.现金流量表：
            经营活动：销售商品，提供劳务收到的现金比重越大越好>=主营收入（利润表）
            经营活动资金净流量 历史同期比较，增长率越高越好。>= 营业利润
                   经营活动资金净流量*(1.2~1.5)=经营现金净流量
            投资活动产生的现金净流量>=投资收益*30%
            对内投资=构建固定资产，无形资产和其他长期资产支付现金（看销售增长）
            对外投资=投资支付现金(越少越好)

            偿债能力：
                经营活动产生的现金净流量>负债总额(以年报为准)
                货币现金+应收账款>负债总额
        6.市净率: (股价/每股净资产)<1.5
        7.市盈率:(股价/每股收益)=总市值/企业净利润<15
        '''

    def StockValueAssess(self):
        '''
        股票内在价值计算:
            1.资本结构：
                货币资金+应收账款+应收票据>负债总额
                货币资金>负债总额
                投资收益率>利息率
                经营活动现金流>负债总额
                投资性资产(长期股权+交易性金融资产)<经营性资产(总资产-投资性资产)
                预收账款>>预付账款

                不良资产：
                    其他应收款 其他预付款 在建工程
            2.利润分析:
                收入增长速度>成本增长速度
                主营业务>>投资收入+其他业务收入
                盈利能力：
                    投资利润<营业利润
                营业利润/营业资产   投资收益/投资资产
                公司税务变化:
                    营业税及附加  所得税
            3.现金流量表：
                经营活动流入小计 销售收入  --销售应该占大部分
                经营活动净流量同期比
            4.盈利能力：
                ->现金流量表中的销售商品>利润表中的营业收入
                ->经营活动净现金流>营业利润
                ->投资活动产生现金净流量>投资收益*30%
                ->投资活动产生现金净额>负债总额
                ->货币现金+应收账款>负债总额
            5.估值:
                市净率=(市值/(现金+应收票据+投资性房地产))<1.5
                市盈率=(总市值/(企业净利润-投资收益))<15 ,高成长<25
                毛利润率=毛利润/总收入<30%(优秀企业)
        '''
        #read xls 
        zcfzb =pd.read_excel('002271.xls','资产负债表')
        zcfzb.set_index('报告日期', inplace=True)
        zcfzb['2017-12-31'] = zcfzb['2017-12-31'].str.replace(',','').astype(int)
        zcfzb =zcfzb.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        # zcfzb =zcfzb.replace([',','--'],['',np.nan])##
        # zcfzb['2017-12-31'] = zcfzb['2017-12-31'].str.replace(',','').astype(int)

        print(zcfzb)
        zcfzb =zcfzb.convert_objects(convert_numeric=True)
        # lrb =pd.read_excel('002271.xls','利润表')
        # lrb.set_index('报告日期', inplace=True)
        # xjllb =pd.read_excel('002271.xls','现金流量表')
        # xjllb.set_index('报告日期', inplace=True)

        kk =zcfzb.loc['货币资金(万元)']
        print(kk)
        
        
        # self.addXlsSheet('002271.xls','result')
        # 货币资金+应收账款+应收票据>负债总额
        # fz =zcfzb.loc['货币资金(万元)']+zcfzb.loc['应收账款(万元)']+zcfzb.loc['应收票据(万元)'] -zcfzb.loc['负债合计(万元)']
        # df =pd.DataFrame(fz)

        # df.to_excel('002271.xls', sheet_name='result')

    def addXlsSheet(self,xlsfile,addSheet):
        # open existing workbook
        rb = xlrd.open_workbook(xlsfile, formatting_info=True)
        # make a copy of it
        wb = xl_copy(rb)
        # add sheet to workbook with existing sheets
        
        Sheet1 = wb.add_sheet(addSheet)
        wb.save(xlsfile)
                
if __name__ == '__main__':
    # seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    # print("Full Mode: " + "/ ".join(seg_list)) # 全模式

    # seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
    # print("Default Mode: " + "/ ".join(seg_list)) # 精确模式

    # seg_list = jieba.cut("他来到了网易杭研大厦") # 默认是精确模式
    # print(", ".join(seg_list))

    # seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") # 搜索引擎模式
    # print(", ".join(seg_list))


    # X, y_true = make_blobs(n_samples=80, centers=5,
    # cluster_std=0.60, random_state=0)
    # X = X[:, ::-1] # flip axes for better plotting

    # sS =selectStock(X)
    # sS.getClusterCenter()
    # # sS.stockCluster(20)

    # sS =selectStock(X)
    x=0
    test =selectStock(x)
    test.StockValueAssess()

