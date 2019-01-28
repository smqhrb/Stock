import numpy as np
def make_data(N, err=1.0, rseed=1):
    # randomly sample the data
    rng = np.random.RandomState(rseed)
    X = rng.rand(N, 1) ** 2
    y = 10 - 1. / (X.ravel() + 0.1)
    if err > 0:
        y += err * rng.randn(N)
    return X, y
X, y = make_data(40)

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
def PolynomialRegression(degree=2, **kwargs):
    return make_pipeline(PolynomialFeatures(degree),LinearRegression(**kwargs))

from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(16, 6))
fig.subplots_adjust(left=0.0625, right=0.95, wspace=0.1)
for i, degree in enumerate([2, 9]):
    N, train_lc, val_lc = learning_curve(PolynomialRegression(degree),X, y, cv=7,train_sizes=np.linspace(0.3, 1, 25))
    ax[i].plot(N, np.mean(train_lc, 1), color='blue', label='training score')
    ax[i].plot(N, np.mean(val_lc, 1), color='red', label='validation score')
    ax[i].hlines(np.mean([train_lc[-1], val_lc[-1]]), N[0], N[-1], color='gray',linestyle='dashed')
    ax[i].set_ylim(0, 1)
    ax[i].set_xlim(N[0], N[-1])
    ax[i].set_xlabel('training size')
    ax[i].set_ylabel('score')
    ax[i].set_title('degree = {0}'.format(degree), size=14)
    ax[i].legend(loc='best')
plt.show()

# from sklearn.model_selection import GridSearchCV
# param_grid = {'polynomialfeatures__degree': np.arange(21),
# 'linearregression__fit_intercept': [True, False],
# 'linearregression__normalize': [True, False]}
# grid = GridSearchCV(PolynomialRegression(), param_grid, cv=7)
# grid.fit(X, y)
# grid.best_params_
# model = grid.best_estimator_
# plt.scatter(X.ravel(), y)
# lim = plt.axis()
# y_test = model.fit(X, y).predict(X_test)
# plt.plot(X_test.ravel(), y_test, hold=True)
# plt.axis(lim)