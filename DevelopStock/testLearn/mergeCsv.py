import os
import pandas as pd
import glob
def merge_csv(path,outfile,cnt=0):
    csv_list = glob.glob('./%s/*.csv'%path) #查看同文件夹下的csv文件数
    print(u'共发现%s个CSV文件'% len(csv_list))
    print(u'正在处理..........outfile..')
    i =0
    tmp_fn ='temp_(%s).csv'%outfile
    for fn in csv_list: #循环读取同文件夹下的csv文件
        fr = open(fn,'rb').read()
        with open(tmp_fn,'ab') as f: #将结果保存为result.csv
            f.write(fr)
        if(cnt>0):
            i =i+1
            if (i>=cnt):
                break
    #print(u'合并完毕！')
    df = pd.read_csv(tmp_fn,header=0)

    datalist = df.drop_duplicates(keep = False)
    # datalist.to_csv("train_data_3500.csv", header = True,index = False)
    datalist_sorted = datalist.sort_values(by = ['DATA','ID'],ascending= False)

    datalist_sorted.to_csv("%s.csv"%outfile, header = True,index = False)
    print("%s.csv 合并完毕！"%outfile)


# merge_csv('20180101To20181031','train_data_3500')
# merge_csv('20181101To20190331','test_data_3500')
# merge_csv('20180101To20181031','train_data_1000',1000)
# merge_csv('20181101To20190331','test_data_1000',1000)