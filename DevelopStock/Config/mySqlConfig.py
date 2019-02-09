import sys
import pymysql
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
        self.gDbPass ="smq1234"
        self.gDbName ="stockdb"
    
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
        except:
            print("except "+sel)
            data =""
        return data

    def updateInsertDelete(self,updateSentence):
        try:
            cursor = self.db.cursor()
            cursor.execute(updateSentence)
        except:
            
            print("except "+updateSentence)
            #self.db.rollback()

    def commit(self):
        self.db.commit()    

    def closeDb(self):
        self.db.close()

if __name__ == '__main__':
    dbExe =dbOperate()
    dbExe.connectDb()
    data = dbExe.select("select version()")
    print ("Database version : %s " % data)
    dbExe.closeDb()

# # 打开数据库连接
# db = pymysql.connect(DBIP,DBUSER,DBPASS,DBNAME )
# # 使用 cursor() 方法创建一个游标对象 cursor
# cursor = db.cursor()
# # 使用 execute()  方法执行 SQL 查询 
# cursor.execute("select * from gupiao")
# # 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()
# print ("Database version : %s " % data)
#  # 关闭数据库连接
# db.close()