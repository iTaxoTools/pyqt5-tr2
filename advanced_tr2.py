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
from collections import defaultdict

import tempfile
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView,QWebEnginePage as QWebPage
from PyQt5 import QtWebEngineWidgets

from functools import partial


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


FORM_CLASS,_=loadUiType(resource_path("tr2_new.ui"))

class Main(QDialog, FORM_CLASS):
    def __init__(self,parent=None):
        QWidget.__init__(self)
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path(os.path.join('icon', 'TR2.ico'))))
        self.Handel_Buttons()
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)
        self.f= tempfile.TemporaryDirectory()
        self.filepath= defaultdict(lambda: None)
        self.outpath= defaultdict(lambda: None)
        self.toolButton_2.setEnabled(False)
        self.toolButton_3.setEnabled(False)
        self.outpath['output']= self.f.name


    def closeEvent(self, event):
         close = QMessageBox.question(self, "QUIT", "Are you sure want to close the program?",QMessageBox.Yes | QMessageBox.No)
         if close == QMessageBox.Yes:
             event.accept()
         else:
             event.ignore()



    def Handel_Buttons(self):
        self.toolButton.clicked.connect(self.trigger1)
        self.toolButton_2.clicked.connect(self.trigger2)
        self.toolButton_3.clicked.connect(self.save_all)

        self.toolButton_4.clicked.connect(self.clear)
        self.listWidget.itemDoubleClicked.connect(self.Clicked)

    def file_dialog(self, msg, path):
        return QFileDialog.getOpenFileName(self, msg, path)[0]


    def trigger1(self):

        if self.radioButton.isChecked() == True:
            self.open_file_delimitation()

        elif self.radioButton_2.isChecked() == True:
            self.open_file_hypothesis()

        else:
            QMessageBox.warning(self, "Warning", f"The selection should be made in radiobuttons")


    def trigger2(self):

        if self.radioButton.isChecked() == True:
            self.download1()

        elif self.radioButton_2.isChecked() == True:
            self.download2()

        else:
            QMessageBox.warning(self, "Warning", f"The selection should be made in radiobuttons")


    def open_file_delimitation(self):
        try:
            msg = '1) First, select the input gene trees in Newick format\n(the maximum number of trees, i.e. of loci, is around 1000).\n'
            msg += '2) Then, select the input guide tree in Newick format\n(you must provide a guide tree for the analysis)'
            QMessageBox.information(self, 'Add input files', msg)
            sel = 'Select tree file'
            tree = self.file_dialog(sel, ".")
            if tree:
                path = os.path.split(tree)[0]
                msg = 'Select guide tree file'
                guide = self.file_dialog(msg, path)
                self.filepath['input1']= tree
                self.filepath['input2']= guide
                self.toolButton_2.setEnabled(True)

        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Please select file upload is failed because {e}")


    def open_file_hypothesis(self):
        try:

            msg = '1) Select the input newick gene tree and \n(the maximum number of trees, i.e. of loci, is around 1000).\n'
            msg += '2) Select a tab delimited assignment file'
            QMessageBox.information(self, 'Add input files', msg)
            sel = 'Select gene file'
            tree = self.file_dialog(sel, ".")
            if tree:
                path = os.path.split(tree)[0]
                msg = 'Select tab delimited assignment file'
                tab = self.file_dialog(msg, path)
                self.filepath['input1']= tree
                self.filepath['input2']= tab
                self.toolButton_2.setEnabled(True)

        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Please select file upload is failed because {e}")




    def download1(self):
        import time, re
        self.unique= str(int(time.time()))

        try:

            open_file1= self.filepath['input1']
            open_file2= self.filepath['input2']
            save_file= self.outpath['output']
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
            self.toolButton_3.setEnabled(True)
            onlyfiles = [self.listWidget.addItem(f) for f in os.listdir(save_file) if os.path.isfile(os.path.join(save_file, f))]


        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Please check data type, analysis is failed because {e}")
            return

        QMessageBox.information(self, "Information", "The analysis is successfully")


    def download2(self):
        try:
            open_file1= self.filepath['input1']
            open_file2= self.filepath['input2']
            save_file= self.outpath['output']
            out_table = open(os.path.join(save_file, "out.table_hypothesis.txt"), "w")
            out_tree= open(os.path.join(save_file, "outnull.tre"), "w")
            res = model_comparison(open_file1, open_file2)
            print("write: %s" % out_table.name)
            print(list_scores(res), file=out_table)
            out_table.close()
            out_tree.close()
            self.toolButton_3.setEnabled(True)
            onlyfiles = [self.listWidget.addItem(f) for f in os.listdir(save_file) if os.path.isfile(os.path.join(save_file, f))]

        except Exception as e:
            QMessageBox.warning(self, "Warning", "The species demitation output not obtained, please check input file type because {e}")
            return
        QMessageBox.information(self, "Information", "The species delimitation output hypothesis result generated successfully")



    def save_all(self):
        try:

            msg = 'Please browse to output folder to save all files'
            QMessageBox.information(self, 'Browse output folder', msg)

            dlg = QFileDialog()
            dlg.setFileMode(QFileDialog.Directory)
            if dlg.exec_():
                filenames = dlg.selectedFiles()
                filename= QDir.toNativeSeparators(str(filenames[0]))
            import shutil
            file_names = os.listdir(self.outpath['output'])
            for file_name in file_names:
                shutil.copy(os.path.join(self.outpath['output'], file_name), filename)

        except Exception as e:
            print(e)
            QMessageBox.warning(self, "Warning", f"The output  is not saved because {e}")


    def clear(self):
        self.toolButton_2.setEnabled(False)
        self.toolButton_3.setEnabled(False)
        self.listWidget.clear()
        import os, shutil
        folder = self.f.name
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


    def Clicked(self, item2):
        try:
            self.w= AnotherWindow()
            name= item2.text()
            self.w= AnotherWindow()
            f = open(os.path.join(self.outpath['output'], name), "rt")
            mytext1 = QGraphicsSimpleTextItem(f.read())
            self.w.scene.addItem(mytext1)
            f.close()
            self.w.layout.addWidget(self.w.graph1)
            self.w.setLayout(self.w.layout)
            self.w.setWindowIcon(QIcon(os.path.join("icon", "TR2.ico")))
            self.w.setWindowTitle("tr2")
            self.w.show()

        except Exception as e:
            QMessageBox.warning(self, "Warning", f"The view  is not obtained because {e}")


class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.graph1= QGraphicsView()
        self.scene = QGraphicsScene()
        self.graph1.setScene(self.scene)
        self.m_output = QtWebEngineWidgets.QWebEngineView()



def main1():

    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()


if __name__=='__main__':
    main1()
