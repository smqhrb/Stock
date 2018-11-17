import GetCompleteData as gg
import xlwt
import sys
print("脚本名：",sys.argv[0])
len =len(sys.argv)
if(len==1):
    wb = xlwt.Workbook()
    
    ws = wb.add_sheet(u'资产负债表')
    
    ws1 = wb.add_sheet(u'利润表')
    ws2 = wb.add_sheet(u'现金流量表')
    # GetData(df,count)
    gg.GetFullAcount('601319')
   
for i in range(1, len(sys.argv)):
    print ("参数", i, sys.argv[i])