# https://www.jb51.net/article/121076.htm
import time
import itchat
import pymysql
import os
import random
import pandas as pd

class dbOperate:
    '''
    configure DBIP,DBUser,DBPass,DBName
    '''
#    gDbIP ="localhost"
#    gDbUser ="root"
#    gDbPass ="smq1234"
#    gDbName ="stockdb"
    def __init__(self):
        self.gDbIP ="localhost"#数据库的IP
        self.gDbUser ="root"#数据库连接用户名
        self.gDbPass ="1234"#数据库连接密码
        self.gDbName ="zj"#数据库的库名称
    
    def setDbConInfo(self,dbIP,dbUser,dbPass,dbName):#set db connect information
        self.gDbIP =dbIP
        self.gDbUser =dbUser
        self.gDbPass =dbPass
        self.gDbName =dbName

    def connectDb(self):
        self.db =pymysql.connect(self.gDbIP,self.gDbUser,self.gDbPass,self.gDbName )

    def select(self,sel):
        try:
            cursor = self.db.cursor()
            cursor.execute(sel)
            #data =cursor.fetchone()
            data =cursor.fetchall()
            cursor.close()
        except:
            print("except "+sel)
            data =""
        return data

    def updateInsertDelete(self,updateSentence):
        try:
            cursor = self.db.cursor()
            row =cursor.execute(updateSentence)
            self.db.commit()
            cursor.close()
            
        except:
            
            print("except "+updateSentence)
            self.db.rollback()

    def commit(self):
        self.db.commit()    

    def closeDb(self):
        self.db.close()

class WxSms:
    def login(self):
        pass

    def sendLoop(self):
        '''
        给自己发只能用'fileHelper'-文件传输助手
        '''
        itchat.auto_login(hotReload=True)
        userNameList =[]
        
        if(os.path.exists("WeList.xls")):
            # WeList.xls exsit
            # read WeList.xls
            df =pd.read_excel("WeList.xls")
        else:
             # not exist
            df =pd.DataFrame(['fileHelper'],columns=['NickName'])
            df.to_excel('WeList.xls')

        nikeNameList =df['NickName'].tolist()    
        
       
        lenList =len(nikeNameList)
        # friends = itchat.get_friends(update=True)[0:]
        for i in range(lenList):
            # for friend in friends[1:]:
            #     nickName = friend['NickName']
            #     if(nickName == nikeNameList[i]):
            #         userName =friend['UserName']
            #         userNameList.append(userName)
            #         break
            if(nikeNameList[i]=='fileHelper'):
                userNameList.append('fileHelper')
            else:
                users = itchat.search_friends(name=nikeNameList[i])
                if(len(users)>0):
                    userNameList.append(users[0]['UserName'])
                else:
                    print("接收对象(微信 %s)没有对应的UserName")
        if(len(userNameList)<=0):
            print("接收对象(微信 昵称)不存在")
            return

        #发送信息 每隔两秒发一个
        # dbOper = mysqlDB()
        dbOper =dbOperate()
        dbOper.connectDb()

        while(1):
            #从短信表中读取记录
             res =dbOper.select("select smsSubject,smsContent,smsType from spcard.sms_send where smsState = 0")
            lenDf =len(res)
            smsTypeCol=2
            smsContentCol=1
            smsSubjectCol =0
            for j in range(lenDf):
                #判断是否是彩信

                smsType =res[j][smsTypeCol]
                smsContent =res[j][smsContentCol]
                smsContentConv =pymysql.escape_string(smsContent)
                smsSubject =res[j][smsSubjectCol]
                lenList =len(userNameList)
                for i in range(lenList):
                    if(smsType ==1):
                        #是彩信
                        index =smsContent.find('####',0,len(smsContent))
                        imageName =smsContent[index+4:]#图片文件路径名
                        userName =userNameList[i]
                        #
                        subContent ="subject:"+smsSubject+":"+smsContent[0:index]
                        flag =itchat.send(subContent, toUserName=userName)
                        flag =itchat.send_image(imageName, toUserName=userName)

                    else:
                        #不是短信
                        subContent ="subject:"+smsSubject+":"+smsContent
                        flag =itchat.send(subContent, toUserName=userName)
                #更新数据表的发送标志
                if(flag['BaseResponse']['Ret']==0):
                    dbOper.updateInsertDelete("update spcard.sms_send set smsState =2 where smsContent='%s' and smsType=%s and smsSubject ='%s'"%(smsContentConv,smsType,smsSubject))
                delaySecond =random.randint(3, 6)#3~6秒之间随机延时
                print(delaySecond)
                time.sleep(delaySecond)

if __name__ == '__main__':
    mainProc =WxSms()
    mainProc.login()
    mainProc.sendLoop()

 
