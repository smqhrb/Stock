'''
特征选择主要有两个功能：
1.减少特征数量、降维，使模型泛化能力更强，减少过拟合
2.增强对特征和特征值之间的理解

为什么要特征工程？
简单的说，你给我的数据能不能直接放到模型里？显然不能，
第一，你的数据可能是假(异常值); 
第二，你的数据太脏了(各种噪声);
第三，你的数据可能不够，或者数据量不平衡(数据采样)；
第三，清洗完数据能直接用吗？显然不能！
     输入模型的数据要和模型输出有关系，没关系的那是噪声！(特征提取或处理)；
第四，特征之间属于亲戚关系，你们是一家,不能反映问题！(特征选择)。
那么怎么区分哪些算法可以调高多线程呢？其实很简单，我们可以看算法的官方文档，
如果它有n_jobs，那么您就有一个可以为高性能而线程化的算法。
'''
from sklearn.feature_selection import SelectKBest,chi2
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import GradientBoostingClassifier
#有别于降维算法(PCA, SVD)
# Pearson相关系数 Pearson Correlation
import numpy as np
from scipy.stats import pearsonr
import numpy as np
import pandas as pd
# from minepy import MINE#minepy包——基于最大信息的非参数估计
class FeatureSel:
    def __init__(self):
        self.data =0
    def pearsonMethode(self,x,y):
        '''
        Pearson Correlation速度快、易于计算，经常在拿到数据(经过清洗和特征提取之后的)之后第一时间就执行。
        Scipy的pearsonr方法能够同时计算相关系数和p-value，
        Pearson相关系数的一个明显缺陷是，作为特征排序机制，他只对线性关系敏感。如果关系是非线性的，
        即便两个变量具有一一对应的关系，Pearson相关性也可能会接近0。
        '''
        return pearsonr(x,y)#error?
    # def minepyMINE(self):
    # '''
    # 互信息和最大信息系数 Mutual information and maximal information coefficient (MIC)
    # '''
    #     m = MINE()
    #     x = np.random.uniform(-1, 1, 10000)#均匀分布
    #     m.compute_score(x, x**2)
    #     print (m.mic())
    def SelectKBestFor(self,x,y):

        '''
        卡方检验
        '''
        return SelectKBest(chi2, k=2).fit_transform(x,y)
        # return SelectKBest(chi2,k=2).fit_transform(x,y)
    '''
    互信息法 
    from sklearn.feature_selection import SelectKBest
    from minepy import MINE

    #由于MINE的设计不是函数式的，定义mic方法将其为函数式的，返回一个二元组，二元组的第2项设置成固定的P值0.5
    def mic(x, y):
        m = MINE()
        m.compute_score(x, y)
        return (m.mic(), 0.5)

    #选择K个最好的特征，返回特征选择后的数据
    SelectKBest(lambda X, Y: array(map(lambda x:mic(x, Y), X.T)).T, k=2).fit_transform(iris.data, iris.target)
    '''
    def rfe(self,x,y):
        '''
        Wrapper
        递归特征消除法
        递归消除特征法使用一个基模型来进行多轮训练，每轮训练后，消除若干权值系数的特征，
        再基于新的特征集进行下一轮训练
        #递归特征消除法，返回特征选择后的数据
        #参数estimator为基模型
        #参数n_features_to_select为选择的特征个数
        '''
        return RFE(estimator=LogisticRegression(), n_features_to_select=2).fit_transform(x, y)

    def SelectFromModelByL1L2(self,x,y):
        '''
        # #带L1惩罚项的逻辑回归作为基模型的特征选择
        # return SelectFromModel(LogisticRegression(penalty="l1", C=0.1)).fit_transform(x, y)
        #带L1和L2惩罚项的逻辑回归作为基模ret型的特征选择
        #参数threshold为权值系数之差的阈值
        '''
        return SelectFromModel(LR(threshold=0.5, C=0.1)).fit_transform(x, y)

    def SelectFromModelByGBDT(self,x,y):
        '''
        基于树模型的特征选择法
        树模型中GBDT也可用来作为基模型进行特征选择，使用feature_selection库的SelectFromModel类结合GBDT模型
        '''
        return SelectFromModel(GradientBoostingClassifier()).fit_transform(x, y)

class LR(LogisticRegression):
    def __init__(self, threshold=0.01, dual=False, tol=1e-4, C=1.0,
                 fit_intercept=True, intercept_scaling=1, class_weight=None,
                 random_state=None, solver='liblinear', max_iter=100,
                 multi_class='ovr', verbose=0, warm_start=False, n_jobs=1):

        #权值相近的阈值
        self.threshold = threshold
        LogisticRegression.__init__(self, penalty='l1', dual=dual, tol=tol, C=C,
                 fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, class_weight=class_weight,
                 random_state=random_state, solver=solver, max_iter=max_iter,
                 multi_class=multi_class, verbose=verbose, warm_start=warm_start, n_jobs=n_jobs)
        #使用同样的参数创建L2逻辑回归
        self.l2 = LogisticRegression(penalty='l2', dual=dual, tol=tol, C=C, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, class_weight = class_weight, random_state=random_state, solver=solver, max_iter=max_iter, multi_class=multi_class, verbose=verbose, warm_start=warm_start, n_jobs=n_jobs)

    def fit(self, X, y, sample_weight=None):
        #训练L1逻辑回归
        super(LR, self).fit(X, y, sample_weight=sample_weight)
        self.coef_old_ = self.coef_.copy()
        #训练L2逻辑回归
        self.l2.fit(X, y, sample_weight=sample_weight)

        cntOfRow, cntOfCol = self.coef_.shape
        #权值系数矩阵的行数对应目标值的种类数目
        for i in range(cntOfRow):
            for j in range(cntOfCol):
                coef = self.coef_[i][j]
                #L1逻辑回归的权值系数不为0
                if coef != 0:
                    idx = [j]
                    #对应在L2逻辑回归中的权值系数
                    coef1 = self.l2.coef_[i][j]
                    for k in range(cntOfCol):
                        coef2 = self.l2.coef_[i][k]
                        #在L2逻辑回归中，权值系数之差小于设定的阈值，且在L1中对应的权值为0
                        if abs(coef1-coef2) < self.threshold and j != k and self.coef_[i][k] == 0:
                            idx.append(k)
                    #计算这一类特征的权值系数均值
                    mean = coef / len(idx)
                    self.coef_[i][idx] = mean
        return self

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
class reduceDimense:
    '''
    当特征选择完成后，可以直接训练模型了，但是可能由于特征矩阵过大，导致计算量大，训练时间长的问题，
    因此降低特征矩阵维度也是必不可少的。
    常见的降维方法除了以上提到的基于L1惩罚项的模型以外，
    另外还有主成分分析法（PCA）和线性判别分析（LDA），
    线性判别分析本身也是一个分类模型。
    PCA和LDA有很多的相似点，其本质是要将原始的样本映射到维度更低的样本空间中，
    但是PCA和LDA的映射目标不一样：PCA是为了让映射后的样本具有最大的发散性；而LDA是为了让映射后的样本有最好的分类性能。
    所以说PCA是一种无监督的降维方法，而LDA是一种有监督的降维方法。
    一般来说，如果我们的数据是有类别标签的，那么优先选择LDA去尝试降维；当然也可以使用PCA做很小幅度的降维去消去噪声，
    然后再使用LDA降维。如果没有类别标签，那么肯定PCA是最先考虑的一个选择了
    '''
    def __init__(self):
         pass
    def rD_PCA(self,x):
        '''
        主成分分析法（PCA）
        主成分分析法，返回降维后的数据
        参数n_components为主成分数目
        '''
        return PCA(n_components=2).fit_transform(x)

    def rD_LDA(self,x,y):
        '''
        线性判别分析法(LDA)
        #线性判别分析法，返回降维后的数据
        #参数n_components为降维后的维数
        '''
        lda = LinearDiscriminantAnalysis(n_components=2)
        lda.fit(x,y)
        X_new = lda.transform(x)
        return X_new

if __name__ == '__main__':
    ##Get Data
    inputData = pd.read_csv('.\ccpp.csv')
    inputData.shape
    orginX = inputData[['AT', 'V', 'AP', 'RH','A','B','C','D','E']]
    print(orginX.head())
    print(orginX.shape)
    orginY = inputData[['RR']]
    fes =FeatureSel()
    # print(fes.pearsonMethode(np.array(orginX)[:,1],np.array(orginX)[:,2]))
    # print(fes.SelectKBestFor(np.array(orginX,dtype='float32'),np.array(orginY).astype('int')))
    # print(fes.rfe(np.array(orginX,dtype='float32'),np.array(orginY).astype('int')))
    # print(fes.SelectFromModelByL1L2(np.array(orginX,dtype='float32'),np.array(orginY).astype('int')))
    # print(fes.SelectFromModelByGBDT(np.array(orginX,dtype='float32'),np.array(orginY).astype('int')))
    rdm =reduceDimense()
    # print(rdm.rD_PCA(np.array(orginX,dtype='float32')))
    print(rdm.rD_LDA(np.array(orginX,dtype='float32'),np.array(orginY).astype('int')))

    
    from sklearn.model_selection import cross_val_score,ShuffleSplit
    # from sklearn.cross_validation import cross_val_score, ShuffleSplit
    from sklearn.datasets import load_boston#波士顿房屋价格预测
    from sklearn.ensemble import RandomForestRegressor
    #集成学习ensemble库中的随机森林回归RandomForestRegressor

    #Load boston housing dataset as an example
    boston = load_boston()
    X = boston["data"]
    Y = boston["target"]
    names = boston["feature_names"]

    rf = RandomForestRegressor(n_estimators=20, max_depth=4)
    #20个弱分类器，深度为4
    scores = []
    for i in range(X.shape[1]):#分别让每个特征与响应变量做模型分析并得到误差率
        score = cross_val_score(rf, X[:, i:i+1], Y, scoring="r2",
                                cv=ShuffleSplit(len(X), 3, .3))
        scores.append((round(np.mean(score), 3), names[i]))
    print (sorted(scores, reverse=True))#对每个特征的分数排序
