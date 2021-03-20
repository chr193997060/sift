import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel

from PyQt5.QtGui import QPixmap, QImage

import cv2

import numpy as np





if __name__ == '__main__':

    app = QApplication(sys.argv)



    widget = QWidget()

    widget.resize(500, 550)

    widget.setWindowTitle('demo')



    lb= QLabel(widget)

    img_cv = cv2.imread(r"bbbb.jpg")
    img_cv = cv2.cvtColor(img_cv,cv2.COLOR_BGR2RGB)
    cv2.rectangle(img_cv,(10,20),(50,60),(0,0,255))

    h,w,c= img_cv.shape

    bytesPerLine= w*3

    qimg= QImage(img_cv.data,w,h,bytesPerLine, QImage.Format_RGB888)

    pix = QPixmap(qimg)

    lb.setPixmap(pix)

    widget.show()

    sys.exit(app.exec_())