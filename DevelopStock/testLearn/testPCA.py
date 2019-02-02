import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import seaborn as sns; 
sns.set()
# rng = np.random.RandomState(1)
# X = np.dot(rng.rand(2, 2), rng.randn(2, 200)).T
# plt.scatter(X[:, 0], X[:, 1])
# plt.axis('equal');
# # plt.show()
# from sklearn.decomposition import PCA
# pca = PCA(n_components=2)
# pca.fit(X)
# print(pca.components_)
# print(pca.explained_variance_)

# def draw_vector(v0, v1, ax=None):
#     ax = ax or plt.gca()
#     arrowprops=dict(arrowstyle='->',
#                     linewidth=2,
#                     shrinkA=0, shrinkB=0)
#     ax.annotate('', v1, v0, arrowprops=arrowprops)

# plt.scatter(X[:, 0], X[:, 1], alpha=0.2)
# for length, vector in zip(pca.explained_variance_, pca.components_):
#     v = vector * 3 * np.sqrt(length)
#     draw_vector(pca.mean_, pca.mean_ + v)
# plt.axis('equal'); 
# # plt.show()  
# pca = PCA(n_components=1)
# pca.fit(X)
# X_pca = pca.transform(X)
# print("original shape: ", X.shape)
# print("transformed shape:", X_pca.shape) 

# X_new = pca.inverse_transform(X_pca)
# plt.scatter(X[:, 0], X[:, 1], alpha=0.2)
# plt.scatter(X_new[:, 0], X_new[:, 1], alpha=0.8)
# plt.axis('equal');
# plt.show()

from sklearn.datasets import load_digits
digits = load_digits()
print(digits.data.shape)
# pca = PCA(2) # project from 64 to 2 dimensions
# projected = pca.fit_transform(digits.data)
# print(digits.data.shape)
# print(projected.shape)

# plt.scatter(projected[:, 0], projected[:, 1],c=digits.target, edgecolor='none', alpha=0.5
#             )#,cmap=plt.cm.get_cmap('spectral', 10)
# plt.xlabel('component 1')
# plt.ylabel('component 2')
# plt.colorbar();
# plt.show()

pca = PCA().fit(digits.data)
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance');
plt.show()