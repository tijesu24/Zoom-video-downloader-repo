# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSettings, pyqtSignal
from PyQt5.QtWidgets import QDialog
from pathlib import Path
import os


class Settings_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Settings")
        Dialog.setWindowModality(QtCore.Qt.WindowModal)
        Dialog.resize(443, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(446, 350))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 433, 250))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.logFile_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.logFile_label.setObjectName("logFile_label")
        self.verticalLayout.addWidget(self.logFile_label)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.logFile_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.logFile_lineEdit.setText("")
        self.logFile_lineEdit.setReadOnly(True)
        self.logFile_lineEdit.setClearButtonEnabled(False)
        self.logFile_lineEdit.setObjectName("logFile_lineEdit")
        self.horizontalLayout.addWidget(self.logFile_lineEdit)
        self.browse_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.browse_pushButton.setObjectName("browse_pushButton")
        self.horizontalLayout.addWidget(self.browse_pushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.openlog_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.openlog_pushButton.setObjectName("openlog_pushButton")
        self.horizontalLayout_5.addWidget(self.openlog_pushButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        # self.openlog_pushButton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        # self.openlog_pushButton.setObjectName("openlog_pushButton")
        # self.verticalLayout_3.addWidget(self.openlog_pushButton)

        self.no_simulDwld_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.no_simulDwld_label.setObjectName("simDwld_label")
        self.verticalLayout_3.addWidget(self.no_simulDwld_label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.no_simulDwnld_spinBox = QtWidgets.QSpinBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.no_simulDwnld_spinBox.sizePolicy().hasHeightForWidth())
        self.no_simulDwnld_spinBox.setSizePolicy(sizePolicy)
        self.no_simulDwnld_spinBox.setObjectName("simDwld_spinBox")
        self.horizontalLayout_2.addWidget(self.no_simulDwnld_spinBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.jwtKey_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jwtKey_label.sizePolicy().hasHeightForWidth())
        self.jwtKey_label.setSizePolicy(sizePolicy)
        self.jwtKey_label.setObjectName("jwlKey_label")
        self.verticalLayout_3.addWidget(self.jwtKey_label)
        self.jwtKey_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jwtKey_lineEdit.sizePolicy().hasHeightForWidth())
        self.jwtKey_lineEdit.setSizePolicy(sizePolicy)
        self.jwtKey_lineEdit.setObjectName("jwtKey_lineEdit")
        self.verticalLayout_3.addWidget(self.jwtKey_lineEdit)

        self.jwtSecret_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jwtSecret_label.sizePolicy().hasHeightForWidth())
        self.jwtSecret_label.setSizePolicy(sizePolicy)
        self.jwtSecret_label.setObjectName("jwtSecret_label")
        self.verticalLayout_3.addWidget(self.jwtSecret_label)

        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.jwtSecret_lineEdit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.jwtSecret_lineEdit.sizePolicy().hasHeightForWidth())
        self.jwtSecret_lineEdit.setSizePolicy(sizePolicy)
        self.jwtSecret_lineEdit.setObjectName("jwtSecret_lineEdit")
        self.horizontalLayout_6.addWidget(self.jwtSecret_lineEdit, stretch=7)
        self.view_secret_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.view_secret_button.setObjectName("View_secret_button")
        self.horizontalLayout_6.addWidget(self.view_secret_button, stretch=1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.testbutton = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.testbutton.setObjectName("Reset_button")
        self.verticalLayout_3.addWidget(self.testbutton)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.scrollAreaWidgetContents)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_3.addWidget(self.buttonBox)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Settings"))
        self.logFile_label.setText(_translate("Dialog", "Log file location :"))
        self.browse_pushButton.setText(_translate("Dialog", "Browse"))
        self.no_simulDwld_label.setText(_translate("Dialog", "Number of simulateneous downloads : "))
        self.jwtKey_label.setText(_translate("Dialog", "JWT Key :"))
        self.jwtSecret_label.setText(_translate("Dialog", "JWT Secret :"))
        self.jwtSecret_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.openlog_pushButton.setText(_translate("Dialog", "Open Log"))
        self.testbutton.setText(_translate("Dialog", "Reset Defaults"))
        self.view_secret_button.setText("show")


class Settings_Dialog_extd(Settings_Dialog, QDialog):
    FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
    jwt_modified = pyqtSignal()

    def __init__(self, parent=None):
        super(Settings_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.init_dialog()
        self.secret_shown = False

    def init_dialog(self):
        # Link buttons
        self.buttonBox.accepted.connect(self.saveSettings)
        self.buttonBox.rejected.connect(self.close)
        self.browse_pushButton.clicked.connect(self.setLogFileDialog)
        self.openlog_pushButton.clicked.connect(self.openLogFileLocation)
        self.testbutton.clicked.connect(self.resetSettings)
        self.testbutton.clicked.connect(self.close)
        self.view_secret_button.clicked.connect(self.toggleSecretShow)

        #

        # Set default value dict
        home = Path.home()
        self.default_values = {"logFileLocation": str(home.joinpath("Documents\\ZVD")),
                               "no_simulDwnld": 10}

        self.settings = QSettings('ZVD', 'tjo')

        # Get settings values
        self.jwtSecret_init = self.settings.value("jwtSecret")
        self.jwtKey_init = self.settings.value("jwtKey")
        self.logFileLocation_init = self.settings.value("logFileLocation")
        self.no_simulDwnld_init = self.settings.value("no_simulDwnld", type=int)

        # Fill up the dialog if exists else fill default values
        if self.jwtSecret_init:
            self.jwtSecret_lineEdit.setText(self.jwtSecret_init)

        if self.jwtKey_init:
            self.jwtKey_lineEdit.setText(self.jwtKey_init)

        if self.logFileLocation_init:
            self.logFile_lineEdit.setText(self.logFileLocation_init)
        else:
            self.logFile_lineEdit.setText(self.default_values["logFileLocation"])

        if self.no_simulDwnld_init:
            self.no_simulDwnld_spinBox.setValue(self.no_simulDwnld_init)
        else:
            self.no_simulDwnld_spinBox.setValue(self.default_values["no_simulDwnld"])

    def saveSettings(self):
        jwtSecret = self.jwtSecret_lineEdit.text()
        jwtKey = self.jwtKey_lineEdit.text()
        logFileLocation = self.logFile_lineEdit.text()
        no_simulDwnld = self.no_simulDwnld_spinBox.value()

        if (self.jwtSecret_init != jwtSecret) and jwtSecret:
            self.settings.setValue("jwtSecret", self.jwtSecret_lineEdit.text())
            self.jwt_modified.emit()
        if (self.jwtKey_init != jwtKey) and jwtKey:
            self.settings.setValue("jwtKey", self.jwtKey_lineEdit.text())
            self.jwt_modified.emit()
        if (self.logFileLocation_init != logFileLocation) and logFileLocation:
            self.settings.setValue("logFileLocation", self.logFile_lineEdit.text())
        if (self.no_simulDwnld_init != no_simulDwnld) and no_simulDwnld:
            self.settings.setValue("no_simulDwnld", self.no_simulDwnld_spinBox.value())
        self.close()

    def resetSettings(self):
        self.settings.clear()

    def setLogFileDialog(self):
        fileDirectory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select folder to save log file in:",
                                                                   self.logFile_lineEdit.text())
        if fileDirectory:
            self.logFile_lineEdit.setText(fileDirectory)

    def openLogFileLocation(self):
        log_file = self.logFile_lineEdit.text() + "/zvd_log.txt"
        if os.path.exists(log_file):
            os.startfile(self.logFile_lineEdit.text())

    def toggleSecretShow(self):
        if self.jwtSecret_lineEdit.echoMode() == QtWidgets.QLineEdit.Password:
            self.jwtSecret_lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.view_secret_button.setText("hide")
        else:
            self.jwtSecret_lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            self.view_secret_button.setText("show")
