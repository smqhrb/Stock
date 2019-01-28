
# import lightgbm as lgb
# import pandas as pd
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import GridSearchCV

# # load or create your dataset
# print('Load data...')
# # df_train =pd.read_csv('ccpp.csv')
# # df_test =pd.read_csv('ccpp.csv')
# df_train = pd.read_csv('../regression/regression.train', header=None, sep='\t')
# df_test = pd.read_csv('../regression/regression.test', header=None, sep='\t')

# y_train = df_train[0].values
# y_test = df_test[0].values
# X_train = df_train.drop(0, axis=1).values
# X_test = df_test.drop(0, axis=1).values

# print('Start training...')
# # train
# gbm = lgb.LGBMRegressor(objective='regression',
#                         num_leaves=31,
#                         learning_rate=0.05,
#                         n_estimators=20)
# gbm.fit(X_train, y_train,
#         eval_set=[(X_test, y_test)],
#         eval_metric='l1',
#         early_stopping_rounds=5)

# print('Start predicting...')
# # predict
# y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration_)
# # eval
# print('The rmse of prediction is:', mean_squared_error(y_test, y_pred) ** 0.5)

# # feature importances
# print('Feature importances:', list(gbm.feature_importances_))

# # other scikit-learn modules
# estimator = lgb.LGBMRegressor(num_leaves=31)

# param_grid = {
#     'learning_rate': [0.01, 0.1, 1],
#     'n_estimators': [20, 40]
# }

# gbm = GridSearchCV(estimator, param_grid)

# gbm.fit(X_train, y_train)

# print('Best parameters found by grid search are:', gbm.best_params_)
# import lightgbm as lgb
# from sklearn import metrics

# def auc2(m, train, test): 
#     return (metrics.roc_auc_score(y_train,m.predict(train)),
#                             metrics.roc_auc_score(y_test,m.predict(test)))

# lg = lgb.LGBMClassifier(silent=False)
# param_dist = {"max_depth": [25,50, 75],
#               "learning_rate" : [0.01,0.05,0.1],
#               "num_leaves": [300,900,1200],
#               "n_estimators": [200]
#              }
# grid_search = GridSearchCV(lg, n_jobs=-1, param_grid=param_dist, cv = 3, scoring="roc_auc", verbose=5)
# grid_search.fit(train,y_train)
# grid_search.best_estimator_

# d_train = lgb.Dataset(train, label=y_train)
# params = {"max_depth": 50, "learning_rate" : 0.1, "num_leaves": 900,  "n_estimators": 300}

# # Without Categorical Features
# model2 = lgb.train(params, d_train)
# auc2(model2, train, test)

# #With Catgeorical Features
# cate_features_name = ["MONTH","DAY","DAY_OF_WEEK","AIRLINE","DESTINATION_AIRPORT",
#                  "ORIGIN_AIRPORT"]
# model2 = lgb.train(params, d_train, categorical_feature = cate_features_name)
# auc2(model2, train, test)
# import xgboost as xgb
# from sklearn import metrics

# def auc(m, train, test): 
#     return (metrics.roc_auc_score(y_train,m.predict_proba(train)[:,1]),
#                             metrics.roc_auc_score(y_test,m.predict_proba(test)[:,1]))

# # Parameter Tuning
# model = xgb.XGBClassifier()
# param_dist = {"max_depth": [10,30,50],
#               "min_child_weight" : [1,3,6],
#               "n_estimators": [200],
#               "learning_rate": [0.05, 0.1,0.16],}
# grid_search = GridSearchCV(model, param_grid=param_dist, cv = 3, 
#                                    verbose=10, n_jobs=-1)
# grid_search.fit(train, y_train)

# grid_search.best_estimator_

# model = xgb.XGBClassifier(max_depth=50, min_child_weight=1,  n_estimators=200,\
#                           n_jobs=-1 , verbose=1,learning_rate=0.16)
# model.fit(train,y_train)

# auc(model, train, test)


from sklearn import datasets    # 载入数据集
digits = datasets.load_digits() # 载入mnist数据集
print(digits.data.shape)        # 打印输入空间维度
print(digits.target.shape)      # 打印输出空间维度
"""
(1797, 64)
(1797,)
"""
from sklearn.model_selection import train_test_split                 # 载入数据分割函数train_test_split
x_train,x_test,y_train,y_test = train_test_split(digits.data,        # 特征空间
                                                 digits.target,      # 输出空间
                                                 test_size = 0.3,    # 测试集占30%
                                                 random_state = 33)  # 为了复现实验，设置一个随机数

from xgboost import XGBClassifier
model = XGBClassifier()               # 载入模型（模型命名为model)
model.fit(x_train,y_train)            # 训练模型（训练集）
y_pred = model.predict(x_test)        # 模型预测（测试集），y_pred为预测结果
### 性能度量
from sklearn.metrics import accuracy_score   # 准确率
accuracy = accuracy_score(y_test,y_pred)
print("accuarcy: %.2f%%" % (accuracy*100.0))

"""
95.0%
"""

### 特征重要性
import matplotlib.pyplot as plt
from xgboost import plot_importance
fig,ax = plt.subplots(figsize=(10,15))
plot_importance(model,height=0.5,max_num_features=64,ax=ax)
plt.show()