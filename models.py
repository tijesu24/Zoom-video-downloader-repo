import sys
from pathlib import Path

import jwt
from PyQt5.QtCore import QTimer, QSettings

import settings
from front_end_mvc import *
from process_dialog import *
from threads import *
import datetime
import os


class Downloader(Ui_MainWindow):
    def __init__(self):
        super(Downloader, self).__init__()
        self.jwtGenPending = True
        self.link_list = []
        self.user_list = []

    def function_bind(self):

        def button_user_select():
            if self.users_comboBox.currentText():
                self.adjust_user_selection("select", self.users_comboBox.currentText())

        # function bindings for buttons
        self.get_user_button.clicked.connect(lambda: self.fill_user_list())
        self.select_names_pushButton.clicked.connect(
            lambda: button_user_select())
        self.no_users_button.clicked.connect(lambda: self.adjust_user_selection("deselect_all"))
        self.all_users_button.clicked.connect(lambda: self.adjust_user_selection("select_all"))
        self.get_links_button.clicked.connect(lambda: self.fill_rec_list())
        self.no_links_button.clicked.connect(lambda: self.adjust_link_selection("deselect_all"))
        self.all_links_button.clicked.connect(lambda: self.adjust_link_selection("select_all"))
        self.csv_export_button.clicked.connect(lambda: self.export_csv())
        self.browser_download_button.clicked.connect(lambda: self.download_links_browser())
        self.users_listWidget.itemClicked.connect(self.user_clicked)
        self.links_listWidget.itemSelectionChanged.connect(self.adjust_selection_count_text)
        self.settings_button.clicked.connect(lambda: self.start_settings_dialog())

        self.updateSettingsParameters()

    def adjust_user_selection(self, action, item=None):
        selected_users = [self.users_listWidget.item(x).text() for x in range(self.users_listWidget.count())]

        if action == "deselect":
            index = selected_users.index(item)
            self.users_listWidget.takeItem(index)
        elif action == "select":
            if item not in [i for i in selected_users]:
                self.users_listWidget.addItem(QtWidgets.QListWidgetItem(item))
        elif action == "select_all":
            self.users_listWidget.clear()
            name_list = [item["name"] for item in self.user_list]
            name_list.sort()
            self.users_listWidget.addItems(name_list)
        elif action == "deselect_all":
            self.users_listWidget.clear()

        self.users_listWidget.update()

    def adjust_link_selection(self, action):
        if action == "select_all":
            self.links_listWidget.selectAll()
        elif action == "deselect_all":
            self.links_listWidget.clearSelection()

    def fill_user_list(self):
        if self.TOKEN == "":
            self.show_error_dialog('Check jwt key and secret in settings')
            return
        status = self.jwt_token_check()
        if status != 0:
            return

        def populate_user_list(user_list):
            self.user_list = sorted(user_list, key=lambda d: d['name'].lower())
            self.users_comboBox.addItems([x['name'] for x in self.user_list])
            self.users_comboBox.update()

        self.clearAll()
        self.process_dialog = Process_Dialog("Getting users", parent=self, closable=False)
        thread = GetUserProcess(self.TOKEN)

        thread.payload.connect(populate_user_list)

        thread.finished.connect(thread.deleteLater)
        thread.progress.connect(self.reportProgress)
        thread.progress.connect(self.write_log_file)
        thread.finished.connect(lambda: self.cancel_status_dialog(1))
        thread.finished.connect(lambda: self.process_dialog.setLoadingCursor(False))
        thread.error.connect(self.show_error_dialog)

        thread.start()
        self.process_dialog.exec()

    def show_error_dialog(self, error_msg):
        self.error_dialog = QtWidgets.QMessageBox(self)
        self.error_dialog.setWindowTitle("Error")
        self.error_dialog.setText(error_msg)
        self.error_dialog.exec()

    def fill_rec_list(self):
        if not self.users_listWidget.count():
            self.show_error_dialog("No user selected")
            return
        status = self.jwt_token_check()
        if status != 0:
            return

        selected_names = [self.users_listWidget.item(x).text() for x in range(self.users_listWidget.count())]

        def populate_link_widget(recordings):
            self.links_listWidget.clear()
            self.links_listWidget.addItems([i["recording_name"] for i in recordings])
            self.link_list = recordings
            self.adjust_selection_count_text()

        selected_userdicts = [i for i in self.user_list if i["name"] in selected_names]
        self.process_dialog = Process_Dialog("Getting links", parent=self)
        thread = GetRecordingsProcess(token=self.TOKEN, users=selected_userdicts,
                                      start_datetime=self.from_dateEdit.dateTime().toPyDateTime(),
                                      end_datetime=self.to_dateEdit.dateTime().toPyDateTime())

        thread.payload.connect(populate_link_widget)
        thread.started.connect(lambda: self.links_listWidget.clear())
        thread.finished.connect(thread.deleteLater)
        thread.dialog_progress.connect(self.reportProgress)
        thread.log_progress.connect(self.write_log_file)
        thread.finished.connect(lambda: self.cancel_status_dialog(1))
        thread.finished.connect(lambda: self.process_dialog.setLoadingCursor(False))
        thread.error.connect(self.show_error_dialog)
        thread.error.connect(self.write_log_file)

        # Connecting the cancel button
        self.process_dialog.pushButton_2.clicked.connect(lambda: thread.stop_execution())
        self.process_dialog.pushButton_2.clicked.connect(lambda: self.process_dialog.done(2))

        thread.start()
        self.process_dialog.exec()

    def user_clicked(self, item):
        self.adjust_user_selection("deselect", item.text())

    def export_csv(self):
        if not len(self.link_list):
            self.show_error_dialog("No recording selected")

        else:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(caption="Save links to csv file",
                                                                filter="CSV files (*.csv)")
            if filename.strip() != "":
                selected_record_names = [self.links_listWidget.indexFromItem(i) for i in
                                         self.links_listWidget.selectedItems()]
                recordings_to_export = [self.link_list[i.row()] for i in selected_record_names]

                self.process_dialog = Process_Dialog("Exporting to text file", parent=self)
                thread = ExportCSVProcess(recordings=recordings_to_export, filename=filename,
                                          get_mp4=self.mp4_checkBox.isChecked(),
                                          get_m4a=self.m4a_checkBox.isChecked()
                                          )

                thread.finished.connect(thread.deleteLater)
                thread.progress.connect(self.reportProgress)
                thread.progress.connect(self.write_log_file)
                thread.finished.connect(lambda: self.cancel_status_dialog(1))
                thread.error.connect(self.show_error_dialog)

                thread.start()
                self.process_dialog.exec()

    def download_links_browser(self):

        if not len(self.link_list):
            self.show_error_dialog("No recording selected")
            return
        if self.TOKEN == "":
            self.show_error_dialog("No token")
            return

        status = self.jwt_token_check()
        if status != 0:
            return

        def set_thread_continue():
            thread.continue_download = True

        selected_record_names = [self.links_listWidget.indexFromItem(i) for i in self.links_listWidget.selectedItems()]
        recordings_to_download = [self.link_list[i.row()] for i in selected_record_names]

        self.process_dialog = Process_Dialog("Getting links", continuable=True, closable=False, parent=self)
        thread = DownloadBrowserProcess(key=self.TOKEN, recordings=recordings_to_download,
                                        get_mp4=self.mp4_checkBox.isChecked(),
                                        get_m4a=self.m4a_checkBox.isChecked(),
                                        cluster=self.no_simulDwnld)

        thread.finished.connect(thread.deleteLater)
        thread.progress.connect(self.reportProgress)
        thread.progress.connect(self.write_log_file)
        thread.finished.connect(lambda: self.cancel_status_dialog(1))
        # Connecting the continue button
        self.process_dialog.pushButton_3.clicked.connect(lambda: set_thread_continue())
        thread.paused.connect(lambda: self.process_dialog.pushButton_3.setEnabled(True))
        thread.paused.connect(lambda: self.process_dialog.setLoadingCursor(False))
        thread.continued.connect(lambda: self.process_dialog.pushButton_3.setEnabled(False))
        thread.continued.connect(lambda: self.process_dialog.setLoadingCursor(True))
        thread.error.connect(self.show_error_dialog)
        # Connecting the cancel button
        self.process_dialog.pushButton_2.clicked.connect(lambda: thread.stop_execution())
        self.process_dialog.pushButton_2.clicked.connect(lambda: self.process_dialog.done(2))
        thread.start()
        self.process_dialog.exec()

    def reportProgress(self, msg):
        self.process_dialog.text_label.setText(str(msg))
        print("Dialog message: " + msg)
        # self.process_dialog.update()

    def cancel_status_dialog(self, status):
        """
        This function waits some seconds and then closes the status dialog
        :param status: I want to make 0 be ok status, 1 be error status and 2 be
        cancel status
        :return:
        """

        def on_cancel():
            self.process_dialog.done(status)

        timer = QTimer(self)
        timer.timeout.connect(lambda: on_cancel())
        timer.timeout.connect(timer.stop)
        timer.start(2000)

    def adjust_selection_count_text(self):
        selected = len(self.links_listWidget.selectedItems())
        total = len(self.link_list)
        self.selected_recs_label.setText(f"{selected}/{total} recordings selected")

    def start_settings_dialog(self):
        settingsDialog = settings.Settings_Dialog_extd(self)
        settingsDialog.buttonBox.accepted.connect(self.updateSettingsParameters)
        settingsDialog.jwt_modified.connect(self.set_jwtGenPending)
        settingsDialog.exec()

    def updateSettingsParameters(self):
        self.settings = QSettings('ZVD', 'tjo')

        # Get settings values
        self.jwtSecret = self.settings.value("jwtSecret")
        self.jwtKey = self.settings.value("jwtKey")
        self.logFileDir = self.settings.value("logFileLocation")
        self.no_simulDwnld = self.settings.value("no_simulDwnld", type=int)

        if self.jwtGenPending:
            self.generate_jwt_token()

    def set_jwtGenPending(self):
        self.jwtGenPending = True

    def write_log_file(self, message):

        # if folder does not exist create it
        if not os.path.exists(self.logFileDir):
            os.mkdir(self.logFileDir)
        # Open a file with access mode 'a'
        log_file_location = Path(self.logFileDir).joinpath("zvd_log.txt")
        file_object = None
        try:
            file_object = open(str(log_file_location), 'a+')
        except FileNotFoundError:
            self.show_error_dialog("Log file not found")

        except PermissionError:
            self.show_error_dialog("Cannot write to log file\n"
                                   "Enable permissions for program or disable antivirus")

        if file_object:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_object.write(current_datetime + ": " + message + "\n")

            # Close the file
            file_object.close()

    def jwt_token_check(self):
        """
        Checks if we can generate token or token is valid and tries to generate token if not valid.
        If there are any issues, it raises the corresponding error dialog
        if the token is valid, it returns 0 else -1
        :return:
        """
        if self.TOKEN == "" or datetime.datetime.now() > self.TOKEN_expiry:
            status = self.generate_jwt_token()
            if status == -1:
                self.show_error_dialog("Invalid Key and/or Secret")
                return -1
            elif status == -2:
                self.show_error_dialog("Network error")
                return -1

        return 0

    def generate_jwt_token(self):
        """
        The function generates a token and if successful, returns 0
        if either key or secret is invalid, it returns -1
        if network issue, it returns -2
        :return:
        """

        self.TOKEN = ""
        self.TOKEN_expiry = datetime.datetime.now()

        if not (self.jwtKey and self.jwtSecret):
            return -1

        self.TOKEN_expiry = datetime.datetime.now() + datetime.timedelta(hours=2)
        payload = {
            'iss': self.jwtKey,
            'exp': self.TOKEN_expiry
        }
        try:
            self.TOKEN = jwt.encode(payload, self.jwtSecret)
            self.jwtGenPending = False
        except Exception as e:
            print(e)

    def clearAll(self):
        self.user_list.clear()
        self.users_comboBox.clear()
        self.users_listWidget.clear()

        self.link_list.clear()
        self.links_listWidget.clear()


def window():
    app = QtWidgets.QApplication(sys.argv)
    custom_font = QtGui.QFont()
    custom_font.setWeight(12)
    app.setFont(custom_font, "QLabel")
    app.setFont(custom_font, "QComboBox")
    ui = Downloader()
    ui.setupUi()
    ui.function_bind()
    ui.show()
    sys.exit(app.exec_())


window()
