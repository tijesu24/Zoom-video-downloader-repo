# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'process.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from time import sleep

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog


class Ui_Dialog(object):
    def __init__(self, parent=None, continuable=False):
        super(Ui_Dialog, self).__init__(parent)
        self.continuable = continuable

    def setupUi(self, Dialog, title):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle(title)
        Dialog.resize(282, 217)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        Dialog.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        Dialog.setAutoFillBackground(True)

        pal = QtGui.QPalette()

        pal.setColor(QtGui.QPalette.Window, QtCore.Qt.white)
        Dialog.setPalette(pal)

        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_label = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.text_label.sizePolicy().hasHeightForWidth())
        self.text_label.setSizePolicy(sizePolicy)
        self.text_label.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        self.text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.text_label.setObjectName("text_label")
        self.verticalLayout_2.addWidget(self.text_label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        if self.continuable:
            self.pushButton_3 = QtWidgets.QPushButton(Dialog)
            self.pushButton_3.setObjectName("continue_pushbutton")
            self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Process Status"))
        self.text_label.setText(_translate("Dialog", "Process Details"))
        self.text_label.setWordWrap(True)

        self.pushButton_2.setText(_translate("Dialog", "Cancel"))
        if self.continuable:
            self.pushButton_3.setText(_translate("Dialog", "Continue"))
            self.pushButton_3.setEnabled(False)


class Process_Dialog(Ui_Dialog, QDialog):
    def __init__(self, title, parent=None, continuable=False, closable=True):
        super(Process_Dialog, self).__init__(parent, continuable=continuable)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, closable)
        self.setupUi(self, title)
        self.setStyleSheet(
            """
        QLabel{
            font-size:12px;

        }""")

    def setLoadingCursor(self, status):
        self.text_label.setCursor(
            QtGui.QCursor(QtCore.Qt.BusyCursor) if status else QtGui.QCursor(QtCore.Qt.ArrowCursor))
