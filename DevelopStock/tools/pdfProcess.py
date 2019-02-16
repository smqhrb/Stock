# PDFMiner其特征有： 
# 1、完全使用python编写。（适用于2.4或更新版本） 
# 2、解析，分析，并转换成PDF文档。 
# 3、PDF-1.7规范的支持。（几乎） 
# 4、中日韩CJK语言和垂直书写脚本支持。 
# 5、各种字体类型（Type1、TrueType、Type3，和CID）的支持。 
# 6、基本加密（RC4）的支持。 
# 7、PDF与HTML转换。 
# 8、纲要（TOC）的提取。 
# 9、标签内容提取。 
# 10、通过分组文本块重建原始的布局。 
#  如果你的Python有安装pip模块，就可以通过pip命令自动安装pdfminer。(不支持中文)

#  #python pip install pdfminer

# 由于我们大部分处理的文档都是中文的 所以不能直接pip 安装 使用中日韩CJK文字须先编译再安装


# 首先下载 安装包

# 使用的是pdfminer-20140328.tar.gz 


# https://pypi.python.org/packages/57/4f/e1df0437858188d2d36466a7bb89aa024d252bd0b7e3ba90cbc567c6c0b8/pdfminer-20140328.tar.gz
# 然后在Windows cmd下输入命令:
# mkdir pdfminer\cmap
# python tools\conv_cmap.py -c B5=cp950 -c UniCNS-UTF8=utf-8 pdfminer\cmap Adobe-CNS1 cmaprsrc\cid2code_Adobe_CNS1.txt
# python tools\conv_cmap.py -c GBK-EUC=cp936 -c UniGB-UTF8=utf-8 pdfminer\cmap Adobe-GB1 cmaprsrc\cid2code_Adobe_GB1.txt
# python tools\conv_cmap.py -c RKSJ=cp932 -c EUC=euc-jp -c UniJIS-UTF8=utf-8 pdfminer\cmap Adobe-Japan1 cmaprsrc\cid2code_Adobe_Japan1.txt
# python tools\conv_cmap.py -c KSC-EUC=euc-kr -c KSC-Johab=johab -c KSCms-UHC=cp949 -c UniKS-UTF8=utf-8 pdfminer\cmap Adobe-Korea1 cmaprsrc\cid2code_Adobe_Korea1.txt
# python setup.py install

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/6 21:02
# @Author  : chen# @Site    : 
# @File    : simplePDF.py
# @Software: PyCharm
import os
from cStringIO import StringIO
import sys
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
def convert_pdf_2_text(path):    
    rsrcmgr = PDFResourceManager()    
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    with open(path, 'rb') as fp:
        for page in PDFPage.get_pages(fp, set()):
            interpreter.process_page(page)
        text = retstr.getvalue()
    device.close()
    retstr.close()
    return text