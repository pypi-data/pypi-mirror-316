# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'connectivity_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_ConnectivityDialog(object):
    def setupUi(self, ConnectivityDialog):
        if not ConnectivityDialog.objectName():
            ConnectivityDialog.setObjectName(u"ConnectivityDialog")
        ConnectivityDialog.resize(356, 190)
        self.verticalLayout = QVBoxLayout(ConnectivityDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.modbusOffset = QSpinBox(ConnectivityDialog)
        self.modbusOffset.setObjectName(u"modbusOffset")
        self.modbusOffset.setEnabled(False)
        self.modbusOffset.setMinimum(0)
        self.modbusOffset.setMaximum(999)
        self.modbusOffset.setSingleStep(1)
        self.modbusOffset.setValue(0)

        self.gridLayout.addWidget(self.modbusOffset, 2, 3, 1, 1)

        self.modbusLabel = QLabel(ConnectivityDialog)
        self.modbusLabel.setObjectName(u"modbusLabel")
        font = QFont()
        font.setBold(True)
        self.modbusLabel.setFont(font)

        self.gridLayout.addWidget(self.modbusLabel, 0, 0, 1, 4)

        self.blankLabel = QLabel(ConnectivityDialog)
        self.blankLabel.setObjectName(u"blankLabel")

        self.gridLayout.addWidget(self.blankLabel, 2, 2, 1, 1)

        self.modbusOffsetLabel = QLabel(ConnectivityDialog)
        self.modbusOffsetLabel.setObjectName(u"modbusOffsetLabel")
        self.modbusOffsetLabel.setEnabled(False)

        self.gridLayout.addWidget(self.modbusOffsetLabel, 2, 1, 1, 1)

        self.modbusCheckBox = QCheckBox(ConnectivityDialog)
        self.modbusCheckBox.setObjectName(u"modbusCheckBox")

        self.gridLayout.addWidget(self.modbusCheckBox, 1, 0, 1, 2)

        self.channelSocketLabel = QLabel(ConnectivityDialog)
        self.channelSocketLabel.setObjectName(u"channelSocketLabel")
        self.channelSocketLabel.setFont(font)

        self.gridLayout.addWidget(self.channelSocketLabel, 4, 0, 1, 4)

        self.horizontalSpacer = QSpacerItem(20, 13, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.modbusDetails = QPushButton(ConnectivityDialog)
        self.modbusDetails.setObjectName(u"modbusDetails")

        self.horizontalLayout.addWidget(self.modbusDetails)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 2, 1, 2)

        self.modbusChannelCountLabel = QLabel(ConnectivityDialog)
        self.modbusChannelCountLabel.setObjectName(u"modbusChannelCountLabel")
        self.modbusChannelCountLabel.setEnabled(False)

        self.gridLayout.addWidget(self.modbusChannelCountLabel, 3, 1, 1, 1)

        self.modbusChannelCount = QLabel(ConnectivityDialog)
        self.modbusChannelCount.setObjectName(u"modbusChannelCount")
        self.modbusChannelCount.setEnabled(False)
        self.modbusChannelCount.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.modbusChannelCount, 3, 2, 1, 2)

        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(10, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.buttonBox = QDialogButtonBox(ConnectivityDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(ConnectivityDialog)
        self.buttonBox.accepted.connect(ConnectivityDialog.accept)
        self.buttonBox.rejected.connect(ConnectivityDialog.reject)
        self.modbusCheckBox.toggled.connect(self.modbusOffsetLabel.setEnabled)
        self.modbusCheckBox.toggled.connect(self.modbusOffset.setEnabled)
        self.modbusCheckBox.toggled.connect(self.modbusChannelCountLabel.setEnabled)
        self.modbusCheckBox.toggled.connect(self.modbusChannelCount.setEnabled)

        QMetaObject.connectSlotsByName(ConnectivityDialog)
    # setupUi

    def retranslateUi(self, ConnectivityDialog):
        ConnectivityDialog.setWindowTitle(QCoreApplication.translate("ConnectivityDialog", u"Device Connectivity", None))
        self.modbusLabel.setText(QCoreApplication.translate("ConnectivityDialog", u"Modbus TCP", None))
        self.blankLabel.setText("")
        self.modbusOffsetLabel.setText(QCoreApplication.translate("ConnectivityDialog", u"Modbus Register Offset", None))
        self.modbusCheckBox.setText(QCoreApplication.translate("ConnectivityDialog", u"Enable Modbus TCP access", None))
        self.channelSocketLabel.setText(QCoreApplication.translate("ConnectivityDialog", u"Channel Socket", None))
        self.modbusDetails.setText(QCoreApplication.translate("ConnectivityDialog", u"Register Details...", None))
        self.modbusChannelCountLabel.setText(QCoreApplication.translate("ConnectivityDialog", u"Modbus Channel Count", None))
        self.modbusChannelCount.setText(QCoreApplication.translate("ConnectivityDialog", u"0", None))
    # retranslateUi

