import os
from PyQt5 import QtCore, QtGui, QtWidgets
from MinDataUiBase import Ui_Dialog
from PyQt5.QtCore import QStringListModel
class MinDataUi_Dialog(Ui_Dialog):#QtWidgets.QWidget
    def setupUi(self,Dialog):
        Dialog.setObjectName("分时数据提取")
        super().setupUi(Dialog)
        self.dqljwj.clicked.connect(self.on_dqljwj_click)#self.myButton.clicked.connect(self.msg)  
        self.dqljwj_2.clicked.connect(self.on_dqljwj_2_click)
        self.listView.clicked.connect(self.on_listview_click)
        self.ljxz.clicked.connect(self.on_ljxz_click)
        # self.dateEdit.setDate(QDate(2018, 12, 28))
    def on_listview_click(self,qModelIndex):
        txtN =self.strlist[qModelIndex.row()]
        txtN =txtN[0:8]
        self.gpdmHb.setText(txtN)
    def on_ljxz_click(self):
        self.savePath = QtWidgets.QFileDialog.getExistingDirectory(self,  
                            "浏览",  
                            ".\\")
        self.bclj_2.setText(self.savePath)
       

    def on_dqljwj_click(self):
        download_path = QtWidgets.QFileDialog.getExistingDirectory(self,  
                            "浏览",  
                            ".\\")
        self.dqlj.setText(download_path)
    def on_dqljwj_2_click(self):
        path =self.dqlj.text()
        files = os.listdir(path)
        self.strlist=[]
        for fi in files:
            fi_d = os.path.join(path,fi) 
            if os.path.isdir(fi_d):
                continue
            else:
                fi_d =fi_d.replace(path+'\\','')
                self.strlist.append(fi_d)
        #实例化列表模型，添加数据
        slm=QStringListModel()
        

        #设置模型列表视图，加载数据列表
        slm.setStringList(self.strlist)

        #设置列表视图的模型
        self.listView.setModel(slm)



        
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = MinDataUi_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
