# https://www.jb51.net/article/121076.htm
import time
import itchat
import pymysql
import random
#DBIP ="localhost"
#DBUSER ="root"
#DBPASS ="smq1234"
#DBNAME ="stockdb"
class dbOperate:
    '''
    configure DBIP,DBUser,DBPass,DBName
    '''
#    gDbIP ="localhost"
#    gDbUser ="root"
#    gDbPass ="smq1234"
#    gDbName ="stockdb"
    def __init__(self):
        self.gDbIP ="localhost"
        self.gDbUser ="root"
        self.gDbPass ="1234"
        self.gDbName ="zj"
    
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
        userNameList =['']
        # userNameList.append(userName)

        lenList =len(nikeNameList)
        for i in range(lenList):
            for friend in friends[1:]:
                nickName = friend['NickName']
                if(nickName == nikeNameList[i]):
                    userName =friend['UserName']
                    userNameList.append(userName)
                    break

        userNameList.clear()
        userNameList.append('filehelper')
            # users = itchat.search_friends(name=nikeNameList[i])
            # userNameList.append(users[0]['UserName'])

        #发送信息 每隔两秒发一个
        # dbOper = mysqlDB()
        dbOper =dbOperate()
        dbOper.connectDb()

        while(1):
            #从短信表中读取记录
            # df =dbOper.read_sql_query("select smsSubject,smsContent,smsType from spcard.sms_send where smsState = 0")
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
                        imageName =smsContent[index+4:]
                        print(imageName)
                        #imageName ='./hello.png'
                        userName =userNameList[i]
                        
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
                delaySecond =random.randint(3, 6)
                print(delaySecond)
                time.sleep(delaySecond)
                
            

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

 
