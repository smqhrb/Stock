import pandas as pd 
import numpy as np
import math
df =pd.DataFrame({'a':[1,2,3,4],'b':[2,5,0,3],'c':[-1,6,1,4]})
dfk =df[['a','b','c']]
print(dfk.max(axis=1))
print(dfk.min(axis=1))
A =dfk.max(axis=1)
B =dfk.min(axis=1)

glue =(A-B)/B*100
print(glue)
C =np.arctan(A/B)
print(C)
