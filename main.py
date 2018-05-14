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

        # Set Vars
        self.vcfsdata = []

        # Set Images
        self.ui.logo_label.setPixmap(QtGui.QPixmap(":/images/adp-vc-logo-100.png"))
        self.ui.vcDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))
        self.ui.vcParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))

        # Gather Config
        self.c = config.load_settings()

        # Create VC Instance
        self.vc = v.Veracross()

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
        Get VC Data
        :return:
        """
        try:
            self.vcfsdata = self.vc.pull(self.c, "facstaff")
            if len(self.vcfsdata) > 0:
                self.ui.vcFSRecordCount.setText(str(len(self.vcfsdata)) + " Faculty Staff Records")
                self.ui.vcDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
                self.ui.lineEditXRateLimitReading.setText(self.vc.rate_limit_remaining)
        except:
            print("cannot get fsdata")

    def parse_vc_data(self):
        """
        Parse Action
        :return:
        """
        d = []
        for i in self.vcfsdata:

            if i["household_fk"] > 0:
                hh = self.vc.pull(self.c, "households/" + str(i["household_fk"]))
            else:
                hh = None

            a = {
                "employee_number": str(i["person_pk"]),
                "last_name": str(i["last_name"]),
                "first_name": str(i["first_name"])
            }

            if hh:
                a.update({"address_1": str(hh["household"]["address_1"])})

            d.insert(int(i["person_pk"]), a)

        if len(d) > 0:
            print(d)
            self.ui.lineEditXRateLimitReading.setText(self.vc.rate_limit_remaining)
            self.ui.vcParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))

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
