# https://www.jb51.net/article/121076.htm
import time
import itchat
import pymysql
import os
import random
import pandas as pd
import datetime
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
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
    def select_df(self,sel):
        df =pd.DataFrame()
        try:
            cursor = self.db.cursor()
            cursor.execute(sel)
            #data =cursor.fetchone()
            data =cursor.fetchall()
            columnDes = cursor.description #获取连接对象的描述信息
            columnNames = [columnDes[i][0] for i in range(len(columnDes))]
            df = pd.DataFrame([list(i) for i in data],columns=columnNames)            
            cursor.close()
        except:
            print("except "+sel)
            data =""
        return df
# def get_df_from_db(sql):
#     cursor = connection.cursor()
#     cursor.execute(sql)
#     data = cursor.fetchall()
#     columnDes = cursor.description #获取连接对象的描述信息
#     columnNames = [columnDes[i][0] for i in range(len(columnDes))]
#     df = pd.DataFrame([list(i) for i in data],columns=columnNames)
#     return df

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

class WxSms(QThread):
    signal = pyqtSignal(str,str)
    def login(self):
        pass
    def EmitMsgToUi(self,lx,msg):
        '''
        向界面发送信息
        '''
        self.signal.emit(lx,msg)
    def __init__(self):
        '''
        runCntl: 1 -run,0 -stop
        '''
        super(WxSms,self).__init__()
        self.EnableExport =False
        self.EnableCheckIP =False
        self.runCntl =1
        self.checkIp ={}
    def run(self):
        self.runCntl =1
    def stop(self):
        self.runCntl =0



    def CheckMachine(self,dbOper,delay):
        '''
        dbOper : db operation
        delay  : check ip feedback delay time (min)
        '''
        now_time = datetime.datetime.now()
        dayL =now_time.strftime('%Y-%m-%d')
        dateL =now_time.strftime('%Y-%m-%d %H:%M:%S')
        # timeL =now_time.strftime('%H:%i:%s')
        # TIMESTAMPDIFF
        sql_machine ="select TIMESTAMPDIFF(MINUTE, max(cap_time),STR_TO_DATE(%s,'%%Y-%%m-%%d %%H:%%i:%%s')) as delay,clientIP from capture_pic where  date_format(cap_time,'%%Y-%%m-%%d') ='%s' and clientIP in (select clientIP from userlogin)"%(dateL,dayL)
        res =dbOper.select_df(sql_machine)
        len_res =len(res)
        ret_df =pd.DataFrame()
        if(len_res>0):
            ret_df = res[res['delay']>delay]
        return ret_df

        # 'select datediff(max(cap_time),STR_TO_DATE(%s,"%Y-%m-%d %H:%i:%s")),clientIP from capture_pic where date_format(cap_time,'%Y-%m-%d') ='%s' and clientIP in (select clientIP from userlogin)'%(dateL,dayL)
    def sendIp(self,wxChat,df_msgIp):
        '''
        '''
        if(self.EnableCheckIP ==False):
            self.EmitMsgToUi("","运行计算机 检测  退出")
            time.sleep(30)
            return
        UserName ="filehelper"
        len_df = len(df_msgIp)
        for j in range(len_df):
            time.sleep(3)
            Ip =df_msgIp['clientIp'][j]
            msgIp ="please check computer IP:"+Ip
            if(self.checkIp.has_key(Ip)):
                self.checkIp[Ip] = self.checkIp[Ip] -1
                if(self.checkIp[Ip]<=0):
                    flag =wxChat.send(msgIp, toUserName=UserName)
                    self.EmitMsgToUi("IP","接收对象(微信 %s):%s"%(UserName,msgIp))
                    if(flag['BaseResponse']['Ret']==0):
                        self.checkIp[Ip] = 5
            else:
                flag =wxChat.send(msgIp, toUserName=UserName)
                self.EmitMsgToUi("IP","接收对象(微信 %s):%s"%(UserName,msgIp))
                if(flag['BaseResponse']['Ret']==0):
                    self.checkIp[Ip] = 5
    
    def IsWorkDay(self):
        today =datetime.datetime.now().weekday()
        
        if(today<=5 and today>=1):
            return True
        else:
            return False
    def time_in_range(self,timeStart,timeEnd):
        now_time =datetime.datetime.now()
        str_day =now_time.strftime("%Y-%m-%d")
        st =str_day+" "+timeStart
        start_time =datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
        st =str_day+" "+timeEnd
        end_time =datetime.datetime.strptime(st, "%Y-%m-%d %H:%M:%S")
        # now_str_time =time.strftime("%H:%M:%S", now_time)
        if((now_time>start_time) and (now_time<end_time)):
            return True
        else:
            return False

    def CheckTime(self,timeStart,timeEnd):
        flag =True
        if(self.time_in_range(timeStart,timeEnd)==False):
            flag =False
            self.EmitMsgToUi("","不在时间区间内")

        if(self.IsWorkDay()):
            pass
        else:
            self.EmitMsgToUi("","不是工作日")
            flag =False
            
    def exportDataFromDB(self,timeStart,timeEnd,day):
        '''
        export data to file, date =day.
        '''
        dbOper =dbOperate()
        dbOper.connectDb()
        while(True):
            if(self.EnableExport ==False):
                self.EmitMsgToUi("","导出数据到xls 退出")
                break
            if(self.CheckTime(timeStart,timeEnd)==True):
                pass
            else:

                time.sleep(30)
                continue
            res =dbOper.select_df("select code,type,fname,jz_num,jz_pos,lz_num,lz_pos,md_num,md_pos,mc_num,mc_pos,bm_num,bm_pos,cap_time,orderPiont,flag,clientIP,count_JL,count_MJL from capture_pic where cap_time = %s"%day)
            # write to xls
            destPath ="export"
            if os.path.exists(destPath):                     #检测路径是否存在,不存在则创建路径
                pass
            else:
                os.mkdir(destPath)
             
            pathName ="%s/%s.xls"%(destPath,day)
            write = pd.ExcelWriter(pathName)
            # ========== 
            res.to_excel(write,sheet_name=day,index=True)
            write.save()
            time.sleep(5*60)# 5 min
        dbOper.closeDb()

    def sendLoop(self,timeStart,timeEnd,timeSpan):
        '''
        给自己发只能用'filehelper'-文件传输助手
        '''
        itchat.auto_login(hotReload=True)
        userNameList =[]
        msgToSelf ="filehelper"# 发送给自己
        if(os.path.exists("WeList.xls")):
            # WeList.xls exsit
            # read WeList.xls
            df =pd.read_excel("WeList.xls")
        else:
             # not exist
            df =pd.DataFrame([msgToSelf],columns=['NickName'])
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
            if(nikeNameList[i]==msgToSelf):
                userNameList.append(msgToSelf)
            else:
                users = itchat.search_friends(name=nikeNameList[i])
                if(len(users)>0):
                    userNameList.append(users[0]['UserName'])
                else:
                    print("接收对象(微信 %s)没有对应的UserName")
                    self.EmitMsgToUi("","接收对象(微信 %s)没有对应的"%UserName)
        if(len(userNameList)<=0):
            print("接收对象(微信 昵称)不存在")
            return

        #发送信息 每隔两秒发一个
        # dbOper = mysqlDB()
        dbOper =dbOperate()
        dbOper.connectDb()
        print("程序正在运行,退出 Ctrl+C")
        self.EmitMsgToUi("","消息发送开始")
        self.runCntl =1
        while(1):
            #从短信表中读取记录
            if (self.runCntl ==0):
                self.EmitMsgToUi("","结束消息发送")
                break
            if(self.CheckTime(timeStart,timeEnd)==True):
                ret_df =self.CheckMachine(dbOper,timeSpan)
            else:
                ret_df =pd.DataFrame()
                time.sleep(30)
                continue
            #
            self.sendIp(itchat,ret_df)

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
                    subContent =""
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
                        #是短信
                        userName =userNameList[i]
                        subContent ="subject:"+smsSubject+":"+smsContent
                        flag =itchat.send(subContent, toUserName=userName)
                    self.EmitMsgToUi("","接收对象(微信 %s):%s"%(userName,subContent))
                    delayMs =random.random()#0~1秒之间随机延时
                    time.sleep(delayMs)
                #更新数据表的发送标志
                if(flag['BaseResponse']['Ret']==0):
                    dbOper.updateInsertDelete("update spcard.sms_send set smsState =2 where smsContent='%s' and smsType=%s and smsSubject ='%s'"%(smsContentConv,smsType,smsSubject))
                delaySecond =random.randint(3, 6)#3~6秒之间随机延时
                time.sleep(delaySecond)

if __name__ == '__main__':
    mainProc =WxSms()
    mainProc.time_in_range("09:07:00","10:07:00")
    # mainProc.login()
    # mainProc.sendLoop()
    # mainProc.CheckMachine(5)


 
