# from sklearn import svm
# X = [[0, 0], [2, 2]]
# y = [0.5, 2.5]
# clf = svm.SVR()
# clf.fit(X, y) 
# print(clf)
# # SVR(C=1.0, cache_size=200, coef0=0.0, degree=3, epsilon=0.1, gamma='auto',
# #     kernel='rbf', max_iter=-1, shrinking=True, tol=0.001, verbose=False)
# print(clf.predict([[1, 1]]))

import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

###############################################################################
# Generate sample data
X = np.sort(5 * np.random.rand(40, 1), axis=0)
y = np.sin(X).ravel()


###############################################################################
# Add noise to targets
y[::5] += 3 * (0.5 - np.random.rand(8))

###############################################################################
# Fit regression model
vX =[]
vY =[]
vC =[]
vL =[]
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(X, y).predict(X)
y_lin = svr_lin.fit(X, y).predict(X)
y_poly = svr_poly.fit(X, y).predict(X)
vX.append(X)
vX.append(X)
vX.append(X)

vY.append(y_rbf)
vY.append(y_lin)
vY.append(y_poly)
vC.append('g')
vC.append('r')
vC.append('b')
vL.append('RBF model')
vL.append('Linear model')
vL.append('Polynomial model')
###############################################################################
# look at the results
plt.scatter(X, y, c='k', label='data')
# plt.plot(X, y_rbf, c='g', label='RBF model')
# plt.plot(X, y_lin, c='r', label='Linear model')
# plt.plot(X, y_poly, c='b', label='Polynomial model')
for i in range(0,len(vX)):
    plt.plot(vX[i], vY[i], c=vC[i], label=vL[i])
plt.xlabel('data')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()



