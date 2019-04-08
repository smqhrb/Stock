# https://www.jianshu.com/p/238a13995b2b
# https://blog.csdn.net/lzw2016/article/details/84720433
# 导入必要模块
import pandas as pd
from sqlalchemy import create_engine

# # 初始化数据库连接，使用pymysql模块
# # MySQL的用户：root, 密码:147369, 端口：3306,数据库：mydb
# engine = create_engine('mysql+pymysql://root:147369@localhost:3306/mydb')

# # 查询语句，选出employee表中的所有数据
# sql = '''
#       select * from employee;
#       '''

# # read_sql_query的两个参数: sql语句， 数据库连接
# df = pd.read_sql_query(sql, engine)

# # 输出employee表的查询结果
# print(df)

# # 新建pandas中的DataFrame, 只有id,num两列
# df = pd.DataFrame({'id':[1,2,3,4],'num':[12,34,56,89]})

# # 将新建的DataFrame储存为MySQL中的数据表，不储存index列
# df.to_sql('mydf', engine, index= False)

# print('Read from and write to Mysql table successfully!')

class mysqlDB:
    def __init__(self):
        self.userName ='root'
        self.passWord ='1234'
        self.IP ='127.0.0.1'
        self.Port ='3306'
        self.dbName ='zj'
        self.engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s'%(self.userName,self.passWord,self.IP,self.Port,self.dbName))
    def read_sql_query(self,sql):
        df = pd.read_sql_query(sql, self.engine)
        return df

    def to_sql(self,dataf,tbl):
        dataf.to_sql(tbl, self.engine, index= False)
###########
#避免写入重复数据
# replace into tableName(ziduan,,,,) values(,,,,)
# insert ignore into tablename(ziduan,,,,,) values(,,,,,)
    # def insert_date(self, rounds, date_time, home_team, home_team_goal, home_team_goal_lost, home_ranking, score,
    #                     guest_team, guest_team_goal, guest_team_goal_lost, guest_ranking, court_all, court_half,
    #                     court_all_size, court_half_size, score_half):
    #         db = pymysql.connect(host=self.host, user=self.user, password=self.passwd, port=self.port, db=self.db)
    #         cursor = db.cursor()
    #         insert_sql = """
    #                             insert into racing_ball(rounds, time, home_team, home_team_goal, home_team_goal_lost, 
    #                             home_ranking, score,guest_team, guest_team_goal, guest_team_goal_lost, guest_ranking,
    #                                 court_all,court_half,court_all_size,court_half_size,score_half
    #                             )
    #                             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #                             ON DUPLICATE KEY UPDATE home_team_goal=VALUES(home_team_goal),
    #                             home_team_goal_lost=VALUES(home_team_goal_lost), home_ranking=VALUES(home_ranking),
    #                             score=VALUES(score), guest_team_goal=VALUES(guest_team_goal),
    #                             guest_team_goal_lost=VALUES(guest_team_goal_lost), guest_ranking=VALUES(guest_ranking),
    #                             score_half=VALUES(score_half)
    #                         """
    #         try:
    #             cursor.execute(insert_sql,
    #                         (rounds, date_time, home_team, home_team_goal, home_team_goal_lost, home_ranking, score,
    #                             guest_team, guest_team_goal, guest_team_goal_lost, guest_ranking, court_all, court_half,
    #                             court_all_size, court_half_size, score_half))
    #             db.commit()
    #         except Exception as e:
    #             print('Error is ' + str(e))
    #             db.rollback()
    #         db.close()

# # 打开数据库连接
# db = pymysql.connect("localhost","testuser","test123","TESTDB" )
  
# # 使用cursor()方法获取操作游标
# cursor = db.cursor()
  
# # SQL 插入语句
# sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
#  LAST_NAME, AGE, SEX, INCOME)
#  VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
# try:
#  # 执行sql语句
#  cursor.execute(sql)
#  # 提交到数据库执行
#  db.commit()
# except:
#  # 如果发生错误则回滚
#  db.rollback()
  
# # 关闭数据库连接
# db.close()
