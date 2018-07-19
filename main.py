import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from mainwindow import Ui_MainWindow
import images
import veracross_api as v
import adp_api as adp
import config
import ast
import traceback


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Main(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.threadpool = QThreadPool()
        self.debug_append_log("Multithreading with maximum %d threads." % self.threadpool.maxThreadCount())

        # Setup vars
        self.vcfsdata = None
        self.vc_parsed_data = None
        self.adpfsdata = None
        self.adp_parsed_data = None
        self.last_sync_step = None

        # Ensure Sync Tab is active
        self.ui.tabs.setCurrentIndex(0)

        # Progress Bar Style
        progress_style = """
                QProgressBar {
                    border: 1px solid grey;
                    border-radius: 3px;
                    text-align: center;
                }

                QProgressBar::chunk {
                    background-color: lightgreen;
                    width: 5px;
                }"""
        self.ui.progressBarGetADPData.setStyleSheet(progress_style)
        self.ui.progressBarGetVCData.setStyleSheet(progress_style)
        self.ui.progressBarParseADPData.setStyleSheet(progress_style)
        self.ui.progressBarParseVCData.setStyleSheet(progress_style)

        self.ui.progressBarParseVCData.setValue(0)
        self.ui.progressBarParseADPData.setValue(0)
        self.ui.progressBarGetVCData.setValue(0)
        self.ui.progressBarGetADPData.setValue(0)

        # Set Images
        self.ui.logo_label.setPixmap(QPixmap(":/images/adp-vc-logo-100.png"))

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
        self.ui.btn_quit.clicked.connect(self.close_app)
        self.ui.btn_sync.clicked.connect(self.sync_data)
        # Map Field Tab Buttons
        self.ui.btn_saveFieldMap.clicked.connect(self.save_field_map)
        # Settings Buttons
        self.ui.settingsSave.clicked.connect(self.save_settings_button)
        self.ui.btn_pickerADPCertificate.clicked.connect(self.select_cert_file)
        self.ui.btn_pickerADPCertificateKey.clicked.connect(self.select_key_file)
        # Debug Tab Buttons
        self.ui.getVCDataButton.clicked.connect(self.get_vc_data_worker)
        self.ui.parseVCDataButton.clicked.connect(self.parse_vc_data_worker)
        self.ui.btn_getADPData.clicked.connect(self.get_adp_data_worker)
        self.ui.btn_parseADPData.clicked.connect(self.parse_adp_data_worker)

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

    def get_vc_data_worker(self):
        """
        Threaded trigger for the get_vc_data method below.
        :return:
        """
        worker = Worker(self.get_vc_data)
        worker.signals.finished.connect(self.get_vc_data_complete)
        self.threadpool.start(worker)

    def get_vc_data_complete(self):
        if len(self.vcfsdata) > 0:
            self.ui.vcFSRecordCount.setText(str(len(self.vcfsdata)))
            self.ui.lineEditXRateLimitReading.setText(str(self.vc.rate_limit_remaining))
            self.ui.lineEditXRateLimitResetReading.setText(str(self.vc.rate_limit_reset))
            self.debug_append_log("Found %d faculty staff records in Veracross." % len(self.vcfsdata))
            self.ui.progressBarGetVCData.setValue(100)

            if self.last_sync_step is "begin":
                self.last_sync_step = "get_vc_data"
                self.parse_vc_data_worker()
            else:
                # Enable next step
                self.ui.parseVCDataButton.setEnabled(True)

    def get_vc_data(self):
        """
        Get VC Data
        :return:
        """
        try:
            self.vc = v.Veracross(self.c)
            self.vcfsdata = self.vc.pull("facstaff")
        except:
            self.debug_append_log("Cannot get faculty staff from Veracross")
            e = sys.exc_info()[0]
            self.debug_append_log(e)
            return None

    def parse_vc_data_worker(self):
        """
        Threaded trigger for the get_vc_data method below.
        :return:
        """
        worker = Worker(self.parse_vc_data)
        worker.signals.finished.connect(self.parse_vc_data_complete)
        self.threadpool.start(worker)

    def parse_vc_data_complete(self):
        try:
            if len(self.vc_parsed_data) > 0:
                # Send results to textedit
                self.ui.vcResultsTextEdit.setText(str(self.vc_parsed_data))
                self.debug_append_log("Veracross data parsed.")
                if self.last_sync_step is "get_vc_data":
                    self.last_sync_step = "parse_vc_data"
                    self.get_adp_data_worker()
                else:
                    # Enable next step
                    self.ui.btn_getADPData.setEnabled(True)
        except:
            print("Error parsing Veracross data.")

    def parse_vc_data(self):
        """
        Parse Veracross Action
        :return:
        """
        # Get field maps from the field maps textBrowser.
        try:
            field_maps = ast.literal_eval(config.load_settings("fields"))
        except:
            self.warn_user("Invalid Field Maps! Check README for more information.")
            e = sys.exc_info()[0]
            self.debug_append_log(e)
            return None

        try:
            d = {}
            increment = 100 / len(self.vcfsdata)
            progress = increment
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
                progress = progress + increment

                # Update UI with rate limits
                self.ui.lineEditXRateLimitReading.setText(str(h.rate_limit_remaining))
                self.ui.lineEditXRateLimitResetReading.setText(str(h.rate_limit_reset))
                self.ui.progressBarParseVCData.setValue(int(progress))
                del hh, h
        except:
            self.debug_append_log("Unable to parse Veracross data.")
            e = sys.exc_info()[0]
            self.debug_append_log(e)
            return None

        if len(d) > 0:
            # Store parsed data in self
            self.vc_parsed_data = d

    def get_adp_data_worker(self):
        """
        Threaded trigger for the get_vc_data method below.
        :return:
        """
        worker = Worker(self.get_adp_data)
        worker.signals.finished.connect(self.get_adp_data_complete)
        self.threadpool.start(worker)

    def get_adp_data_complete(self):
        if len(self.adpfsdata) > 0:
            self.ui.adpRecordCount.setText(str(len(self.adpfsdata)))
            self.debug_append_log("Found %d employee records in ADP." % len(self.adpfsdata))
            # Progress Bar
            self.ui.progressBarGetADPData.setValue(100)

            if self.last_sync_step is "parse_vc_data":
                self.last_sync_step = "get_adp_data"
                self.parse_adp_data_worker()
            else:
                # Enable next step
                self.ui.btn_parseADPData.setEnabled(True)

    def get_adp_data(self):
        try:
            # Since we cannot get progress.  Set Progress to 50 so user is aware.
            self.ui.progressBarGetADPData.setValue(int(50))
            a = adp.Adp(self.c)
            self.adpfsdata = a.workers()
        except:
            self.debug_append_log("Unable to get ADP data.")
            e = sys.exc_info()[0]
            self.debug_append_log(e)
            return None

    def parse_adp_data_worker(self):
        """
        Threaded trigger for the get_vc_data method below.
        :return:
        """
        worker = Worker(self.parse_adp_data)
        worker.signals.finished.connect(self.parse_adp_data_complete)
        self.threadpool.start(worker)

    def parse_adp_data_complete(self):
        try:
            if len(self.adp_parsed_data) > 0:
                # Notify the interface
                self.ui.adpResultsTextEdit.setText(str(self.adp_parsed_data))
                self.debug_append_log("ADP data parse complete.")
                if self.last_sync_step is "get_adp_data":
                    self.last_sync_step = "complete"
                    self.sync_data_ready()
        except:
            self.debug_append_log("Error parsing ADP Data.")

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
        increment = 100 / len(self.adpfsdata)
        progress = increment
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
                d.update({int(vcid): a})

            # Update progress bar
            progress = progress + increment
            self.ui.progressBarParseADPData.setValue(int(progress))

        if len(d) > 0:
            # Store parsed data in self
            self.adp_parsed_data = d

    def sync_data(self):

        if not self.ask_user_continue("This process will take a while to complete. Continue?"):
            return None

        self.last_sync_step = "begin"
        self.get_vc_data_worker()

    def sync_data_ready(self):
        intersect = []
        for k in self.adp_parsed_data.keys():
            if k in self.vc_parsed_data.keys():
                intersect.append(int(k))

        for i in intersect:
            vc_set = set(self.vc_parsed_data[i].items())
            adp_set = set(self.adp_parsed_data[i].items())

            data_diff = vc_set - adp_set

            # Append to UI
            for s in data_diff:
                self.ui.txt_SyncDataResults.moveCursor(QTextCursor.End)
                self.ui.txt_SyncDataResults.insertPlainText(str(self.vc_parsed_data[i]['first_name']) +
                                                            " " +
                                                            str(self.vc_parsed_data[i]['last_name']) +
                                                            ": " +
                                                            str(s) +
                                                            "\n"
                                                            )

    def close_app(self):
        self.close()

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
        self.ui.textLog.moveCursor(QTextCursor.End)
        self.ui.textLog.ensureCursorVisible()
        self.ui.textLog.insertHtml(text + "<br />")

    def warn_user(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(text)
        msg.exec_()

    def ask_user_continue(self, text):
        msg = QMessageBox.question(self,
                                   "Confirm",
                                    text,
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.Yes)
        if msg == QMessageBox.Yes:
            return True
        else:
            return False

    def select_cert_file(self):
        file = QFileDialog.getOpenFileName(None,
                                           "Select ADP API Certificate (Base64 PEM)",
                                           "",
                                           "Certificate (*.pem)")
        self.ui.lineEdit_adpCertificatePEMPath.setText(file[0])

    def select_key_file(self):
        """
        Selects a file
        :return:
        """
        file = QFileDialog.getOpenFileName(None,
                                           "Select ADP API Certificate Key",
                                            "",
                                            "Certificate (*.key)")
        self.ui.lineEdit_adpCertificateKeyPath.setText(file[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
