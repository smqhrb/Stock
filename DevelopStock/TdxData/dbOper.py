
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
