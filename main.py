import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from mainwindow import Ui_MainWindow
import images
import veracross_api as v
import adp_api as adp
import config
import json
import ast

class Main(QtWidgets.QMainWindow):
    def __init__(self):

        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set Images
        self.ui.logo_label.setPixmap(QtGui.QPixmap(":/images/adp-vc-logo-100.png"))
        self.ui.vcDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))
        self.ui.vcParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))
        self.ui.adpDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))
        self.ui.adpParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/red_status.png"))

        # Gather Config
        self.c = config.load_settings("config")
        self.field_maps = ast.literal_eval(config.load_settings("fields"))

        # Setup LineEdit Text
        if "vcuser" in self.c.keys():
            self.ui.vc_api_user.setText(self.c["vcuser"])
        if "vcpass" in self.c.keys():
            self.ui.vc_api_pass.setText(self.c["vcpass"])
        if "vcurl" in self.c.keys():
            self.ui.vc_api_url.setText(self.c["vcurl"])
        if "adpnetuser" in self.c.keys():
            self.ui.lineEdit_adpUsername.setText(self.c["adpnetuser"])
        if "adpnetpass" in self.c.keys():
            self.ui.lineEdit_adpPassword.setText(self.c["adpnetpass"])
        if "adpcertpath" in self.c.keys():
            self.ui.lineEdit_adpCertificatePEMPath.setText(self.c["adpcertpath"])
        if "adpcertkeypath" in self.c.keys():
            self.ui.lineEdit_adpCertificateKeyPath.setText(self.c["adpcertkeypath"])
        if "adpvccustomfieldname" in self.c.keys():
            self.ui.lineEdit_adpVCCustomFieldName.setText(self.c["adpvccustomfieldname"])
        if self.field_maps:
            self.ui.txt_fieldMap.setText(str(self.field_maps))

        # Connect buttons to methods
        # Sync Tab Buttons
        self.ui.getVCDataButton.clicked.connect(self.get_vc_data)
        self.ui.parseVCDataButton.clicked.connect(self.parse_vc_data)
        self.ui.btn_getADPData.clicked.connect(self.get_adp_data)
        self.ui.btn_parseADPData.clicked.connect(self.parse_adp_data)
        # Map Field Tab Buttons
        self.ui.btn_saveFieldMap.clicked.connect(self.save_field_map)
        # Settings Buttons
        self.ui.settingsSave.clicked.connect(self.save_settings_button)
        self.ui.btn_pickerADPCertificate.clicked.connect(self.select_cert_file)
        self.ui.btn_pickerADPCertificateKey.clicked.connect(self.select_key_file)

        # Enable Buttons
        self.ui.getVCDataButton.setEnabled(True)

    def get_nested_dict(self, data, path, default=None):
        keys = path.split("/")
        val = None
        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(data, key, default)
            if not val:
                break;
        return val

    def map_field(self, field):
        """
        Look in field maps for what key to store data in.
        :param field:
        :return:
        """
        for k, v in self.field_maps.items():
            if field in v:
                return k

    def get_vc_data(self):
        """
        Get VC Data
        :return:
        """
        try:
            self.vcfsdata = []
            self.vc = v.Veracross(self.c)
            self.vcfsdata = self.vc.pull("facstaff")

            if len(self.vcfsdata) > 0:
                self.ui.vcFSRecordCount.setText(str(len(self.vcfsdata)) + " Faculty Staff Records")
                self.ui.vcDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
                self.ui.lineEditXRateLimitReading.setText(str(self.vc.rate_limit_remaining))
                self.ui.lineEditXRateLimitResetReading.setText(str(self.vc.rate_limit_reset))
                self.debug_append_log("Found " + str(len(self.vcfsdata)) + " faculty staff records in VC.")
                # Enable next step
                self.ui.parseVCDataButton.setEnabled(True)
        except:
            self.debug_append_log("Cannot get faculty staff from VC")

    def parse_vc_data(self):
        """
        Parse Veracross Action
        :return:
        """
        self.warn_user("Please be patient while the VC data is parsed, this may take a long time.  "
                       "Press OK to begin")

        # Get field maps from the field maps textBrowser.
        try:
            field_maps = ast.literal_eval(config.load_settings("fields"))
        except:
            self.warn_user("Invalid Field Maps! Check README for more information.")
            return None

        d = {}
        for i in self.vcfsdata:
            h = v.Veracross(self.c)

            if i["household_fk"] > 0:
                hh = h.pull("households/" + str(i["household_fk"]))
            else:
                hh = None

            a = {}
            for f in i:
                if field_maps.get(f):
                    a.update({f: str(i[f])})
            if hh:
                for fh in hh["household"]:
                    if field_maps.get(fh):
                        a.update({fh: str(hh["household"][fh])})

            d.update({int(i["person_pk"]): a})
            del hh, h

        if len(d) > 0:
            self.ui.lineEditXRateLimitReading.setText(str(self.vc.rate_limit_remaining))
            self.ui.lineEditXRateLimitResetReading.setText(str(self.vc.rate_limit_reset))
            self.debug_append_log("Veracross data parse complete.")
            self.ui.vcParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
            self.ui.vcResultsTextEdit.setText(str(d))
            # Enable next step
            self.ui.btn_getADPData.setEnabled(True)

    def get_adp_data(self):
        try:
            a = adp.Adp(self.c)
            self.adpfsdata = a.workers()
            if len(self.adpfsdata) > 0:
                self.ui.adpRecordCount.setText(str(len(self.adpfsdata)) + " Employee Records")
                self.ui.adpDataFSStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
                self.debug_append_log("Found " + str(len(self.adpfsdata)) + " employee records in ADP.")
                # Enable next step
                self.ui.btn_parseADPData.setEnabled(True)
        except:
            return None

    def parse_adp_data(self):
        d = {}

        if not self.c["adpvccustomfieldname"]:
            return None

        # Get field maps from the field maps textBrowser.
        try:
            field_maps = ast.literal_eval(config.load_settings("fields"))
        except:
            self.warn_user("Invalid Field Maps! Check README for more information.")
            return None

        for i in self.adpfsdata:
            a = {}
            # Get VC ID from field set in settings
            # VC Person_PK must be a custom ADP field.
            if self.get_nested_dict(i, "person/customFieldGroup/stringFields"):
                for s in i['person']['customFieldGroup']['stringFields']:
                    if s['nameCode']['shortName'] == self.c["adpvccustomfieldname"]:
                        vcid = s['stringValue']
            if vcid:
                for f in field_maps:
                    a.update({f: self.get_nested_dict(i, str(field_maps[f]))})
                d.update({vcid: a})

        if len(d) > 0:
            self.ui.adpParseStatusLabel.setPixmap(QtGui.QPixmap(":/images/green_status.png"))
            self.ui.adpResultsTextEdit.setText(str(d))

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
            "adpcertpath": self.ui.lineEdit_adpCertificatePEMPath.text(),
            "adpcertkeypath": self.ui.lineEdit_adpCertificateKeyPath.text(),
            "adpvccustomfieldname": self.ui.lineEdit_adpVCCustomFieldName.text()
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

    def select_cert_file(self):
        file = QtWidgets.QFileDialog.getOpenFileName(None,
                                                     "Select ADP API Certificate (Base64 PEM)",
                                                     "",
                                                     "Certificate (*.pem)")
        self.ui.lineEdit_adpCertificatePEMPath.setText(file[0])

    def select_key_file(self):
        """
        Selects a file
        :return:
        """
        file = QtWidgets.QFileDialog.getOpenFileName(None,
                                                     "Select ADP API Certificate Key",
                                                     "",
                                                     "Certificate (*.key)")
        self.ui.lineEdit_adpCertificateKeyPath.setText(file[0])


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
