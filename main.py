import sys,os,socket,pickle
from PyQt5 import QtWidgets, QtGui, QtCore
from mainwindow import Ui_MainWindow
import images
import veracross_api as v
import config
import pprint

class Main(QtWidgets.QMainWindow):
    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set Images
        self.ui.logo_label.setPixmap(QtGui.QPixmap(":/images/adp-vc-logo-100.png"))
        self.ui.vcDataStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))
        self.ui.vcParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))

        #Gather Config
        self.c = config.load_settings()

        # Set Labels
        self.ui.vc_api_user.setText(self.c["vcuser"])
        self.ui.vc_api_pass.setText(self.c["vcpass"])
        self.ui.vc_api_url.setText(self.c["vcurl"])

        # Connect buttons to methods
        self.ui.getVCDataButton.clicked.connect(self.get_vc_data)
        self.ui.settingsSave.clicked.connect(self.save_settings_button)
        self.ui.parseVCDataButton.clicked.connect(self.parse_vc_data)

    def get_vc_data(self):
        """
        Get VC Faculty Staff
        :return:
        """
        try:
            self.vcdata = v.fs(self.c["vcurl"], self.c["vcuser"], self.c["vcpass"])
            if len(self.vcdata) > 0:
                self.ui.vcRecordCount.setText(str(len(self.vcdata)) + " Records")
                self.ui.vcDataStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
        except:
            print("cannot get fsdata")

    def parse_vc_data(self):
        """
        Parse Action
        :return:
        """
        try:
            self.vc_parsed_data = v.parse_fs(self.vcdata)
            if len(self.vc_parsed_data) > 0:
                self.ui.vcParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
        except:
            print("no vcdata")

    def save_settings_button(self):
        """
        Save settings
        :return:
        """
        settings = {
            "vcuser": self.ui.vc_api_user.text(),
            "vcpass": self.ui.vc_api_pass.text(),
            "vcurl": self.ui.vc_api_url.text()
        }
        # Save settings
        config.save_settings(settings)
        # Reload Settings
        self.c = config.load_settings()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
