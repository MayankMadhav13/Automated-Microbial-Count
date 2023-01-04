# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 21:44:46 2019

@author: MAYANK
"""

# coding: utf-8

# In[1]:

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
from tqdm import * 
from skimage.morphology import erosion, dilation, opening, closing, white_tophat


class Img_Proc_Gui(QWidget):
    def __init__(self, parent=None):
        super(Img_Proc_Gui, self).__init__(parent)
        self.img_processed = False
        btn_process_img = QPushButton("Process Image")
        
        #calling for INPUT
        btn_process_img.clicked.connect(self.getInput)
         #NS
        btn_count = QPushButton("Count")
        btn_count.clicked.connect(self.count)
        #NE

        btn_quit = QPushButton("Quit")
        btn_quit.clicked.connect(self.quit_clicked)
        hbox_btn = QHBoxLayout()
        hbox_btn.addWidget(btn_process_img)
        hbox_btn.addWidget(btn_count)
        hbox_btn.addWidget(btn_quit)
        
        hbox_viewcount = QHBoxLayout()
        self.count_view = QLineEdit()
        hbox_viewcount.addWidget(self.count_view)
        
      #  self.Count_View = QtWidgets.QTextEdit()
       # self.Count_View.setGeometry(QtCore.QRect(500, 650, 104, 87))
       # self.Count_View.setObjectName("Count_View")
        #new end
        
        hbox_address = QHBoxLayout()
        self.address = QLineEdit()
        hbox_address.addWidget(self.address)
        btn_img_explorer = QPushButton('Open Image')
        hbox_address.addWidget(btn_img_explorer)

        btn_img_explorer.clicked.connect(self.open)

        hbox_size = QHBoxLayout()
        label_width = QLabel('Width :')
        label_height = QLabel('Height :')
        self.et_width = QLineEdit()
        self.et_height = QLineEdit()
        hbox_size.addWidget(label_width)
        hbox_size.addWidget(self.et_width)
        hbox_size.addWidget(label_height)
        hbox_size.addWidget(self.et_height)


       # hbox_save = QHBoxLayout()
       # self.address_save = QLineEdit()
       # hbox_save.addWidget(self.address_save)
       # self.btn_save = QPushButton('Save Image')
       # self.btn_save.clicked.connect(self.save)
      #  hbox_save.addWidget(self.btn_save)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_address)
        vbox.addLayout(hbox_size)
        vbox.addLayout(hbox_btn)
        vbox.addLayout(hbox_viewcount)
        #vbox.addLayout(hbox_save)
        

        self.setGeometry(200,200,600,600)
        self.setWindowTitle('Microbe Counter')
        self.setLayout(vbox)
        
    
    
    
    #@pyqtSlot()
    def quit_clicked(self):
        print("TAATAAAAA!!")
        cv2.destroyAllWindows()
        self.close()

   # @pyqtSlot()
    def open(self):
        fileName = QFileDialog.getOpenFileName(self,'openFile')
        self.address.setText(fileName[0])
        self.showImage(fileName[0])
        #print(fileName)

    def save(self):
        if self.img_processed:
            saveFile = QFileDialog.getSaveFileName(self,'saveFile')
            self.address_save.setText(saveFile[0])
            if saveFile[0] != '':
                cv2.imwrite(str(self.address_save.text()),self.req_img)
        else:
            QMessageBox.about(self,'Suggestion','Do Something')


    def showImage(self,address):
        img = cv2.imread(address)
        cv2.imshow('Yo',img)

    def getInput(self):
        self.req_height = self.et_height.text()
        self.req_width = self.et_width.text()
        if self.req_width != '' and self.req_height != '':
            self.ready = True
            self.img_processed = True
        else:
            self.ready =  False

        if self.ready is False :
            QMessageBox.about(self,'Error','Fill parameters to process')
        elif self.address.text() is '':
            QMessageBox.about(self,'Error','Select Image to process')
        else:
            self.req_img = self.process_img(cv2.imread(self.address.text()))
            cv2.imshow("req_img",self.req_img)

        #print(self.req_height,self.req_width)
        
     #NS   
    def count(self, imgtoproc):
        imgtoproc = cv2.cvtColor(imgtoproc, cv2.COLOR_BGR2GRAY)
        ret, thresh= cv2.threshold(imgtoproc,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=1) 
        from skimage import measure

        labels = measure.label(thresh)

        #print(labels.max())
        a = labels.max()
        count = "The total microbial count is:" + str(a)
        self.count_view.setText(count)
        
        
    #NE

    def process_img(self,imgtoproc):
        imgtoproc = cv2.cvtColor(imgtoproc, cv2.COLOR_BGR2GRAY)
        ret, thresh= cv2.threshold(imgtoproc,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=2) 
        from skimage import measure

        labels = measure.label(thresh)

        #print(labels.max())
        a = labels.max()
        count = "The total microbial count is:" + str(a)
        self.count_view.setText(count)
        return cv2.resize(thresh, (int(self.req_width), int(self.req_height)))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = Img_Proc_Gui()
    screen.show()
    sys.exit(app.exec_())

