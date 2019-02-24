# class Person(object):   # 定义一个父类
#    def talk(self):    # 父类中的方法
#         print("person is talking.")   
# class Chinese(Person):    # 定义一个子类， 继承Person类
#     def walk(self):      # 在子类中定义其自身的方法
#         print('is walking')
# c = Chinese()
# c.talk()      # 调用继承的Person类的方法
# c.walk()     # 调用本身的方法
####################
# ## 构造函数的继承
# class Person(object):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.weight = 'weight'
#     def talk(self):
#         print("person is talking.")

# class Chinese(Person):
#     def __init__(self, name, age, language):  # 先继承，在重构
#         Person.__init__(self, name, age)  #继承父类的构造方法，也可以写成：super(Chinese,self).__init__(name,age)
#         self.language = language    # 定义类的本身属性

#     def walk(self):
#         print('is walking')
# class American(Person):
#     pass

# c = Chinese('bigberg', 22, 'Chinese')

#### 子类对父类方法的重写
# class Person(object):
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age
#         self.weight = 'weight'

#     def talk(self):
#         print("person is talking.")

# class Chinese(Person):
#     def __init__(self, name, age, language):  
#         Person.__init__(self, name, age)  
#         self.language = language
#         print(self.name, self.age, self.weight, self.language)

#     def talk(self):  # 子类 重构方法
#         print('%s is speaking chinese' % self.name)

#     def walk(self):
#         print('is walking')

# c = Chinese('bigberg', 22, 'Chinese')
# c.talk()

### 类继承的事例
# class SchoolMember(object):
#     '''学习成员基类'''
#     member = 0
#     def __init__(self, name, age, sex):
#         self.name = name
#         self.age = age
#         self.sex = sex
#         self.enroll()

#     def enroll(self):
#         '注册'
#         print('just enrolled a new school member [%s].' % self.name)
#         SchoolMember.member += 1

#     def tell(self):
#         print('----%s----' % self.name)
#         for k, v in self.__dict__.items():
#             print(k, v)
#         print('----end-----')
#     def __del__(self):
#         print('开除了[%s]' % self.name)
#         SchoolMember.member -= 1

# class Teacher(SchoolMember):
#     '教师'
#     def __init__(self, name, age, sex, salary, course):
#         SchoolMember.__init__(self, name, age, sex)
#         self.salary = salary
#         self.course = course

#     def teaching(self):
#         print('Teacher [%s] is teaching [%s]' % (self.name, self.course))

# class Student(SchoolMember):
#     '学生'
#     def __init__(self, name, age, sex, course, tuition):
#         SchoolMember.__init__(self, name, age, sex)
#         self.course = course
#         self.tuition = tuition
#         self.amount = 0

#     def pay_tuition(self, amount):
#         print('student [%s] has just paied [%s]' % (self.name, amount))
#         self.amount += amount

# t1 = Teacher('Wusir', 28, 'M', 3000, 'python')
# t1.tell()
# s1 = Student('haitao', 38, 'M', 'python', 30000)
# s1.tell()
# s2 = Student('lichuang', 12, 'M', 'python', 11000)
# print(SchoolMember.member)
# del s2
# print(SchoolMember.member)

###可以把属性的名称前加上两个下划线__，
# 在Python中，实例的变量名如果以__开头，
# 就变成了一个私有变量（private），只有内部可以访问，外部不能访问，

#判断class的类型，可以使用isinstance()函数#


# 但是，如果我们想要限制class的属性怎么办？比如，只允许对Student实例添加name和age属性。
# 为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class能添加的属性：
# class Student(object):
#      __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称
###########
# 有没有既能检查参数，又可以用类似属性这样简单的方式来访问类的变量呢？
# 对于追求完美的Python程序员来说，这是必须要做到的！
# 还记得装饰器（decorator）可以给函数动态加上功能吗？对于类的方法，装饰器一样起作用。
# Python内置的@property装饰器就是负责把一个方法变成属性调用的：
# class Student(object):

#     @property
#     def score(self):
#         return self._score

#     @score.setter
#     def score(self, value):
#         if not isinstance(value, int):
#             raise ValueError('score must be an integer!')
#         if value < 0 or value > 100:
#             raise ValueError('score must between 0 ~ 100!')
#         self._score = value
# s = Student()
# s.score = 60 # OK，实际转化为s.set_score(60)
# print(s.score )# OK，实际转化为s.get_score()
# s.score = 9999

# # 多重继承
# class Dog(Mammal, Runnable):
#     pass

# 看到类似__slots__这种形如__xxx__的变量或者函数名就要注意，这些在Python中是有特殊用途的
# __len__()方法我们也知道是为了能让class作用于len()函数。
# __str__  打印一个实例：

# class Student(object):
#     def __init__(self, name):
#         self.name = name
#     def __str__(self):
#         return 'Student object (name: %s)' % self.name


# print (Student('Michael'))
# >>> s = Student('Michael')
# >>> s
# <__main__.Student object at 0x109afb310>

# 这是因为直接显示变量调用的不是__str__()，而是__repr__()，
# 两者的区别是__str__()返回用户看到的字符串，而__repr__()返回程序开发者看到的字符串，
# 也就是说，__repr__()是为调试服务的。

# __iter__
# 如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，
# 该方法返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的next()方法拿到循环的下一个值，
# 直到遇到StopIteration错误时退出循环。
# class Fib(object):
#     def __init__(self):
#         self.a,self.b = 0,1 # 初始化两个计数器a，b


#     def __next__(self):
#         self.a, self.b = self.b, self.a + self.b # 计算下一个值
#         if self.a > 100000: # 退出循环的条件
#             raise StopIteration
#         return self.a # 返回下一个值

#     def __iter__(self):
#         return self # 实例本身就是迭代对象，故返回自己

#     def __getitem__(self, n):
#         # a, b = 1, 1
#         # for x in range(n):
#         #     a, b = b, a + b
#         # return a
#         if isinstance(n, int):
#             a, b = 1, 1
#             for x in range(n):
#                 a, b = b, a + b
#             return a
#         if isinstance(n, slice):
#             # 对于Fib却报错。原因是__getitem__()传入的参数可能是一个int，也可能是一个切片对象slice，所以要做判断
#             start = n.start
#             stop = n.stop
#             a, b = 1, 1
#             L = []
#             for x in range(stop):
#                 if x >= start:
#                     L.append(a)
#                 a, b = b, a + b
#             return L
# for n in Fib():
#     print( n)
# # 要表现得像list那样按照下标取出元素，需要实现__getitem__()方法：
# f = Fib()
# print(f[2])
# print(f[3])
# f1 = Fib()
# print(f1[0:5])

# ############
# class Chain(object):
#     def __init__(self, path=''):
#         self._path = path

#     def __getattr__(self, path):
#         return Chain('%s/%s' % (self._path, path))

#     def __str__(self):
#         return self._path

# print(Chain().status.user.timeline.list)

# ### /status/user/timeline/list
#####
# #任何类，只需要定义一个__call__()方法，就可以直接对实例进行调用
# class Student(object):
#     def __init__(self, name):
#         self.name = name

#     def __call__(self,kk):
#         print('My name is %s/%s.' % (self.name,kk))
# s = Student('Michael')
# s('hello')
# #判断一个对象是否能被调用，能被调用的对象就是一个Callable对象
# print(callable(s))
#############
from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
#########
# # 若A.py和B.py位于不同的目录下，可以用以下方法

# # (假设B.py位于D盘的根目录下)

# import sys
# sys.path.append('D:/')
# import B
# if __name__=="__main__":
#     print B.pr(x,y)
#////////////////////////////////
# not useful python 中MethodType方法详解和使用
# from types import MethodType 
# """
# 文件名 class2.py
# MethodType 测试
# """
# # 首先看第一种方式
# #创建一个方法
# # def set_age(self, arg):
# #     self.age = arg    
# # #创建一个类    
# # class Student(object):
# #     pass
# # #------以上为公共部分
# # s_one = Student()
# # #给student 创建一个方法 但这里不是在class中创建而是创建了一个链接把外部的set_age 方法用链接知道Student内
# # s_one.set_age = MethodType(set_age,s_one,Student)
# # s_one.set_age(32)  #调用实例方法
# # print (s_one.age)
# # #》》》》结果 32
# # s_two = Student() 
# # s_two.set_age(100)  #这里来验证下是在类内有方法还是类外有方法。
# # print (s_two.age)
# #直接用类来创建一个方法  不过此时还是用链接的方式在类外的内存中创建
# # Student.set_age = MethodType(set_age,Student)
# # #此时在创建实例的时候外部方法 set_age 也会复制 这些实例和Student类都指向同一个set_age方法
# # new1 = Student()
# # new2 = Student()
# # new1.set_age(99)
# # new2.set_age(98) 　　#第二个会覆盖第一个 
# # print (new1.age,new2.age) 　　#看结果 2个都是98  