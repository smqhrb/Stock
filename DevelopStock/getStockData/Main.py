import GetCompleteData 
import xlwt
import sys
import getopt
sys.path.append('./')
print("脚本名：",sys.argv[0])
len =len(sys.argv)
# if(len==1):
#     # GetData(df,count)
#     GetCompleteData.GetFullAcount('601319')
# else:
        
# for i in range(1, len(sys.argv)):
#     print ("参数", i, sys.argv[i])
def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'a:c:f:h',['all=','code =','files=','help'])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        sys.exit()

    print (opts)
    print (args)
    for o, a in opts:
        if o in ("-h", "--help"):
            sys.exit()
        elif o in ("-a", "--all"):
            all = a
        elif o in ("-f", "--files"):
            files = a
        elif o in ("-c","--code"):
            code =a
    print (all) 
    print (files)
    print (code)
    if(len(files)==0):
        

if __name__ == '__main__':
    MainOpt()