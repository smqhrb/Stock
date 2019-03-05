import GetCompleteData 
import xlwt
import sys
import getopt
sys.path.append('./')
print("脚本名：",sys.argv[0])
len1 =len(sys.argv)

def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'d:t:i:a:c:f:p:y:h',['industry=','text=','item=','all=','code =','files=','pa =','year=','help'])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        sys.exit()


    all =""
    files=""
    code=""
    item=""
    text=""
    industry =""
    pp =""
    quarter =""
    for o, a in opts:
        if o in ("-h", "--help"):
            print("-a a           [get all stock account data,-a can not use with -c]       ")  #所有的股票信息
            print("-f fname       [set out file name,can use it with other option]       ")     #指定文件名前缀
            print("-c code        [set stock code ,get this code account data]")                #股票代码
            print("-i type        [set account type, 1- zcfzb ,2 - lrb ,3-xjllb]")              #股票财务类型
            print("-t accountItem [set accout item]")                                           #财务的项目
            print("-d industry    [set industry item]")                                         #行业类别
            print("-p analyst     [get index of account]")                                      #分析财务数据
            print("-j report      [if with this parameter,read year report ]")               #指定按年还是按报告季度
            print("for example:")
            print("      python main.py -a a")
            print("      python main.py -c 000625 -f QuarterReport")
            print("      python main.py -i 1 -t 所有者权益")
            print("      python main.py -i 1 -d 综合行业 -t 所有者权益")
            print("      python main.py -p 1")
            print("      python main.py -c 000625 -y 1 -f YearReport")
            sys.exit()
        elif o in ("-a", "--all"): #所有股票读取
            all = a
        elif o in ("-f", "--files"):    #设置输出文件的前缀名称
            files = a
        elif o in ("-c","--code"):  #股票代码
            code =a
        elif o in ("-i","--item"):
            if (a in('1','2','3')):  #指定三表之一 1- 资产负债表 ,2 - 利润表 ,3-现金流量表
                item =a
            else:
                item ='1'
        elif o in ("-t","--text"):  #按财务条目读取
            text = a
        elif o in ("-d","--industry"):#指定行业
            industry =a
        elif o in ("-p","--pa"):    #财务分析结果 1.从网上下载:1)基本指标(元) 2)杜邦分析 3)行业对比:估值水平, 市场表现 , 财务指标 , 公司规模
            pp =a                   #            2.读取三表输出的 :1)偿还能力 2)竞争力  3)盈利能力 4)清算估计 5)指标
        elif o in ("-y","--year"):
            quarter =a
    allC =GetCompleteData.CollectFrom163() 
    df =allC.Get_Stock_List()           #获取所有股票的信息

    if len(files)>0:
        allC.Set_Stock_fName(files)     #设置输出文件的前缀
    if len(quarter)>0:
        quarter ='year'
    if all =="a":
        if len(files)>0:
            allC.Set_Stock_fName(files) #设置输出文件的前缀
        
        allC.GetAllFullAcount(df,quarter)       #获取所有的股票的财务信息
    elif len(code)>0:
        allC.GetFullAcountTop(df,code,quarter)  #获取指定股票代码的财务信息
    elif len(item)>0:                   #获取指定表的指定项目进行汇总
        print (item)                    #三表之一
        print (text)                    #按财务条目
        print (industry)                #行业
        allC.Set_Stock_Item(item)
        allC.Set_Stock_Text(text)
        if len(industry)>0:
             allC.get_industry_classified(industry,0) #按行业获取 只能按年读取
        else:
            allC.GetData(df,0)
    elif len(pp)>0:
        allC.CaculateAssest()       #根据三表计算财务数据 和 从网上获取财务指标

if __name__ == '__main__':
    MainOpt()