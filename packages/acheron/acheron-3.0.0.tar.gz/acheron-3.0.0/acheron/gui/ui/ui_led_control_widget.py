# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'led_control_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSlider,
    QSpinBox, QWidget)

class Ui_LEDControlWidget(object):
    def setupUi(self, LEDControlWidget):
        if not LEDControlWidget.objectName():
            LEDControlWidget.setObjectName(u"LEDControlWidget")
        LEDControlWidget.resize(176, 20)
        self.horizontalLayout_3 = QHBoxLayout(LEDControlWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.slider = QSlider(LEDControlWidget)
        self.slider.setObjectName(u"slider")
        self.slider.setMinimumSize(QSize(128, 0))
        self.slider.setMaximum(255)
        self.slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_3.addWidget(self.slider)

        self.spinBox = QSpinBox(LEDControlWidget)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMaximum(255)

        self.horizontalLayout_3.addWidget(self.spinBox)

        QWidget.setTabOrder(self.slider, self.spinBox)

        self.retranslateUi(LEDControlWidget)
        self.slider.valueChanged.connect(self.spinBox.setValue)
        self.spinBox.valueChanged.connect(self.slider.setValue)

        QMetaObject.connectSlotsByName(LEDControlWidget)
    # setupUi

    def retranslateUi(self, LEDControlWidget):
        LEDControlWidget.setWindowTitle(QCoreApplication.translate("LEDControlWidget", u"LED Control Widget", None))
    # retranslateUi

