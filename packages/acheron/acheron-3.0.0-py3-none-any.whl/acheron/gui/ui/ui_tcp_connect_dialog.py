# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tcp_connect_dialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QLineEdit, QSizePolicy,
    QSpinBox, QWidget)

class Ui_TCPConnectDialog(object):
    def setupUi(self, TCPConnectDialog):
        if not TCPConnectDialog.objectName():
            TCPConnectDialog.setObjectName(u"TCPConnectDialog")
        TCPConnectDialog.resize(341, 119)
        self.formLayout = QFormLayout(TCPConnectDialog)
        self.formLayout.setObjectName(u"formLayout")
        self.hostnameLabel = QLabel(TCPConnectDialog)
        self.hostnameLabel.setObjectName(u"hostnameLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.hostnameLabel)

        self.hostname = QLineEdit(TCPConnectDialog)
        self.hostname.setObjectName(u"hostname")
        self.hostname.setMinimumSize(QSize(200, 0))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.hostname)

        self.portLabel = QLabel(TCPConnectDialog)
        self.portLabel.setObjectName(u"portLabel")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.portLabel)

        self.port = QSpinBox(TCPConnectDialog)
        self.port.setObjectName(u"port")
        self.port.setMinimum(1)
        self.port.setMaximum(65535)
        self.port.setValue(5760)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.port)

        self.serialLabel = QLabel(TCPConnectDialog)
        self.serialLabel.setObjectName(u"serialLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.serialLabel)

        self.serial = QLineEdit(TCPConnectDialog)
        self.serial.setObjectName(u"serial")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.serial)

        self.buttonBox = QDialogButtonBox(TCPConnectDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.buttonBox)


        self.retranslateUi(TCPConnectDialog)
        self.buttonBox.accepted.connect(TCPConnectDialog.accept)
        self.buttonBox.rejected.connect(TCPConnectDialog.reject)

        QMetaObject.connectSlotsByName(TCPConnectDialog)
    # setupUi

    def retranslateUi(self, TCPConnectDialog):
        TCPConnectDialog.setWindowTitle(QCoreApplication.translate("TCPConnectDialog", u"Connect TCP Device", None))
        self.hostnameLabel.setText(QCoreApplication.translate("TCPConnectDialog", u"Hostname", None))
#if QT_CONFIG(tooltip)
        self.portLabel.setToolTip(QCoreApplication.translate("TCPConnectDialog", u"Default: 5760", None))
#endif // QT_CONFIG(tooltip)
        self.portLabel.setText(QCoreApplication.translate("TCPConnectDialog", u"Port", None))
#if QT_CONFIG(tooltip)
        self.port.setToolTip(QCoreApplication.translate("TCPConnectDialog", u"Default: 5760", None))
#endif // QT_CONFIG(tooltip)
        self.serialLabel.setText(QCoreApplication.translate("TCPConnectDialog", u"Serial Number (Optional)", None))
    # retranslateUi

