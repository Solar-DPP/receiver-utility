# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'serial_saver.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
                            QMetaObject, QObject, QPoint, QRect, QSize, Qt,
                            QTime, QUrl)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
                           QFontDatabase, QGradient, QIcon, QImage,
                           QKeySequence, QLinearGradient, QPainter, QPalette,
                           QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout,
                               QMainWindow, QPushButton, QSizePolicy,
                               QSpacerItem, QTextEdit, QVBoxLayout, QWidget)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.portsCombo = QComboBox(self.centralwidget)
        self.portsCombo.setObjectName("portsCombo")

        self.horizontalLayout.addWidget(self.portsCombo)

        self.refresh_button = QPushButton(self.centralwidget)
        self.refresh_button.setObjectName("refresh_button")

        self.horizontalLayout.addWidget(self.refresh_button)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.open_button = QPushButton(self.centralwidget)
        self.open_button.setObjectName("open_button")

        self.horizontalLayout.addWidget(self.open_button)

        self.CloseButton = QPushButton(self.centralwidget)
        self.CloseButton.setObjectName("CloseButton")

        self.horizontalLayout.addWidget(self.CloseButton)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.textEdit)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "SerialSaver", None)
        )
        self.refresh_button.setText(
            QCoreApplication.translate("MainWindow", "Refresh", None)
        )
        self.open_button.setText(QCoreApplication.translate("MainWindow", "Open", None))
        self.CloseButton.setText(
            QCoreApplication.translate("MainWindow", "Close", None)
        )

    # retranslateUi
