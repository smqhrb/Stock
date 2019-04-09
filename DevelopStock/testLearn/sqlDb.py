# https://www.jb51.net/article/49789.htm
# https://www.jianshu.com/p/238a13995b2b
# https://blog.csdn.net/lzw2016/article/details/84720433
# 导入必要模块
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CONNECT_STRING = 'mysql+pymysql://root:1234@localhost:3306/zj'#'mysql+mysqldb://root:1234@localhost/zj?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=True)
DB_Session = sessionmaker(bind=engine)
session = DB_Session()
# session.execute('create database abc')
# print session.execute('show databases').fetchall()
# session.execute('use abc')
# # 建 user 表的过程略
# print session.execute('select * from user where id = 1').first()
# print session.execute('select * from user where id = :id', {'id': 1}).first()


from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
BaseModel = declarative_base()#declarative_base() 创建了一个 BaseModel 类，这个类的子类可以自动与一个表关联。

def init_db():
    BaseModel.metadata.create_all(engine)

def drop_db():
    BaseModel.metadata.drop_all(engine)

# 以 User 类为例，它的 __tablename__ 属性就是数据库中该表的名称，
# 它有 id 和 name 这两个字段，分别为整型和 30 个定长字符。Column 还有一些其他的参数，我就不解释了。
class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(CHAR(30)) # or Column(String(30))
df =pd.DataFrame()
df ={'a':1,"b":2}
init_db()

user = User(id=1, name='ooxx')
session.merge(user)
session.commit()

# df =pd.DataFrame([{'name': `randint(1, 100)`,'age': randint(1, 100)} for i in xrange(10000)])
session.execute(
    User.__table__.insert(),
    [{'name': `randint(1, 100)`,'age': randint(1, 100)} for i in xrange(10000)]
)
session.commit()
# from sqlalchemy import func, or_, not_

# user = User(name='a')
# session.add(user)
# user = User(name='b')
# session.add(user)
# user = User(name='a')
# session.add(user)
# user = User()
# session.add(user)
# session.commit()

# query = session.query(User)
# print (query) # 显示SQL 语句
# print query.statement # 同上
# for user in query: # 遍历时查询
#     print user.name
# print query.all() # 返回的是一个类似列表的对象
# print query.first().name # 记录不存在时，first() 会返回 None
# # print query.one().name # 不存在，或有多行记录时会抛出异常
# print query.filter(User.id == 2).first().name
# print query.get(2).name # 以主键获取，等效于上句
# print query.filter('id = 2').first().name # 支持字符串

# query2 = session.query(User.name)
# print query2.all() # 每行是个元组
# print query2.limit(1).all() # 最多返回 1 条记录
# print query2.offset(1).all() # 从第 2 条记录开始返回
# print query2.order_by(User.name).all()
# print query2.order_by('name').all()
# print query2.order_by(User.name.desc()).all()
# print query2.order_by('name desc').all()
# print session.query(User.id).order_by(User.name.desc(), User.id).all()

# print query2.filter(User.id == 1).scalar() # 如果有记录，返回第一条记录的第一个元素
# print session.query('id').select_from(User).filter('id = 1').scalar()
# print query2.filter(User.id > 1, User.name != 'a').scalar() # and
# query3 = query2.filter(User.id > 1) # 多次拼接的 filter 也是 and
# query3 = query3.filter(User.name != 'a')
# print query3.scalar()
# print query2.filter(or_(User.id == 1, User.id == 2)).all() # or
# print query2.filter(User.id.in_((1, 2))).all() # in

# query4 = session.query(User.id)
# print query4.filter(User.name == None).scalar()
# print query4.filter('name is null').scalar()
# print query4.filter(not_(User.name == None)).all() # not
# print query4.filter(User.name != None).all()

# print query4.count()
# print session.query(func.count('*')).select_from(User).scalar()
# print session.query(func.count('1')).select_from(User).scalar()
# print session.query(func.count(User.id)).scalar()
# print session.query(func.count('*')).filter(User.id > 0).scalar() # filter() 中包含 User，因此不需要指定表
# print session.query(func.count('*')).filter(User.name == 'a').limit(1).scalar() == 1 # 可以用 limit() 限制 count() 的返回数
# print session.query(func.sum(User.id)).scalar()
# print session.query(func.now()).scalar() # func 后可以跟任意函数名，只要该数据库支持
# print session.query(func.current_timestamp()).scalar()
# print session.query(func.md5(User.name)).filter(User.id == 1).scalar()

# query.filter(User.id == 1).update({User.name: 'c'})
# user = query.get(1)
# print user.name

# user.name = 'd'
# session.flush() # 写数据库，但并不提交
# print query.get(1).name

# session.delete(user)
# session.flush()
# print query.get(1)

# session.rollback()
# print query.get(1).name
# query.filter(User.id == 1).delete()
# session.commit()
# print query.get(1)



#    pd.io.sql.to_sql(df,table_name,con=conn,schema='w_analysis',if_exists='append')
    # def updateDayData(self,df):
    #     # replace into tableName(ziduan,,,,) values(,,,,)
    #      "replace into data_k(code, date, open, high, low, close, amount,volume, DIF, DEA, MACD,MA_5, MA_10,  MA_20, MA_31,  MA_60,"
    #                        " MA_120,Glue20_31_60,Glue31_60_120,Slope_M5,Slope_M10,Slope_M20,Slope_M31,Slope_M60, Slope_M120, BOLL,UB, LB) values("+")"
    #     try:
    #         cursor.execute(insert_sql,
    #                     (rounds, date_time, home_team, home_team_goal, home_team_goal_lost, home_ranking, score,
    #                         guest_team, guest_team_goal, guest_team_goal_lost, guest_ranking, court_all, court_half,
    #                         court_all_size, court_half_size, score_half))
    #         db.commit()
    #     except Exception as e:
    #         print('Error is ' + str(e))
    #         db.rollback()        

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

# #very fast 
# import cStringIO
 
# output = cStringIO.StringIO()
# # ignore the index
# df_a.to_csv(output, sep='\t',index = False, header = False)
# output.getvalue()
# # jump to start of stream
# output.seek(0)
 
# connection = engine.raw_connection() #engine 是 from sqlalchemy import create_engine
# cursor = connection.cursor()
# # null value become ''
# cursor.copy_from(output,table_name,null='')
# connection.commit()

#NULL ->None
# {'a' : [test,test,test], 'b' : [sun,sun,sun], 'c' : [red,red,red]}
# 这样的字典，只要下面一句话：
# {col:df[col].tolist() for col in df.columns} 
# INSERT INTO data_k (date, open, high, low, close, amount, volume, `DIF`, `DEA`, `MACD`, `MA_5`, `MA_10`, `MA_20`, `MA_31`, `MA_60`, `MA_120`, `Glue20-31-60`, `Glue20_31_60`, `Glue31_60_120`, `Slope_M5`, `Slope_M10`, `Slope_M20`, `Slope_M31`, `Slope_M60`, `Slope_M120`, `BOLL`, `UB`, `LB`) VALUES (%(date)s, %(open)s, %(high)s, %(low)s, %(close)s, %(amount)s, %(volume)s, %(DIF)s, %(DEA)s, %(MACD)s, %(MA_5)s, %(MA_10)s, %(MA_20)s, %(MA_31)s, %(MA_60)s, %(MA_120)s, %(Glue20-31-60)s, %(Glue20_31_60)s, %(Glue31_60_120)s, %(Slope_M5)s, %(Slope_M10)s, %(Slope_M20)s, %(Slope_M31)s, %(Slope_M60)s, %(Slope_M120)s, %(BOLL)s, %(UB)s, %(LB)s)]
# [parameters: (
# {'low': 6.71, 'LB': None, 'amount': 17261867.2, 'DEA': 0.0, 'volume': 25366281, 'Slope_M120': None, 'MA_20': None, 'Slope_M20': None, 'Slope_M5': None, 'MA_5': None, 'MA_120': None, 'Slope_M31': None, 'Glue20-31-60': 0, 'Slope_M60': None, 'close': 6.86, 'MACD': 0.0, 'open': 6.75, 'date': '2014-09-02', 'MA_31': None, 'BOLL': None, 'high': 6.91, 'Slope_M10': None, 'Glue31_60_120': None, 'MA_60': None, 'Glue20_31_60': None, 'DIF': 0.0, 'UB': None, 'MA_10': None}, 
# {'low': 6.76, 'LB': None, 'amount': 16510476.8, 'DEA': 0.0003739316239315116, 'volume': 24071574, 'Slope_M120': None, 'MA_20': None, 'Slope_M20': None, 'Slope_M5': None, 'MA_5': None, 'MA_120': None, 'Slope_M31': None, 'Glue20-31-60': 0, 'Slope_M60':None, 'close': 6.89, 'MACD': 0.0005982905982904185, 'open': 6.9, 'date': '2014-09-03', 'MA_31': None, 'BOLL': None, 'high': 6.94, 'Slope_M10': None, 'Glue31_60_120': None, 'MA_60': None, 'Glue20_31_60': None, 'DIF': 0.0006730769230767208, 'UB': None, 'MA_10': None}, 
# {'low': 6.91, 'LB': None, 'amount': 28772476.8, 'DEA': 0.003113968511483159, 'volume': 40897690, 'Slope_M120': None, 'MA_20': None, 'Slope_M20': None, 'Slope_M5': None, 'MA_5': None, 'MA_120': None, 'Slope_M31': None, 'Glue20-31-60': 0, 'Slope_M60': None, 'close': 7.09, 'MACD': 0.007891306236148747, 'open': 7.04, 'date': '2014-09-04', 'MA_31': None, 'BOLL': None, 'high': 7.17, 'Slope_M10': None, 'Glue31_60_120': None, 'MA_60': None, 'Glue20_31_60': None, 'DIF': 0.007059621629557533, 'UB': None, 'MA_10': None},
# {'low': 6.9, 'LB': None, 'amount': 24865852.8, 'DEA': 0.006599004879848342, 'volume': 35077814, 'Slope_M120': None, 'MA_20': None, 'Slope_M20': None, 'Slope_M5': None, 'MA_5': None, 'MA_120': None, 'Slope_M31': None, 'Glue20-31-60': 0, 'Slope_M60': None, 'close': 7.19, 'MACD': 0.01360558198209768, 'open': 7.09, 'date': '2014-09-05', 'MA_31': None, 'BOLL': None, 'high': 7.27, 'Slope_M10': None, 'Glue31_60_120': None, 'MA_60': None, 'Glue20_31_60': None, 'DIF': 0.013401795870897182, 'UB': None, 'MA_10': None},
# {'low': 7.09, 'LB': None, 'amount': 29425145.6, 'DEA': 0.010274168539312917, 'volume': 40509649, 'Slope_M120': None, 'MA_20': None, 'Slope_M20': None, 'Slope_M5':None, 'MA_5': 7.056, 'MA_120': None, 'Slope_M31': None, 'Glue20-31-60': 0, 'Slope_M60': None, 'close': 7.25, 'MACD': 0.01735853299638309, 'open':7.35, 'date': '2014-09-09', 'MA_31': None, 'BOLL': None, 'high': 7.43, 'Slope_M10': None, 'Glue31_60_120': None, 'MA_60': None, 'Glue20_31_60': None, 'DIF': 0.018953435037504462, 'UB': None, 'MA_10': None})]
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