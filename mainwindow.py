# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT/ADP/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(772, 555)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.tabs = QtWidgets.QTabWidget(self.centralWidget)
        self.tabs.setGeometry(QtCore.QRect(10, 20, 751, 481))
        self.tabs.setObjectName("tabs")
        self.syncTab = QtWidgets.QWidget()
        self.syncTab.setObjectName("syncTab")
        self.logo_label = QtWidgets.QLabel(self.syncTab)
        self.logo_label.setGeometry(QtCore.QRect(630, 10, 100, 100))
        self.logo_label.setText("")
        self.logo_label.setObjectName("logo_label")
        self.gridLayoutWidget = QtWidgets.QWidget(self.syncTab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 371, 71))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.vcFSRecordCount = QtWidgets.QLabel(self.gridLayoutWidget)
        self.vcFSRecordCount.setObjectName("vcFSRecordCount")
        self.gridLayout.addWidget(self.vcFSRecordCount, 0, 2, 1, 1)
        self.vcParseStatusLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.vcParseStatusLabel.setText("")
        self.vcParseStatusLabel.setObjectName("vcParseStatusLabel")
        self.gridLayout.addWidget(self.vcParseStatusLabel, 1, 1, 1, 1)
        self.parseVCDataButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.parseVCDataButton.setObjectName("parseVCDataButton")
        self.gridLayout.addWidget(self.parseVCDataButton, 1, 0, 1, 1)
        self.getVCDataButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.getVCDataButton.setObjectName("getVCDataButton")
        self.gridLayout.addWidget(self.getVCDataButton, 0, 0, 1, 1)
        self.vcDataFSStatusLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.vcDataFSStatusLabel.setText("")
        self.vcDataFSStatusLabel.setObjectName("vcDataFSStatusLabel")
        self.gridLayout.addWidget(self.vcDataFSStatusLabel, 0, 1, 1, 1)
        self.tabs.addTab(self.syncTab, "")
        self.fieldMapTab = QtWidgets.QWidget()
        self.fieldMapTab.setObjectName("fieldMapTab")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.fieldMapTab)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 731, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.btn_saveFieldMap = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_saveFieldMap.setObjectName("btn_saveFieldMap")
        self.verticalLayout_3.addWidget(self.btn_saveFieldMap)
        self.txt_fieldMap = QtWidgets.QTextBrowser(self.verticalLayoutWidget)
        self.txt_fieldMap.setReadOnly(False)
        self.txt_fieldMap.setAcceptRichText(False)
        self.txt_fieldMap.setObjectName("txt_fieldMap")
        self.verticalLayout_3.addWidget(self.txt_fieldMap)
        self.tabs.addTab(self.fieldMapTab, "")
        self.resultsTab = QtWidgets.QWidget()
        self.resultsTab.setObjectName("resultsTab")
        self.resultsTextEdit = QtWidgets.QTextEdit(self.resultsTab)
        self.resultsTextEdit.setGeometry(QtCore.QRect(10, 70, 721, 371))
        self.resultsTextEdit.setObjectName("resultsTextEdit")
        self.btn_ResultsPrevious = QtWidgets.QPushButton(self.resultsTab)
        self.btn_ResultsPrevious.setGeometry(QtCore.QRect(0, 20, 113, 32))
        self.btn_ResultsPrevious.setObjectName("btn_ResultsPrevious")
        self.btn_ResultsNext = QtWidgets.QPushButton(self.resultsTab)
        self.btn_ResultsNext.setGeometry(QtCore.QRect(130, 20, 113, 32))
        self.btn_ResultsNext.setObjectName("btn_ResultsNext")
        self.tabs.addTab(self.resultsTab, "")
        self.settingsTab = QtWidgets.QWidget()
        self.settingsTab.setObjectName("settingsTab")
        self.settingsSave = QtWidgets.QPushButton(self.settingsTab)
        self.settingsSave.setGeometry(QtCore.QRect(580, 410, 161, 41))
        self.settingsSave.setObjectName("settingsSave")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.settingsTab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 731, 339))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_3.setSpacing(6)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lbl_adpVCCustomFieldName = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lbl_adpVCCustomFieldName.setObjectName("lbl_adpVCCustomFieldName")
        self.gridLayout_3.addWidget(self.lbl_adpVCCustomFieldName, 5, 0, 1, 1)
        self.btn_pickerADPCertificateKey = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.btn_pickerADPCertificateKey.setObjectName("btn_pickerADPCertificateKey")
        self.gridLayout_3.addWidget(self.btn_pickerADPCertificateKey, 11, 1, 1, 1)
        self.lbl_CertificateKeyPath = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lbl_CertificateKeyPath.setObjectName("lbl_CertificateKeyPath")
        self.gridLayout_3.addWidget(self.lbl_CertificateKeyPath, 10, 0, 1, 1)
        self.lineEdit_adpCertificateKeyPath = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_adpCertificateKeyPath.setObjectName("lineEdit_adpCertificateKeyPath")
        self.gridLayout_3.addWidget(self.lineEdit_adpCertificateKeyPath, 10, 1, 1, 1)
        self.lbl_adpNetworkUsername = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lbl_adpNetworkUsername.setObjectName("lbl_adpNetworkUsername")
        self.gridLayout_3.addWidget(self.lbl_adpNetworkUsername, 3, 0, 1, 1)
        self.vc_api_url = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.vc_api_url.setObjectName("vc_api_url")
        self.gridLayout_3.addWidget(self.vc_api_url, 2, 1, 1, 1)
        self.lbl_vcapiurl = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lbl_vcapiurl.setObjectName("lbl_vcapiurl")
        self.gridLayout_3.addWidget(self.lbl_vcapiurl, 2, 0, 1, 1)
        self.vc_api_pass = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.vc_api_pass.setText("")
        self.vc_api_pass.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.vc_api_pass.setObjectName("vc_api_pass")
        self.gridLayout_3.addWidget(self.vc_api_pass, 1, 1, 1, 1)
        self.vc_api_user = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.vc_api_user.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.vc_api_user.setObjectName("vc_api_user")
        self.gridLayout_3.addWidget(self.vc_api_user, 0, 1, 1, 1)
        self.lbl_vcapiusername = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lbl_vcapiusername.setObjectName("lbl_vcapiusername")
        self.gridLayout_3.addWidget(self.lbl_vcapiusername, 0, 0, 1, 1)
        self.lbl_vcpassword = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lbl_vcpassword.setObjectName("lbl_vcpassword")
        self.gridLayout_3.addWidget(self.lbl_vcpassword, 1, 0, 1, 1)
        self.lineEdit_adpCertificatePEMPath = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_adpCertificatePEMPath.setObjectName("lineEdit_adpCertificatePEMPath")
        self.gridLayout_3.addWidget(self.lineEdit_adpCertificatePEMPath, 7, 1, 1, 1)
        self.lineEdit_adpUsername = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_adpUsername.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_adpUsername.setObjectName("lineEdit_adpUsername")
        self.gridLayout_3.addWidget(self.lineEdit_adpUsername, 3, 1, 1, 1)
        self.lbl_CertificatePath = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lbl_CertificatePath.setObjectName("lbl_CertificatePath")
        self.gridLayout_3.addWidget(self.lbl_CertificatePath, 7, 0, 1, 1)
        self.btn_pickerADPCertificate = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.btn_pickerADPCertificate.setObjectName("btn_pickerADPCertificate")
        self.gridLayout_3.addWidget(self.btn_pickerADPCertificate, 8, 1, 1, 1)
        self.lineEdit_adpVCCustomFieldName = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_adpVCCustomFieldName.setObjectName("lineEdit_adpVCCustomFieldName")
        self.gridLayout_3.addWidget(self.lineEdit_adpVCCustomFieldName, 5, 1, 1, 1)
        self.lbl_adpNetworkPassword = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.lbl_adpNetworkPassword.setObjectName("lbl_adpNetworkPassword")
        self.gridLayout_3.addWidget(self.lbl_adpNetworkPassword, 4, 0, 1, 1)
        self.lineEdit_adpPassword = QtWidgets.QLineEdit(self.gridLayoutWidget_3)
        self.lineEdit_adpPassword.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.lineEdit_adpPassword.setObjectName("lineEdit_adpPassword")
        self.gridLayout_3.addWidget(self.lineEdit_adpPassword, 4, 1, 1, 1)
        self.tabs.addTab(self.settingsTab, "")
        self.debugTab = QtWidgets.QWidget()
        self.debugTab.setObjectName("debugTab")
        self.textLog = QtWidgets.QTextBrowser(self.debugTab)
        self.textLog.setGeometry(QtCore.QRect(10, 240, 731, 192))
        self.textLog.setObjectName("textLog")
        self.lbl_Log = QtWidgets.QLabel(self.debugTab)
        self.lbl_Log.setGeometry(QtCore.QRect(10, 210, 60, 16))
        self.lbl_Log.setObjectName("lbl_Log")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.debugTab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 471, 71))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lbl_vcLastXRateLimitReading = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.lbl_vcLastXRateLimitReading.setObjectName("lbl_vcLastXRateLimitReading")
        self.gridLayout_2.addWidget(self.lbl_vcLastXRateLimitReading, 0, 0, 1, 1)
        self.lineEditXRateLimitReading = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEditXRateLimitReading.setObjectName("lineEditXRateLimitReading")
        self.gridLayout_2.addWidget(self.lineEditXRateLimitReading, 0, 1, 1, 1)
        self.lbl_vcLastXRateResetReading = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.lbl_vcLastXRateResetReading.setObjectName("lbl_vcLastXRateResetReading")
        self.gridLayout_2.addWidget(self.lbl_vcLastXRateResetReading, 1, 0, 1, 1)
        self.lineEditXRateLimitResetReading = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEditXRateLimitResetReading.setObjectName("lineEditXRateLimitResetReading")
        self.gridLayout_2.addWidget(self.lineEditXRateLimitResetReading, 1, 1, 1, 1)
        self.tabs.addTab(self.debugTab, "")
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.getVCDataButton, self.parseVCDataButton)
        MainWindow.setTabOrder(self.parseVCDataButton, self.btn_saveFieldMap)
        MainWindow.setTabOrder(self.btn_saveFieldMap, self.txt_fieldMap)
        MainWindow.setTabOrder(self.txt_fieldMap, self.btn_ResultsPrevious)
        MainWindow.setTabOrder(self.btn_ResultsPrevious, self.btn_ResultsNext)
        MainWindow.setTabOrder(self.btn_ResultsNext, self.resultsTextEdit)
        MainWindow.setTabOrder(self.resultsTextEdit, self.vc_api_user)
        MainWindow.setTabOrder(self.vc_api_user, self.vc_api_pass)
        MainWindow.setTabOrder(self.vc_api_pass, self.vc_api_url)
        MainWindow.setTabOrder(self.vc_api_url, self.lineEdit_adpUsername)
        MainWindow.setTabOrder(self.lineEdit_adpUsername, self.lineEdit_adpCertificatePEMPath)
        MainWindow.setTabOrder(self.lineEdit_adpCertificatePEMPath, self.settingsSave)
        MainWindow.setTabOrder(self.settingsSave, self.lineEditXRateLimitReading)
        MainWindow.setTabOrder(self.lineEditXRateLimitReading, self.lineEditXRateLimitResetReading)
        MainWindow.setTabOrder(self.lineEditXRateLimitResetReading, self.textLog)
        MainWindow.setTabOrder(self.textLog, self.tabs)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Veracross to ADP Sync"))
        self.vcFSRecordCount.setText(_translate("MainWindow", "0 Faculty Staff Records"))
        self.parseVCDataButton.setText(_translate("MainWindow", "Parse Veracross Data"))
        self.getVCDataButton.setText(_translate("MainWindow", "Get Veracross Data"))
        self.tabs.setTabText(self.tabs.indexOf(self.syncTab), _translate("MainWindow", "Sync"))
        self.label.setText(_translate("MainWindow", "Insert field mapping in JSON format.  See README."))
        self.btn_saveFieldMap.setText(_translate("MainWindow", "Save"))
        self.tabs.setTabText(self.tabs.indexOf(self.fieldMapTab), _translate("MainWindow", "Map Fields"))
        self.btn_ResultsPrevious.setText(_translate("MainWindow", "Previous"))
        self.btn_ResultsNext.setText(_translate("MainWindow", "Next"))
        self.tabs.setTabText(self.tabs.indexOf(self.resultsTab), _translate("MainWindow", "Results"))
        self.settingsSave.setText(_translate("MainWindow", "Save"))
        self.lbl_adpVCCustomFieldName.setToolTip(_translate("MainWindow", "Name of custom field in ADP where the Veracross ID is stored."))
        self.lbl_adpVCCustomFieldName.setText(_translate("MainWindow", "ADP VC Custom Field Name"))
        self.btn_pickerADPCertificateKey.setText(_translate("MainWindow", "Select Certificate Key"))
        self.lbl_CertificateKeyPath.setToolTip(_translate("MainWindow", "Certificate file used to create ADP certificate above."))
        self.lbl_CertificateKeyPath.setText(_translate("MainWindow", "ADP Certificate Key"))
        self.lbl_adpNetworkUsername.setToolTip(_translate("MainWindow", "ADP Network Username provided by ADP."))
        self.lbl_adpNetworkUsername.setText(_translate("MainWindow", "ADP Network Username"))
        self.lbl_vcapiurl.setToolTip(_translate("MainWindow", "Veracross API Base URL."))
        self.lbl_vcapiurl.setText(_translate("MainWindow", "Veracross API Base URL"))
        self.lbl_vcapiusername.setToolTip(_translate("MainWindow", "Veracross API Username provided by Veracross."))
        self.lbl_vcapiusername.setText(_translate("MainWindow", "Veracross API Username"))
        self.lbl_vcpassword.setToolTip(_translate("MainWindow", "Veracross API Password provided by Veracross."))
        self.lbl_vcpassword.setText(_translate("MainWindow", "Veracross API Password"))
        self.lbl_CertificatePath.setToolTip(_translate("MainWindow", "Path to Base64 encoded certificate provided by ADP."))
        self.lbl_CertificatePath.setText(_translate("MainWindow", "ADP Certificate (PEM)"))
        self.btn_pickerADPCertificate.setText(_translate("MainWindow", "Select Certificate"))
        self.lbl_adpNetworkPassword.setToolTip(_translate("MainWindow", "ADP Network Password provided by ADP."))
        self.lbl_adpNetworkPassword.setText(_translate("MainWindow", "ADP Network Password"))
        self.tabs.setTabText(self.tabs.indexOf(self.settingsTab), _translate("MainWindow", "Settings"))
        self.lbl_Log.setText(_translate("MainWindow", "Log"))
        self.lbl_vcLastXRateLimitReading.setText(_translate("MainWindow", "Veracross Last X-Rate-Limit-Remaining Reading"))
        self.lbl_vcLastXRateResetReading.setText(_translate("MainWindow", "Veracross Last X-Rate-Limit-Reset Reading"))
        self.tabs.setTabText(self.tabs.indexOf(self.debugTab), _translate("MainWindow", "Debug"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

