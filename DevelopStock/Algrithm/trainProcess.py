
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.externals import joblib
import numpy as np
import pandas as pd
class trainProcess:
    def __init__(self):
        self.inputX =0
        self.inputY =0
        self.trainX =0
        self.trainY =0
        self.testX =0
        self.testY =0
        self.finalClf =0
        self.flag = 0

    def setData(self,x,y):
        self.inputX =x
        self.inputY =y

    def prepareData(self):
        ##process nan data
        self.flag =0
        imp = SimpleImputer(missing_values=np.nan, strategy='mean')
        im1 = imp.fit(self.inputX)
        tmpX =imp.transform(self.inputX)  
        self.inputX =tmpX  

        im2 = imp.fit(self.inputY) 
        tmpY =imp.transform(self.inputY)
        self.inputY =tmpY

        #Data normalize
        pre =StandardScaler()
        tmpX =pre.fit_transform(self.inputX)
        self.inputX =tmpX
        tmpY =pre.fit_transform(self.inputY)
        self.inputY =tmpY

    def divDataAsTrain(self):
        X_train, X_test, y_train, y_test = train_test_split(self.inputX, self.inputY, random_state=1) 
        self.trainX =X_train
        self.trainY =y_train
        self.testX =X_test
        self.testY =y_test        
    
    def modelFix(self):
        ###model
        linregModel = LinearRegression()
        linregModel.fit(self.trainX, self.trainY)
        ##test on X_test
        y_pred = linregModel.predict(self.testX)
        scoreLinear =linregModel.score(self.testX, self.testY)
        print('Variance score: %.2f' % scoreLinear)
        ###
        lassoModel =Lasso(alpha=0.5)
        lassoModel.fit(self.trainX, self.trainY)
        y_pre =lassoModel.predict(self.testX)
        ###score
        scoreLasso =lassoModel.score(self.testX, self.testY)
        print('Lasso Variance score: %.2f' % scoreLasso)

        if scoreLinear>scoreLasso:
            self.finalClf =linregModel
        else:
            self.finalClf =lassoModel
        self.flag =1

    def learnToFinalModel(self):
 ##save model
        self.finalClf.fit(self.inputX,self.inputY)
        joblib.dump(self.finalClf,'finalModel.pkl')
        
    def getModelFromPkl(self,fileName,x):
        haveModel =joblib.load(fileName)  
        y_pred =haveModel.predict(x)
        return y_pred

    def getModel(self):
        if self.flag ==1:
            return self.finalClf
        else:
            return None

    def runDataLearnModel(self,x,y):
        self.setData(x,y)
        self.prepareData()
        self.divDataAsTrain()
        self.modelFix()
        self.learnToFinalModel()

if __name__ == '__main__':
    ##Get Data
    inputData = pd.read_csv('.\ccpp.csv')
    inputData.shape
    orginX = inputData[['AT', 'V', 'AP', 'RH','A','B','C','D','E']]
    print(orginX.head())
    print(orginX.shape)
    orginY = inputData[['RR']]
    train =trainProcess()
    train.runDataLearnModel(orginX,orginY)
