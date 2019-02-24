from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from numpy import shape
import numpy as np
from sklearn.metrics.metrics import classification_report
from sklearn.metrics import confusion_matrix


train_data = open("../../data/data/train.csv","r")
test_data = open("../../data/data/test.csv","r")
##train data
train_feature=[]
train_target=[]
for line in train_data:
    temp = line.strip().split(',')
    train_feature.append(map(int,temp[0:-1]))
    train_target.extend(map(int,temp[-1]))
train_data.close()
##test data
test_feature=[]
test_target=[]
for line in test_data:
    temp = line.strip().split(',')
    test_feature.append(map(int,temp[0:-1]))
    test_target.extend(map(int,temp[-1]))
test_data.close()

train_feature = np.array(train_feature)
test_feature = np.array(test_feature)


##OneHotEncoder used
enc = OneHotEncoder(categorical_features=np.array([1,2,4,5,6,7,8,9,10,11,14,15,16,17,18,21]),n_values=[13,13,9,5,5,13,5,2,13,13,9,31,10,5,2,9])
enc.fit(train_feature)

train_feature = enc.transform(train_feature).toarray()
test_feature = enc.transform(test_feature).toarray()
clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(train_feature,train_target)

##result
print (clf.predict(test_feature))
target_names = ['losing', 'active']
print (classification_report(test_target, clf.predict(test_feature),target_names=target_names))