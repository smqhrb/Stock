import numpy as np
X = np.array([[1,2,3,4,5],[21,22,23,24,25],[31,32,33,34,35],[41,42,43,44,45]])
print(X)
X1 =X[-1:]
print(X1)
X2 =X[:-1]
print(X2)
def a(d,e):
    return d,e
dd,ee =a([1,2,3],[4,5])
print(dd)
print(ee)
aa = [1,2,3,4,5]
print(aa.index(max(aa)))