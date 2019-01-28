# import sys
# sys.path.append('./')
from prepareData import *
from getStockTradeData import stockData
import datetime
from datetime import timedelta
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
from sklearn.externals import joblib
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from sklearn.metrics import r2_score

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor

import matplotlib.pyplot as plt
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

    def localPrepareData(self):
        ##process nan data
        self.flag =0
        imp = SimpleImputer(missing_values=np.nan, strategy='mean')
        im1 = imp.fit(self.inputX)
        tmpX =imp.transform(self.inputX)  
        self.inputX =tmpX  

        imp2 = SimpleImputer(missing_values=np.nan, strategy='mean')
        im2 = imp2.fit(self.inputY) 
        tmpY =imp2.transform(self.inputY)
        self.inputY =tmpY

        #Data normalize
        pre =StandardScaler()
        tmpX =pre.fit_transform(self.inputX)
        self.inputX =tmpX
        pre1 =StandardScaler()
        tmpY =pre1.fit_transform(self.inputY)
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

    def multiModelFix(self,mList,mLable):
        dataFeedX =[]
        dataFeedY =[]
        dataScore =[]
        for ind in range(0,len(mList)):
            mList[ind].fit(self.trainX, self.trainY)
            y_pred = mList[ind].predict(self.testX)
            scoreK = mList[ind].score(self.testX, self.testY)
            # print("r2:%.2f"%r2_score(self.testY,y_pred))
            print(mLable[ind]+'Variance score: %.2f' % scoreK)
            dataFeedX.append(self.testX)
            dataFeedY.append(y_pred)
            dataScore.append(scoreK)
        print("model index :"+str(dataScore.index(max(dataScore))))
        self.finalClf =mList[dataScore.index(max(dataScore))]

        return dataFeedX,dataFeedY,dataScore

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
        # # self.localPrepareData()
        # preDX =prepareData(self.inputX)
        # self.inputX =preDX.scale()
        # preDY =prepareData(self.inputY)
        # self.inputY =preDY.scale()
        self.divDataAsTrain()
        # self.modelFix()
        ###Multi Model Learn###
        modelList =[]
        modelLabel =[]
        # linregModel = LinearRegression()
        # modelList.append(linregModel)
        # modelLabel.append('LinearRegression ')

        # lassoModel =Lasso(alpha=0.5)
        # modelList.append(lassoModel)
        # modelLabel.append('Lasso ')

        # svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.3)
        # modelList.append(svr_rbf)
        # modelLabel.append('SVR.rbf ') 

        # regr_1 = DecisionTreeRegressor(max_depth=4)
        # modelList.append(regr_1)
        # modelLabel.append('regr_1 ') 

        rng = np.random.RandomState(1)
        regr_2 = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4),n_estimators=300,loss='square', random_state=rng)
        modelList.append(regr_2)
        modelLabel.append('regr_2 ') 



        dataFeedX,dataFeedY,dataScore=self.multiModelFix(modelList,modelLabel)
        # self.showResultPlot(dataFeedX,dataFeedY,['r','g'],['linear','lasso'])
        #####
        
        
        self.learnToFinalModel()

    def showResultPlot(self,dataFeedX,dataFeedY,dataColor,dataLabel):
        '''
        only support X,Y are the same dimense
        '''
        # look at the results
        plt.scatter(self.inputX, self.inputY, c='k', label='data')
        for i in range(0,len(dataFeedX)):
            plt.plot(dataFeedX[i], dataFeedY[i], c=dataColor[i], label=dataLabel[i])
        plt.xlabel('data')
        plt.ylabel('target')
        plt.title('Support Vector Regression')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    ##Get Data
    # inputData = pd.read_csv('.\ccpp.csv')
    # inputData.shape
    # orginX = inputData[['A','B','C','D','E']]
    # print(orginX.head())
    # print(orginX.shape)
    # orginY = inputData[['RR']]
    # train =trainProcess()
    # train.runDataLearnModel(np.array(orginX),np.array(orginY))
    ###############
    # start = datetime.datetime(2019, 1, 7)
    # end = datetime.datetime(2019, 1, 9)
    # #从互联网获取数据
    # df = web.DataReader("000651.SZ", "yahoo", start, end)
    # print(df)
    # #print(df.head())
    # df = df[['Open',  'High',  'Low',  'Close', 'Volume']]
    # df['HL_PCT'] = (df['High'] - df['Low']) / df['Close'] * 100.0
    # df['PCT_change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0
    # df = df[['Close', 'HL_PCT', 'PCT_change', 'Volume']]
    # last_date = df.iloc[-1].name
    # last_unix = last_date.timestamp()
    # print(last_date,last_unix)
    # one_day = 86400
    # next_unix = last_unix + one_day

    # for i in range(5):
    #     next_date = datetime.datetime.fromtimestamp(next_unix)
    #     next_unix += 86400
    #     print(next_date)

    # X =np.array(df)
    # X = preprocessing.scale(X)
    # ####
    # train =trainProcess()
    # y_pred =train.getModelFromPkl('000651.pkl',X)
    # print(y_pred)

    # train =trainProcess()
    # # 8.669896007	0.797576364	0.715665422	1.431330844	2.146996266	3.578327111
    # # 3.489489941	0.294683444	0.290436954	0.580873908	0.871310863	1.452184771
    # # 7.951857877	0.717696375	0.657651046	1.315302091	1.972953137	3.288255228
    # # 9.598156776	0.647320792	2.048074513	2.695395305	0.75598543	3.451380736
    # # 13.17550301	0.992880429	2.376762874	3.369643303	1.533286551	4.902929855
    # # 57.14744374	10	8.61690736	18.61690736	0.648360827	19.26526819


    # X=np.array([[10,8.61690736,18.61690736,0.648360827,19.26526819],
    #             [0.992880429,2.376762874,3.369643303,1.533286551,4.902929855]])
    # # X=X.reshape(1,-1)
    # y_pred =train.getModelFromPkl('finalModel.pkl',X)
    # print(y_pred)

    # now_time = datetime.datetime.now()
    # end =now_time.strftime('%Y%m%d')
    # lastyear_time =now_time -timedelta(days=365)
    # start =lastyear_time.strftime('%Y%m%d') 
    ##
    # start ='20000101'
    # end ='20180101'   
    # sd =stockData('000651.SZ',start,end)
    # X,y =sd.preDataForProcess()
    # print(X,y)
    # print(X.shape)
    # print(y.shape)
    # train =trainProcess()
    # train.runDataLearnModel(np.array(X),np.array(y))

    sd =stockData('000651.SZ',"20181121","20190123")
    X,y =sd.preDataForProcess()
    train =trainProcess()
    
    # X=X.reshape(1,-1)
    y_pred =train.getModelFromPkl('finalModel.pkl',X)
    print(y,y_pred)
    print("r2:%.2f"%r2_score(y,y_pred))


