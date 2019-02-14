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
import xlwt
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.covariance import GraphLassoCV
from sklearn.cluster import affinity_propagation
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
        n_components = np.arange(1, 30, 1)
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

    sS =selectStock(X)

