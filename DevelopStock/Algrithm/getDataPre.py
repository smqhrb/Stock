import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
# read_csv里面的参数是csv在你电脑上的路径，此处csv文件放在notebook运行目录下面的CCPP目录里
data = pd.read_csv('.\ccpp.csv')
#读取前五行数据，如果是最后五行，用data.tail()
data.shape
X1 = data[['AT', 'V', 'AP', 'RH','A','B','C','D','E']]
print(X1.head())
print(X1.shape)
y1 = data[['RR']]
y1.head()

from sklearn.impute import SimpleImputer
imp = SimpleImputer(missing_values=np.nan, strategy='mean')
im1 = imp.fit(X1)
X2 =imp.transform(X1)

# print(X1(20),X2(20))
X1 =X2
from sklearn.preprocessing import StandardScaler

# X =preprocessing.scale(X1)
# y =preprocessing.scale(y1)
pre =StandardScaler()
pre1 =StandardScaler()
X =pre.fit_transform(X1)
# y =pre1.fit_transform(y1)
y =y1

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
print (X_train.shape)
print (y_train.shape)


from sklearn.linear_model import LinearRegression

linreg = LinearRegression()
# from sklearn.svm import SVR
# linreg =SVR()
linreg.fit(X_train, y_train)
print("linreg coefficent")
print (linreg.intercept_)
print (linreg.coef_)

#模型拟合测试集
y_pred = linreg.predict(X_test)
print('Variance score: %.2f' % linreg.score(X_test, y_test))
from sklearn.linear_model import Lasso
la =Lasso(alpha=0.5)
la.fit(X_train, y_train)
print("Lasso coefficent")
print (la.intercept_)
print (la.coef_)
y_pre =la.predict(X_test)
print('Lasso Variance score: %.2f' % la.score(X_test, y_test))
from sklearn import metrics
# 用scikit-learn计算MSE
print ("MSE:",metrics.mean_squared_error(y_test, y_pred))
# 用scikit-learn计算RMSE
print ("RMSE:",np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

# X = data[['AT', 'V', 'AP', 'RH']]
# y = data[['PE']]
# from sklearn.model_selection import cross_val_predict
# predicted = cross_val_predict(linreg, X, y, cv=5)
# # 用scikit-learn计算MSE
# print ("MSE:",metrics.mean_squared_error(y, predicted))
# # 用scikit-learn计算RMSE
# print ("RMSE:",np.sqrt(metrics.mean_squared_error(y, predicted)))

fig, ax = plt.subplots()
#ax.scatter(y, predicted)
ax.scatter(y_test, y_pred)
print(y_test)
print(y_pred)

# print(pre.inverse_transform(y_test))
# print(pre1.inverse_transform(y_pred))
#ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
# ax.plot(y_test, y_pred, 'g', lw=1)

ax.set_xlabel('Measured')
ax.set_ylabel('Predicted')
plt.show()

# import pickle
# s =pickle.dumps(la)
# f =open("lasso.txt",'w')
# f.write(s)
# f.close()
# f2 =open('lasso.txt','r')
# s2 =f2.read()
# clf2 = pickle.load(s2)
# print('Variance score: %.2f' % clf2.score(X_test, y_test))

#save model
from sklearn.externals import joblib
joblib.dump(la,'lasso.pkl')
la1=joblib.load('lasso.pkl')
print('Lasso1 Variance score: %.2f' % la1.score(X_test, y_test))
