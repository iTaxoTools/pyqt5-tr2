#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#import Qt
from PyQt5 import QtWidgets, QtCore, QtGui

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import re
import sys, os
from PyQt5.uic import loadUiType
from run_tr2 import *

from PyQt5.QtGui import *

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


FORM_CLASS,_=loadUiType(resource_path("tr2py.ui"))

class Main(QMainWindow, FORM_CLASS):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path(os.path.join('icons', 'TR2.ico'))))
        self.Handel_Buttons()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)


    def closeEvent(self, event):
         close = QMessageBox.question(self, "QUIT", "Are you sure want to close the program?",QMessageBox.Yes | QMessageBox.No)
         if close == QMessageBox.Yes:
             event.accept()
         else:
             event.ignore()



    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.browse_file1)
        self.pushButton_2.clicked.connect(self.browse_file2)
        self.pushButton_3.clicked.connect(self.browse_file3)
        self.pushButton_4.clicked.connect(self.download1)
        self.pushButton_5.clicked.connect(self.browse_file4)
        self.pushButton_6.clicked.connect(self.browse_file5)
        self.pushButton_7.clicked.connect(self.browse_file6)
        self.pushButton_8.clicked.connect(self.download2)
        self.pushButton_9.clicked.connect(self.clear)



    def browse_file1(self):
        self.browse_file = QFileDialog.getOpenFileName(self, "browse file", directory=".",filter="All Files (*.*)")
        self.lineEdit.setText(QDir.toNativeSeparators(str(self.browse_file[0])))
        return self.browse_file[0]
    def browse_file2(self):
        self.browse_file = QFileDialog.getOpenFileName(self, "browse file", directory=".",filter="All Files (*.*)")
        self.lineEdit_2.setText(QDir.toNativeSeparators(str(self.browse_file[0])))
        return self.browse_file[0]


    def browse_file3(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)



        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.lineEdit_3.setText(QDir.toNativeSeparators(str(filenames[0])))
    def browse_file4(self):
        self.browse_file = QFileDialog.getOpenFileName(self, "browse file", directory=".",filter="All Files (*.*)")
        self.lineEdit_4.setText(QDir.toNativeSeparators(str(self.browse_file[0])))
        return self.browse_file[0]
    def browse_file5(self):
        self.browse_file = QFileDialog.getOpenFileName(self, "browse file", directory=".",filter="All Files (*.*)")
        self.lineEdit_5.setText(QDir.toNativeSeparators(str(self.browse_file[0])))
        return self.browse_file[0]
    def browse_file6(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)



        if dlg.exec_():
            filenames = dlg.selectedFiles()
            self.lineEdit_6.setText(QDir.toNativeSeparators(str(filenames[0])))





    def download1(self):
        import time, re
        self.unique= str(int(time.time()))

        try:

            open_file1= self.lineEdit.text()
            open_file2= self.lineEdit_2.text()
            save_file = self.lineEdit_3.text()
            out_table= open(os.path.join(save_file, f"{self.unique}_out.table.txt"), "w+")
            out_table1= open(os.path.join(save_file, f"{self.unique}_out.table_tr2.spart"), "w+")
            out_tree = open(os.path.join(save_file, f"{self.unique}_out.tree.tre"), "w+")

            if open_file2== "":
                print("run tree search + guide search")
                ctr= build_consensus(open_file1)
                with open(open_file1+"_rtc", "w+") as f:
                    f.write(ctr.decode())
                from Bio import Phylo
                Phylo.convert(open_file1+"_rtc", "newick", open_file1[0:-4]+"guide", "newick")
                res= search(open_file1, open_file1[0:-4]+"guide")
                print("write: %s" % out_tree.name)
                print(res, file=out_tree)
                print("write: %s" % out_table.name)
                print(create_table(res), file=out_table)
                print(create_table_spart(res, open_file1), file=out_table1)

            else:
                res = search(open_file1, open_file2)
                print("write: %s" % out_tree.name)
                print(res, file=out_tree)
                print("write: %s" % out_table.name)
                print(create_table(res), file=out_table)

                print(create_table_spart(res, open_file1), file=out_table1)

            out_table.close()
            out_table1.close()
            out_tree.close()
            with open(os.path.join(save_file, f"{self.unique}_out.tree.tre"), "r+") as f:
                ww= f.read()
            ww= ww.replace("nan", "-0")
            ww= ww.replace("*", "")
            from ete3 import Tree, TreeStyle
            t= Tree(ww)
            ts= TreeStyle()
            ts.show_leaf_name= True
            ts.show_branch_length= True
            ts.show_branch_support= True
            t.render(save_file+"\\img_faces.png", w= 600, tree_style= ts)

        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Please check data type, analysis is failed because {e}")
            return

        QMessageBox.information(self, "Information", "The analysis is successfully")

        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")

    def download2(self):
        try:
            open_file1= self.lineEdit_4.text()
            open_file2= self.lineEdit_5.text()
            save_file = self.lineEdit_6.text()
            out_table = open(os.path.join(save_file, "out.table_hypothesis.txt"), "w")
            out_tree= open(os.path.join(save_file, "outnull.tre"), "w")
            res = model_comparison(open_file1, open_file2)
            print("write: %s" % out_table.name)
            print(list_scores(res), file=out_table)
            out_table.close()
            out_tree.close()

        except Exception as e:
            QMessageBox.warning(self, "Warning", "The species demitation output not obtained, please check input file type because {e}")
            return
        QMessageBox.information(self, "Information", "The species delimitation output hypothesis result generated successfully")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")



    def clear(self):
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")

def main1():

    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()


if __name__=='__main__':
    main1()
