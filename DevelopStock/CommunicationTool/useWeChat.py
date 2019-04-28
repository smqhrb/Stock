# https://www.jb51.net/article/121076.htm
import time
import itchat
import pandas as pd
from sqlalchemy import create_engine
class mysqlDB:
    def __init__(self):
        self.userName ='root'#数据库用户名
        self.passWord ='1234'#数据库密码
        self.IP ='127.0.0.1'#数据库IP
        self.Port ='3306'#数据库端口
        self.dbName ='zj'#数据库内库名
        self.status ="connected"#连接状态
        try:
            #连接数据库
            self.engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s'%(self.userName,self.passWord,self.IP,self.Port,self.dbName))
            self.con = self.engine.connect()
        except Exception as e:#连接异常
            self.status ="unconnect"
            # print(str(e))
    def read_sql_query(self,sql):
        '''
        读取数据库
        sql ：查询sql
        '''
        if(self.status =="connected"):#检测数据库的连接状态
            df = pd.read_sql_query(sql, self.engine)#读取数据返回 DataFrame
            return df
        else:
            return pd.DataFrame()
        
    def updateInsertDelete(self,updateSentence):
        try:
            cursor = self.engine.execute(updateSentence)
            
            
        except:
            
            print("except "+updateSentence)
    def getDbStatus(self):
        '''
        返回数据库状态
        '''
        return  (self.status =="connected" )     

    def to_sql(self,dataf,tbl):
        '''
        dataf:存入数据的DataFrame
        tbl：数据库表名
        '''
        rowCnt =len(dataf)
        for i in range(rowCnt):
            try: 
                dataf.iloc[i:i+1].to_sql(name =tbl,  con=self.con, if_exists='append',index= False)
                # dataf.to_sql(name =tbl,  con=self.con, if_exists='append',index= False)#name='rumousdata', con=con, if_exists='append', index=False
            except Exception as e:
                pass#
                # print('Error is ' + str(e))
                #self.con.rollback()
class WxSms:
    def login(self):
        pass

    def sendLoop(self):
        itchat.auto_login(hotReload=True)
        # #想给谁发信息，先查找到这个朋友
        # users = itchat.search_friends(name=u'安士霞')
        # #找到UserName
        # userName = users[0]['UserName']
        # #然后给他发消息
        # flag =itchat.send('hello',toUserName = userName)
        # print(flag)

        #从文件或数据库读取发送人员昵称列表
        friends = itchat.get_friends(update=True)[0:]


        nikeNameList =['安士霞']
        userNameList =[]
        # userNameList.append(userName)

        lenList =len(nikeNameList)
        for i in range(lenList):
            for friend in friends[1:]:
                nickName = friend['NickName']
                if(nickName == nikeNameList[i]):
                    userName =friend['UserName']
                    userNameList.append(userName)
                    break


            # users = itchat.search_friends(name=nikeNameList[i])
            # userNameList.append(users[0]['UserName'])

        #发送信息 每隔两秒发一个
        dbOper = mysqlDB()
        while(1):
            #从短信表中读取记录
            df =dbOper.read_sql_query("select smsSubject,smsContent,smsType from spcard.sms_send where smsState = 0")
            lenDf =len(df)
            for j in range(lenDf):
                #判断是否是彩信
                smsType =df.iloc[[j]].smsType[0]
                smsContent =df.iloc[[j]].smsContent[0]
                smsSubject =df.iloc[[j]].smsSubject[0]
                lenList =len(userNameList)
                for i in range(lenList):
                    if(smsType ==1):
                        #是彩信
                        
                        index =smsContent.find('####',0,len(smsContent))
                        imageName =smsContent[index+4:]
                        print(imageName)
                        #imageName ='./hello.png'
                        userName =userNameList[i]
                        
                        subContent ="subject:"+smsSubject+":"+smsContent[0:index]
                        flag =itchat.send(subContent, toUserName=userName)
                        flag =itchat.send_image(imageName, toUserName=userName)
                    else:
                        #不是短信
                        smsSubject =df.iloc[[j]].smsSubject[0]
                        subContent ="subject:"+smsSubject+":"+smsContent
                        flag =itchat.send(subContent, toUserName=userName)
                #更新数据表的发送标志
                if(flag['BaseResponse']['Ret']==0):
                    dbOper.read_sql_query("update spcard.sms_send set smsState =2 where smsContent='%s' and smsType=%s and smsSubject ='%s'"%(smsContent,smsType,smsSubject))
                time.sleep(2)
                break
            break

if __name__ == '__main__':
    test =WxSms()
    test.login()
    test.sendLoop()
    # hotReload(热加载),短时间内不需要再次扫码登陆
    # itchat.auto_login(hotReload=True)
    
    # # 获取微信好友的信息,返回的是json格式的信息
    # friends = itchat.get_friends(update=True)[0:]
    # for i in friends[0:]:
    #     sex = i['NickName']
    #     if(sex == '安士霞'):
    #         userName = i['UserName']
    #         break

    # # itchat.send('Hello, 文件助手', toUserName='filehelper')#send_image
    # # itchat.send_image('./hello.png', toUserName='filehelper')
    # flag =itchat.send('Hello, 文件助手', toUserName=userName)#send_image success
    # print(flag)
    # itchat.send_image('./hello.png', toUserName=userName)
    # print(flag)
    # 连接mysql数据库

 
