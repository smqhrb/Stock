
import pandas as pd
from sqlalchemy import create_engine
class mysqlDB:
    def __init__(self):
        self.userName ='root'
        self.passWord ='1234'
        self.IP ='127.0.0.1'
        self.Port ='3306'
        self.dbName ='zj'
        
        self.engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s'%(self.userName,self.passWord,self.IP,self.Port,self.dbName))
        self.con = self.engine.connect()
    def read_sql_query(self,sql):
        df = pd.read_sql_query(sql, self.engine)
        return df

    def to_sql(self,dataf,tbl):
        try: 
            dataf.to_sql(name =tbl,  con=self.con, if_exists='append',index= False)#name='rumousdata', con=con, if_exists='append', index=False
        except Exception as e:
            print('Error is ' + str(e))
            #self.con.rollback()        
