'''
https://blog.csdn.net/sinat_34817187/article/details/81285747
'''
import xlrd
import xlwt
from xlutils.copy import copy

dir = os.path.abspath('.').split('src')[0]
'''主要逻辑实现'''
oldWb = xlrd.open_workbook(dir+"/data/考勤系统/考勤系统.xlsx");#先打开已存在的表
newWb = copy(oldWb)#复制
newWs = newWb.get_sheet(2);#取sheet表
newWs.write(2, 4, "pass");#写入 2行4列写入pass
newWb.save(dir+"/result/考勤系统.xls"); #保存至result路径
#创建一个样式----------------------------
style = XFStyle()
pattern = Pattern()
pattern.pattern = Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = Style.colour_map['red'] #设置单元格背景色为黄色
style.pattern = pattern
#-----------------------------------------
部分代码：
 xpath="html/body/div[1]/div/div/div/div[2]/h4"
              if self.isElementExist(xpath):
                    text1 = self.driver.find_element_by_xpath(xpath).text
                    if text1 == except1:
                        newWs.write(rows, 5, "pass");
                    else:
                        newWs.write(rows, 5, "fail",style = style);     ###样式引用     
                else:
                    logger.error("没找到元素" ) 
