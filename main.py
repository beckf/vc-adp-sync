import sys
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
        self.ui.vcDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))
        self.ui.vcParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))

        # Gather Config
        self.c = config.load_settings()
        self.field_maps = config.load_field_maps()

        # Set Labels
        self.ui.vc_api_user.setText(self.c["vcuser"])
        self.ui.vc_api_pass.setText(self.c["vcpass"])
        self.ui.vc_api_url.setText(self.c["vcurl"])
        self.ui.txt_fieldMap.setText(self.field_maps)

        # Connect buttons to methods
        self.ui.getVCDataButton.clicked.connect(self.get_vc_data)
        self.ui.settingsSave.clicked.connect(self.save_settings_button)
        self.ui.parseVCDataButton.clicked.connect(self.parse_vc_data)
        self.ui.btn_saveFieldMap.clicked.connect(self.save_field_map)

    def get_vc_data(self):
        """
        Get VC Data
        :return:
        """
        try:
            self.vcfsdata = []
            self.vc = v.Veracross()
            self.vcfsdata = self.vc.pull(self.c, "facstaff")

            if len(self.vcfsdata) > 0:
                self.ui.vcFSRecordCount.setText(str(len(self.vcfsdata)) + " Faculty Staff Records")
                self.ui.vcDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
                self.ui.lineEditXRateLimitReading.setText(self.vc.rate_limit_remaining)
                self.ui.lineEditXRateLimitResetReading.setText(self.vc.rate_limit_reset)
                self.debug_append_log("Found " + str(len(self.vcfsdata)) + " faculty staff records.")
        except:
            self.debug_append_log("Cannot get faculty staff from VC")

    def parse_vc_data(self):
        """
        Parse Action
        :return:
        """
        d = []
        for i in self.vcfsdata:

            if i["household_fk"] > 0:
                h = v.Veracross()
                hh = h.pull(self.c, "households/" + str(i["household_fk"]))
            else:
                hh = None

            a = {
                "employee_number": str(i["person_pk"]),
                "last_name": str(i["last_name"]),
                "first_name": str(i["first_name"]),
                "nick_name": str(i["nick_first_name"]),
                "middle_name": str(i["middle_name"]),
                "mobile_phone": str(i["mobile_phone"]),
                "home_phone": str(i["home_phone"]),
                "work_phone": str(i["business_phone"]),
                "email_1": str(i["email_1"])
            }

            if hh:
                a.update({"address_1": str(hh["household"]["address_1"])})
                a.update({"address_2": str(hh["household"]["address_2"])})
                a.update({"city": str(hh["household"]["city"])})
                a.update({"state_province": str(hh["household"]["state_province"])})
                a.update({"postal_code": str(hh["household"]["postal_code"])})

            d.insert(int(i["person_pk"]), a)
            del(hh)

        if len(d) > 0:
            self.ui.lineEditXRateLimitReading.setText(self.vc.rate_limit_remaining)
            self.ui.lineEditXRateLimitResetReading.setText(self.vc.rate_limit_reset)
            self.debug_append_log("Veracross data parse complete.")
            self.ui.vcParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
            self.ui.resultsTextEdit.setText(str(d))

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

    def save_field_map(self):
        """
        Saves the field maps to the config file
        :return:
        """
        # Save settings
        config.save_field_maps(self.ui.txt_fieldMap.toPlainText())
        # Reload Settings
        self.field_maps = config.load_field_maps()

    def debug_append_log(self, text):
        """
        Write to log window
        :param text:
        :return:
        """
        self.ui.textLog.moveCursor(QtGui.QTextCursor.End)
        self.ui.textLog.ensureCursorVisible()
        self.ui.textLog.insertHtml(text + "<br />")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
