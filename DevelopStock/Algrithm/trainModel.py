import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
 
##Get Data
inputData = pd.read_csv('.\ccpp.csv')
inputData.shape
orginX = inputData[['AT', 'V', 'AP', 'RH','A','B','C','D','E']]
print(orginX.head())
print(orginX.shape)
orginY = inputData[['RR']]
##process nan data
from sklearn.impute import SimpleImputer
imp = SimpleImputer(missing_values=np.nan, strategy='mean')
im1 = imp.fit(orginX)
secondX =imp.transform(orginX)
#Data normalize
from sklearn.preprocessing import StandardScaler
pre =StandardScaler()
X =pre.fit_transform(secondX)

##div trainData,TestData,ValidataData
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, orginY, random_state=1)

###start traina
from sklearn.linear_model import LinearRegression
linregModel = LinearRegression()
linregModel.fit(X_train, y_train)



##test on X_test
y_pred = linregModel.predict(X_test)
print('Variance score: %.2f' % linregModel.score(X_test, y_test))

##other model
# from sklearn.svm import SVR
#
from sklearn.linear_model import Lasso
lassoModel =Lasso(alpha=0.5)
lassoModel.fit(X_train, y_train)
y_pre =lassoModel.predict(X_test)
print('Lasso Variance score: %.2f' % lassoModel.score(X_test, y_test))
##
## train on whole X using the best Model
## get final model
finalModel_lasso = Lasso(alpha=0.5)
finalModel_lasso.fit(X,orginY)


##save model
from sklearn.externals import joblib
joblib.dump(finalModel_lasso,'lasso.pkl')
finalModel_lasso1=joblib.load('lasso.pkl')
print('Final Model Lasso1 Variance score: %.2f' % finalModel_lasso1.score(X_test, y_test))
