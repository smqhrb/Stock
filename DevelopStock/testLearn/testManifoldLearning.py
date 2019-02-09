from matplotlib.image import imread
import matplotlib.pyplot as plt
import numpy as np
def make_hello(N=1000, rseed=42):
    # Make a plot with "HELLO" text; save as PNG
    fig, ax = plt.subplots(figsize=(4, 1))
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis('off')
    ax.text(0.5, 0.4, 'HELLO', va='center', ha='center', weight='bold', size=85)
    fig.savefig('hello.png')
    plt.close(fig)
    # Open this PNG and draw random points from it

    data = imread('hello.png')[::-1, :, 0].T
    rng = np.random.RandomState(rseed)
    X = rng.rand(4 * N, 2)
    i, j = (X * data.shape).astype(int).T
    mask = (data[i, j] < 1)
    X = X[mask]
    X[:, 0] *= (data.shape[0] / data.shape[1])
    X = X[:N]
    return X[np.argsort(X[:, 0])]
X = make_hello(1000)
colorize = dict(c=X[:, 0], cmap=plt.cm.get_cmap('rainbow', 5))
plt.scatter(X[:, 0], X[:, 1], **colorize)
plt.axis('equal');

def rotate(X, angle):
    theta = np.deg2rad(angle)
    R = [[np.cos(theta), np.sin(theta)],[-np.sin(theta), np.cos(theta)]]
    return np.dot(X, R)
X2 = rotate(X, 20) + 5
plt.scatter(X2[:, 0], X2[:, 1], **colorize)
plt.axis('equal')
plt.show()

from sklearn.metrics import pairwise_distances
D = pairwise_distances(X)
print(D.shape)

from sklearn.manifold import MDS
model = MDS(n_components=2, dissimilarity='precomputed', random_state=1)
out = model.fit_transform(D)
plt.scatter(out[:, 0], out[:, 1], **colorize)
plt.axis('equal');
# plt.show()

def random_projection(X, dimension=3, rseed=42):
    assert dimension >= X.shape[1]
    rng = np.random.RandomState(rseed)
    C = rng.randn(dimension, dimension)
    e, V = np.linalg.eigh(np.dot(C, C.T))
    return np.dot(X, V[:X.shape[1]])
X3 = random_projection(X, 3)
print(X3.shape)

# from mpl_toolkits import mplot3d
# ax = plt.axes(projection='3d')
# ax.scatter3D(X3[:, 0], X3[:, 1], X3[:, 2],**colorize)
# ax.view_init(azim=70, elev=50)

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
y3 = np.arctan2(X3[:, 0], X3[:, 1])
ax.scatter(X3[:, 0], X3[:, 1], X3[:, 2], c=y3, marker='.', s=50, label='')
plt.show()

def make_hello_s_curve(X):
    t = (X[:, 0] - 2) * 0.75 * np.pi
    x = np.sin(t)
    y = X[:, 1]
    z = np.sign(t) * (np.cos(t) - 1)
    return np.vstack((x, y, z)).T
XS = make_hello_s_curve(X)
# from mpl_toolkits import mplot3d
# ax = plt.axes(projection='3d')
# ax.scatter3D(XS[:, 0], XS[:, 1], XS[:, 2],**colorize);

from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = Axes3D(fig)
y3 = np.arctan2(XS[:, 0], XS[:, 1])
ax.scatter(XS[:, 0], XS[:, 1], XS[:, 2], c=y3, marker='.', s=50, label='')
# plt.show()

# from sklearn.manifold import MDS
# model = MDS(n_components=2, random_state=2)
# outS = model.fit_transform(XS)
# plt.scatter(outS[:, 0], outS[:, 1], **colorize)
# plt.axis('equal');
# plt.show()

rom sklearn.manifold import LocallyLinearEmbedding
model = LocallyLinearEmbedding(n_neighbors=100, n_components=2, method='modified',
eigen_solver='dense')
out = model.fit_transform(XS)
fig, ax = plt.subplots()
ax.scatter(out[:, 0], out[:, 1], **colorize)
ax.set_ylim(0.15, -0.15);