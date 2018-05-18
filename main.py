import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from mainwindow import Ui_MainWindow
import images
import veracross_api as v
import config
import json

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
        self.c = config.load_settings("config")
        self.field_maps = config.load_settings("fields")

        # Set Labels
        self.ui.vc_api_user.setText(self.c["vcuser"])
        self.ui.vc_api_pass.setText(self.c["vcpass"])
        self.ui.vc_api_url.setText(self.c["vcurl"])
        self.ui.lineEdit_adpUsername.setText(self.c["adpnetuser"])
        self.ui.lineEdit_adpPassword.setText(self.c["adpnetpass"])
        self.ui.lineEdit_adpCertificatePath.setText("~/")
        self.ui.lineEdit_adpCertificatePath.setText(self.c["adpcertpath"])
        self.ui.txt_fieldMap.setText(self.field_maps)

        # Connect buttons to methods
        self.ui.getVCDataButton.clicked.connect(self.get_vc_data)
        self.ui.settingsSave.clicked.connect(self.save_settings_button)
        self.ui.parseVCDataButton.clicked.connect(self.parse_vc_data)
        self.ui.btn_saveFieldMap.clicked.connect(self.save_field_map)
        self.ui.btn_pickerADPCertificate.clicked.connect(self.select_adp_certfile)


    def get_vc_data(self):
        """
        Get VC Data
        :return:
        """
        try:
            self.vcfsdata = []
            self.vc = v.Veracross()
            self.vc.session.auth = (self.c["vcuser"], self.c["vcpass"])
            self.vc.base_url = self.c["vcurl"]
            self.vcfsdata = self.vc.pull("facstaff")

            if len(self.vcfsdata) > 0:
                self.ui.vcFSRecordCount.setText(str(len(self.vcfsdata)) + " Faculty Staff Records")
                self.ui.vcDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
                self.ui.lineEditXRateLimitReading.setText(str(self.vc.rate_limit_remaining))
                self.ui.lineEditXRateLimitResetReading.setText(str(self.vc.rate_limit_reset))
                self.debug_append_log("Found " + str(len(self.vcfsdata)) + " faculty staff records.")
        except:
            self.debug_append_log("Cannot get faculty staff from VC")

    def parse_vc_data(self):
        """
        Parse Action
        :return:
        """
        self.warn_user("Please be patient while the VC data is parsed, this may take a long time.  Press OK to begin")
        d = []
        for i in self.vcfsdata:
            h = v.Veracross()
            h.session.auth = (self.c["vcuser"], self.c["vcpass"])
            h.base_url = self.c["vcurl"]

            if i["household_fk"] > 0:
                hh = h.pull("households/" + str(i["household_fk"]))
            else:
                hh = None

            # Get field maps from the field maps textBrowser.
            try:
                field_maps = json.loads(self.ui.txt_fieldMap.toPlainText())
            except:
                self.warn_user("Invalid Field Maps! Check that field maps are in JSON format.")
                break

            a = {}
            for f in i:
                if field_maps.get(f):
                    a.update({f: str(i[f])})
            if hh:
                for fh in hh["household"]:
                    if field_maps.get(fh):
                        a.update({fh: str(hh["household"][fh])})

            d.insert(int(i["person_pk"]), a)
            del hh, h

        if len(d) > 0:
            self.ui.lineEditXRateLimitReading.setText(str(self.vc.rate_limit_remaining))
            self.ui.lineEditXRateLimitResetReading.setText(str(self.vc.rate_limit_reset))
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
            "vcurl": self.ui.vc_api_url.text(),
            "adpnetuser": self.ui.lineEdit_adpUsername.text(),
            "adpnetpass": self.ui.lineEdit_adpPassword.text(),
            "adpcertpath": self.ui.lineEdit_adpCertificatePath.text()
        }
        # Save settings
        config.save_settings(settings, "config")
        # Reload Settings
        self.c = config.load_settings("config")

    def save_field_map(self):
        """
        Saves the field maps to the config file
        :return:
        """
        # Save settings
        config.save_settings(self.ui.txt_fieldMap.toPlainText(), "fields")
        # Reload Settings
        self.field_maps = config.load_settings("fields")

    def debug_append_log(self, text):
        """
        Write to log window
        :param text:
        :return:
        """
        self.ui.textLog.moveCursor(QtGui.QTextCursor.End)
        self.ui.textLog.ensureCursorVisible()
        self.ui.textLog.insertHtml(text + "<br />")

    def warn_user(self, text):
        completeMsg = QtWidgets.QMessageBox()
        completeMsg.setIcon(QtWidgets.QMessageBox.Information)
        completeMsg.setText(text)
        completeMsg.exec_()

    def select_adp_certfile(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None,
                                                     "Select ADP API PFX Certificate",
                                                     "",
                                                     "Certificate (*.pfx)")
        self.ui.lineEdit_adpCertificatePath.setText(file[0])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
