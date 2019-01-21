from sklearn import svm
from sklearn.datasets import samples_generator #引入生成数据集
from sklearn.feature_selection import SelectKBest #特征选择，选出最佳的K个特征
from sklearn.feature_selection import f_regression#f_regression（单因素线性回归试验）用作回归 chi2卡方检验，f_classif（方差分析的F值）等用作分类
from sklearn.pipeline import Pipeline

X, y = samples_generator.make_classification(
    # n_samples=100 #样本数
    # n_features=100 #特征数量（自变量个数）
    # n_targets=3 #因变量个数
    # bias=1 #偏差（截距）
    # coef=True #是否输出coef回归系数，
    n_informative=5, #相关特征(相关自变量个数)即参与了建模型的特征数
    n_redundant=0,  #冗余数量
    random_state=42) #随机种子，不需要调该参数而是固定之后，再训练模型，可实现可重复训练。
print(X.shape)  #100行20列
print(y)  #100行1列
anova_filter = SelectKBest(f_regression, k=5)  #方差(anova)分析
clf = svm.SVC(kernel='linear')  #SVC分类  SVR回归
anova_svm = Pipeline(steps=[
    ('anova', anova_filter),
    ('svc', clf)
    ])
anova_svm.set_params(anova__k=10, svc__C=.1).fit(X, y)  #parameters变量里面的key都有一个前缀，该前缀就是在Pipeline中定义的操作名
prediction = anova_svm.predict(X)
print(prediction)
print(anova_svm.score(X, y)) #0.83
print(anova_svm.named_steps['anova'].get_support())#20个特征中选出的10个特征
# [False False  True  True False False  True  True False  True False
# True True False  True False  True  True False False]
anova_svm.named_steps.anova.get_support() #同样是输出选择的10个特征
from sklearn import linear_model
clf = linear_model.LinearRegression()
X = [[0,0],[1,1],[2,2]]   
y = [0,1,2]
clf.fit(X,y,sample_weight = None)#则是每条测试数据的权重，同样以array格式传入。
print(clf.coef_) #[ 0.5 0.5]存放回归系数，
print(clf.intercept_)# 1.11022302463e-16 存放截距
