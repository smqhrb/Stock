import GetCompleteData 
import xlwt
import sys
import getopt
sys.path.append('./')
print("脚本名：",sys.argv[0])
len1 =len(sys.argv)
# if(len==1):
#     # GetData(df,count)
#     GetCompleteData.GetFullAcount('601319')
# else:
        
# for i in range(1, len(sys.argv)):
#     print ("参数", i, sys.argv[i])
def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'t:i:a:c:f:h',['text=','item=','all=','code =','files=','help'])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        sys.exit()

    print (opts)
    print (args)
    all =""
    files=""
    code=""
    item=""
    text=""
    for o, a in opts:
        if o in ("-h", "--help"):
            print("-h ")
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
        if len(item)>0:
            allC.Set_Stock_Item(item)
            allC.Set_Stock_Text(text)
            allC.GetData(df,0)
        


        

if __name__ == '__main__':
    MainOpt()