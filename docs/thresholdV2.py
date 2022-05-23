# import system module and os module
import sys
import os

# import some PyQt5 modules
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QImage
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox


import cv2
import matplotlib.pyplot as plt 
import numpy as np
import sqlite3

from PyQt5.QtCore import pyqtSlot, pyqtSignal

from ui_thresholdV2 import *

class esikleme(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(esikleme, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.baglanti_olustur()
        self.ui.setupUi(self)        

        self.image = cv2.imread("img1.jpg")
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = cv2.resize(self.image, (450,450))
        cv2.imwrite("image.png", self.image)
        self.pixmap = QPixmap("image.png")

        self.ui.label_image.setPixmap(self.pixmap)
        self.ui.pushButtonBaslat.clicked.connect(self.threshold_start)
        self.ui.horizontalSlider.valueChanged[int].connect(self.threshold_changed)
        self.ui.pushButtonCikis.clicked.connect(self.cikis)

        self.cursor.execute("SELECT * FROM Threshold WHERE ref = 1;")
        self.data = self.cursor.fetchone()
        self.ui.horizontalSlider.setValue(self.data["deger"])
        self.threshold_changed(self.data["deger"])

 
    # connect to database
    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("thresh_database.db",isolation_level=None)
        self.baglanti.row_factory = sqlite3.Row
        self.cursor = self.baglanti.cursor()
        self.cursor.execute("Create table If not exists Threshold (deger INTEGER)")
        self.baglanti.commit()

    def threshold_start(self):
        self.ui.label_threshold.setPixmap(self.pixmap)
 
    def threshold_changed(self, index):
        self.ui.lineEdit.setText(str(index))
        self.index = index
        self.resim = cv2.imread("image.png")

        image_gray = cv2.cvtColor(self.resim, cv2.COLOR_BGR2GRAY)
    
        _, resim_thres = cv2.threshold(image_gray, self.index, 255, cv2.THRESH_BINARY)
        _, step = resim_thres.shape
        qImgResult = QtGui.QImage(resim_thres, resim_thres.shape[1], resim_thres.shape[0], step,
                                    QtGui.QImage.Format_Grayscale8)

        self.ui.label_threshold.setPixmap(QPixmap.fromImage(qImgResult))

        yeni_deger = self.ui.horizontalSlider.value()
        
        self.cursor.execute("UPDATE Threshold SET deger = {} WHERE ref = 1;".format(yeni_deger))
        self.baglanti.commit()     
    
    def cikis(self):
        self.index = self.data
        if __name__ == '__main__':
            sys.exit(app.exec_())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = esikleme()
    mainWindow.show()
    sys.exit(app.exec_())