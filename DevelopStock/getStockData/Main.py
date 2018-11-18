import GetCompleteData 
import xlwt
import sys
import getopt
sys.path.append('./')
print("脚本名：",sys.argv[0])
len1 =len(sys.argv)

def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'t:i:a:c:f:h',['text=','item=','all=','code =','files=','help'])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        sys.exit()

    # print (opts)
    # print (args)
    all =""
    files=""
    code=""
    item=""
    text=""
    for o, a in opts:
        if o in ("-h", "--help"):
            print("-a a   [get all stock account data,-a can not use with -c]       ")
            print("-f fname   [set out file name,can use it with other option]       ")
            print("-c code [set stock code ,get this code account data]")
            print("-i type [set account type, 1- zcfzb ,2 - lrb ,3-xjllb]")
            print("-t accountItem [set accout item]")
            print("for example:")
            print("      python main.py -a a")
            print("      python main.py -c 000625 -f test")
            print("      python main.py -i 1 -t 所有者权益")
            sys.exit()
        elif o in ("-a", "--all"):
            all = a
        elif o in ("-f", "--files"):
            files = a
        elif o in ("-c","--code"):
            code =a
        elif o in ("-i","--item"):
            if (a in('1','2','3')):
                item =a
            else:
                item ='1'
        elif o in ("-t","--text"):
            text = a
    # print (all) 
    # print (files)
    # print (code)
    # if(len(files)==0):
    allC =GetCompleteData.CollectFrom163() 
    df =allC.Get_Stock_List()
    if len(files)>0:
        allC.Set_Stock_fName(files)
    if all =="a":
        if len(files)>0:
            allC.Set_Stock_fName(files)
        
        allC.GetAllFullAcount(df)
    elif len(code)>0:
        allC.GetFullAcount(code)
    elif len(item)>0:
        allC.Set_Stock_Item(item)
        allC.Set_Stock_Text(text)
        allC.GetData(df,0)

if __name__ == '__main__':
    MainOpt()