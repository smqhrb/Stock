from sklearn import preprocessing
import numpy as np
class prepareData:
    def __init__(self,data):
        self.data =data
    def __call__(self,data):
        self.data =data
#标准化(中心化)
    def scale(self):
        '''
        忽略了分布的形状，只需要通过减去每个特征的均值，然后除以非标准特征的标准偏差来转换数据
        preprocessing.scale
        方法提供了在一个类似数据的数据集上执行操作的简便方法
        公式为：(X-mean)/std  计算时对每个属性/每列分别进行
        将数据按期属性（按列进行）减去其均值，并处以其方差。
        得到的结果是，对于每个属性/每列来说所有数据都聚集在0附近，方差为1。
        '''
        X_scaled = preprocessing.scale(self.data)
        print("%s/%s"%(X_scaled.mean(axis=0),X_scaled.std(axis=0)))
        return X_scaled
    def StandardScaler(self):
        '''
        preprocessing模块还提供了一种使用类：StandardScaler，主要计算训练集的均值和标准差，然后应用在测试集的转换上
        '''
        scaler = preprocessing.StandardScaler().fit(self.data)      
        data =scaler.transform(self.data)                          
        return data

    def MinMaxScaler(self):
        '''
        # 1.1将特征缩放到一个范围
        另一种标准化方法是将特征值缩放到在一个给定的最小值和最大值之间，通常是0~1；
        或者每个特征的最大绝对值被缩放到单位大小。该方法可以分别通过MinMaxScaler或者MaxAbsScaler实现。
        X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
        X_scaled = X_std * (max - min) + min
        '''
        # preprocessing.minmax_scale(self.data)
        min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0,1))
        X_train_minmax = min_max_scaler.fit_transform(self.data)
        # X=min_max_scaler.inverse_transform(X_train_minmax)#利用上面的归一化结构反归一化
        return X_train_minmax
    
    def MaxAbsScaler(self):
        '''
        1.2稀疏数据缩放
        对稀疏数据中心化处理会破坏数据的稀疏性结构，所以很少对稀疏数据中心化。
        但是如果特征在不同的方差下，依然需要对数据进行缩放。
        类MaxAbsScaler和方法maxabs_scale是专门用来对稀疏数据进行缩放的。
        '''
        max_abs_scaler = preprocessing.MaxAbsScaler()
        X_train_maxabs = max_abs_scaler.fit_transform(self.data)
        # preprocessing.maxabs_scale(self.data)
        return X_train_maxabs
    def RobustScaler(self):
        '''
        如果数据集中包含很多离群点，那么使用数据的均值方差进行缩放的效果不会很好。
        在这种情况下，可以使用方法robust_scale和类RobustScaler来进行替换，它们对数据的均值和方差使用更健壮的估计
        '''
        robustscalerr_scaler = preprocessing.RobustScaler() # 建立RobustScaler标准化对象
        data_scale = robustscalerr_scaler.fit_transform(self.data) # RobustScaler标准化标准化处理
        # preprocessing.robust_scale(self.data)
        return data_scale
    def KernelCenterer(self):
        '''
        1.4、中心化核矩阵
        如果有一个核K的核矩阵，通过定义的函数phi计算特征空间的点积，
        使用类KernelCenterer可以变换核矩阵，它包含去除特征空间均值后，再利用phi计算特征空间的内积
        '''
        transformer = preprocessing.KernelCenterer().fit(self.data)
        return transformer.transform(self.data)
    def Normalizer(self):
        '''
        2、归一化
        归一化是将单个样本缩放为单位范数的过程。如果使用一个二次形式，例如点积或其他任何内核来量化一对样本的相似度，这个步骤会很有必要。这个步骤是向量空间模型的基础，常被用于文本分类和聚类中。
        normalize方法提供了快速简单的方法来对单个array数据集进行归一化，可以选择L1或者L2范数。
        preprocessing.normalize(X, norm='l2')
        preprocessing模块还提供了类Normalizer，通过方法Transformer API对另一数据集执行同样的操作。
        normalizer = preprocessing.Normalizer().fit(X)
        normalizer.transform(X)
        注：normalize和Normalizer同样适用于类似array的稠密的或者稀疏的矩阵
        '''
        # preprocessing.normalize(self.data, norm='l2')
        normalizer = preprocessing.Normalizer().fit(self.data)
        normData =normalizer.transform(self.data)
        return normData

    def Binarizer(self,thresholdV):
        '''
        3、二值化
        特征二值化是对数值特征进行阈值化以得到布尔值的过程。这对于假设输入数据服从多变量伯努利分布的后验分布的估计是有用的。例如，在sklearn.neural_network.BernoulliRBM的使用时需要二值化。
        在文本处理中经常使用二值特征（可能是为了简化推理过程），例如在计数或者TF-IDF特征值中，使用二值特征能够更有效。
        类Binarizer是专门用于二值化的，例如：
        preprocessing.Binarizer().fit(X)或者preprocessing.Binarizer(threshold=1.1)
        binarizer.transform(X)
        preprocessing模块提供binarize方法来对特征进行二值化处理
        '''
        # preprocessing.Binarizer(threshold=thresholdV)
        binarizer =preprocessing.Binarizer(threshold=thresholdV).fit(self.data)
        binData =binarizer.transform(self.data)
        return binData
    def OneHotEncoder(self):
        '''
        4、种类特征编码
        在很多情况下，特征值不是连续的值而是种类。例如，一个人可能的特征是[male, female]等等，这些特征可以用整数值来进行编码。
        在scikit-learn中，将种类特征用1-of-k或者one-hot编码。预处理模块中有OneHotEncoder来对种类特征编码，
        通常是m个可能的种类用m个值来表示。例如： preprocessing.OneHotEncoder()
        默认情况下，m值时通过数据集自动推断出来的。例如，数据集中有2种性别，三种可能的地方，4中可能的浏览器。
        然后在编码时，在9列的array数组中，前2个数字编码性别，接下来3个数字编码地方，最后4个数字编码浏览器
        '''
        # enc =preprocessing.OneHotEncoder()
        enc = preprocessing.OneHotEncoder(categorical_features=np.array([1,2,4,5,6,7,8,9,10,11,14,15,16,17,18,21]),
                                                  n_values=[13,13,9,5,5,13,5,2,13,13,9,31,10,5,2,9])
        enc.fit(self.data)
        return enc.transform(self.data).toarray()

    def Imputer(self):
        '''
        5、缺失值处理
        由于各种原因，许多现实世界的数据集包含缺失值，通常变为为空白、NaN或其他占位符。
        使用不完整数据集的基本策略是丢弃包含缺失值的整行或整列，然而这样会丢失可能有价值的数据。
        一个更好的策略就是从已知的部分数据中推断出缺失值。
        Imputer类提供了基本的策略来填充缺失值，可以用行或者列的均值、中位数或众数来填充缺失值。例如：
        imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
        imp.fit([[1, 2], [np.nan, 3], [7, 6]])
        X = [[np.nan, 2], [6, np.nan], [7, 6]]
        imp.transform(X)
        该类还支持稀疏矩阵（将缺失值编码为0），将稀疏矩阵填充为稠密的矩阵。
        '''
        imp = preprocessing.Imputer(missing_values='NaN', strategy='mean', axis=0)
        imp.fit(self.data)
        return imp.transform(self.data)
    
    def PolynomialFeatures(self,order):
        '''
        6、生成多项式特征
        通常，通过考虑输入数据的非线性特征来增加模型的复杂度是很有用的。一个简单常用的方法是多项式特征，
        它可以得到特征的高阶和相互作用项。PolynomialFeatures类可以用来生成多项式特征。
        poly = PolynomialFeatures(2)
        poly.fit_transform(X)     
        上述将(X1, X2)转化为(1, X1, X2, X1^2, X1X2, X2^2)
        应用范围：多样式特征常用于核方法中（SVM, 核PCA）
        '''
        poly = preprocessing.PolynomialFeatures(order)
        polyData =poly.fit_transform(self.data)
        return polyData

if __name__ == '__main__':
    preD =prepareData( np.array([[1,2,3],[2,3,4],[3,4,5]]))
    # print(preD.scale())
    # print(preD.StandardScaler())
    # print(preD.MinMaxScaler())
    # print(preD.MaxAbsScaler())
    # print(preD.RobustScaler())
    # print(preD.KernelCenterer())
    # print(preD.Normalizer())
    print(preD.Binarizer(3))
    # print(preD.OneHotEncoder())##not understand
    preD =prepareData(np.array([[1, 2], [np.nan, 3], [7, 6]]))
    preD.data=preD.Imputer()
    print(preD.data)

    print(preD.PolynomialFeatures(2))



        








    
