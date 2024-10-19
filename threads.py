import datetime
import json

import requests
from PyQt5.QtCore import pyqtSignal, QThread

from zoom_api_interface import get_link_from_zoom, export_links_to_file, BASE_URL, download_single_rec


class GetRecordingsProcess(QThread):
    payload = pyqtSignal(list)
    dialog_progress = pyqtSignal(str)
    log_progress = pyqtSignal(str)
    error = pyqtSignal(str)
    stop = False
    link_list = []

    def __init__(self, token, users, start_datetime, end_datetime, parent=None, **kwargs):

        self.TOKEN = token
        self.selected_userdicts = users
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        super().__init__(parent, **kwargs)

    def run(self):
        """Long-running task."""

        self.started.emit()
        self.link_list = []
        self.log_announce()

        for i, user in enumerate(self.selected_userdicts):
            self.dialog_announce(i, user)
            try:
                self.get_sing_user_rec(i, token=self.TOKEN, user=user,
                                       start_datetime=self.start_datetime,
                                       end_datetime=self.end_datetime)
            except OSError as e:  # Connection error
                self.error.emit("No connection. Check connection and try again. \n" + repr(e))
                self.finished.emit()
                return
            except Exception:
                self.error.emit("An error occurred")
                self.finished.emit()
                return

            if self.stop:
                return

        if not self.link_list:  # If nothing is found
            self.dialog_progress.emit("No recording found with the parameters given")
        else:  # Done and found stuff

            self.dialog_progress.emit(f"Done with search. Found {len(self.link_list)} recordings")
            self.log_progress.emit(f"Done with search. Found {len(self.link_list)} recordings")
        self.payload.emit(self.link_list)
        self.finished.emit()

    def get_sing_user_rec(self, cnt, token, user, start_datetime, end_datetime):
        # This function gets all the recordings when given the list of user_ids
        # start_datetime and end_datetime have to be datetime objects

        # start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        # end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        if self.stop:
            return

        diff_datetime = end_datetime - start_datetime
        payload = {'authorization': "Bearer " + token, 'content-type': "application/json"}
        days_diff = divmod(diff_datetime.days, 30)
        for itertn in range(days_diff[0]):
            if self.stop:
                return

            frm = datetime.datetime.strftime(start_datetime + datetime.timedelta(days=(itertn * 30)), "%Y-%m-%d")
            to = datetime.datetime.strftime(start_datetime + datetime.timedelta(days=((itertn + 1) * 30) - 1),
                                            "%Y-%m-%d")

            result = get_link_from_zoom(frm, payload, to, user)
            self.link_list.extend(result)
            if self.stop:
                return
            if result:
                self.dialog_announce(cnt, user)

        # Remainder
        if days_diff[1] != 0:
            frm = (
                datetime.datetime.strftime(start_datetime + datetime.timedelta(days=days_diff[0] * 30), "%Y-%m-%d"))
            to = datetime.datetime.strftime(
                start_datetime + datetime.timedelta(days=days_diff[0] * 30 + days_diff[1]),
                "%Y-%m-%d")

            result = get_link_from_zoom(frm, payload, to, user)
            self.link_list.extend(result)

            if self.stop:
                return

            if result:
                self.dialog_announce(cnt, user)

    def log_announce(self):

        self.log_progress.emit(f"Getting recording for {len(self.selected_userdicts)} selected users.")

    def dialog_announce(self, cnt, user):
        links_gotten = len(self.link_list)
        self.dialog_progress.emit(
            f"""Getting recordings for {user['name']} ({cnt + 1}/{len(self.selected_userdicts)}). 
{links_gotten} recording{'' if links_gotten == 1 else "s"} found so far""")

    def stop_execution(self):
        self.stop = True


class GetUserProcess(QThread):
    payload = pyqtSignal(list)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)
    TOKEN = ""

    def __init__(self, TOKEN, parent=None, **kwargs):
        self.TOKEN = TOKEN
        super().__init__(parent, **kwargs)

    def run(self):
        """Long-running task."""

        self.started.emit()
        self.progress.emit("Getting all users")
        user_list = self.get_all_users(self.TOKEN)
        if user_list: self.progress.emit(f"Done. Found {len(user_list)} users.")
        self.payload.emit(user_list)
        self.finished.emit()

    # The get_all_users function uses the get users part of the api
    # You can read the parameters needed from the documentation
    def get_all_users(self, token):
        payload = {'authorization': "Bearer " + token, 'content-type': "application/json"}
        try:
            r = requests.get(BASE_URL + "/users?status=active&page_size=300", headers=payload)
        except OSError:  # Connection error
            self.error.emit("No connection. Check network and try again")
            return []

        # print(r.text)
        result = json.loads(r.text)
        users = []
        if r.status_code == 401:  # if key error
            self.error.emit("Invalid Authorization credentials")
            return users
        elif r.status_code == 400 and "message" in result:  # If there is another error
            self.error.emit(result["message"])
            return users

        for user in result["users"]:
            name = " ".join([user["first_name"], user["last_name"]])
            if name.strip() == "": name = user["email"]
            users.append({"id": user["id"], "name": name})

        return users


class ExportCSVProcess(QThread):
    progress = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, recordings, get_mp4, get_m4a, filename, parent=None, **kwargs):
        self.recordings = recordings
        self.get_mp4 = get_mp4
        self.get_m4a = get_m4a
        self.filename = filename
        super().__init__(parent, **kwargs)

    def run(self):
        """Long-running task."""

        self.started.emit()
        if self.filename.strip() != "":

            self.progress.emit(f"Exporting to {self.filename}")
            try:
                export_links_to_file(self.recordings, self.filename,
                                     get_mp4=self.get_mp4,
                                     get_m4a=self.get_m4a)
            except PermissionError:  # Connection error
                self.error.emit("Can't write to file.\n"
                                "Change filename or check permissions and try again")
                self.finished.emit()
                return

            self.progress.emit("Done with export")

        else:
            self.progress.emit("Invalid filename")

        self.finished.emit()


class DownloadBrowserProcess(QThread):
    progress = pyqtSignal(str)
    paused = pyqtSignal()
    continued = pyqtSignal()
    error = pyqtSignal(str)
    stop = False

    def __init__(self, recordings, key, get_mp4, get_m4a, cluster, parent=None, **kwargs):
        self.recordings = recordings
        self.key = key
        self.get_mp4 = get_mp4
        self.get_m4a = get_m4a
        self.cluster = cluster
        self.continue_download = False
        super().__init__(parent, **kwargs)

    def run(self):
        """Long-running task."""
        self.started.emit()
        for i, recording in enumerate(self.recordings):
            self.progress.emit(f"Downloading {recording['recording_name']} ({i + 1}/{len(self.recordings)})")

            try:
                download_single_rec(recording, self.key, self.get_mp4, self.get_m4a, client="Browser")
            except Exception:
                self.error.emit("An error occurred")
                self.finished.emit()
                return

            if self.stop:  # Check for canceled
                self.finished.emit
                return

            if (i + 1) % self.cluster == 0:
                self.paused.emit()
                self.progress.emit(f"Downloaded ({i + 1}/{len(self.recordings)}). Click button to continue")
                while not self.continue_download:
                    if self.stop:  # Check for canceled
                        self.finished.emit
                        return
                    pass
                else:
                    self.continued.emit()
                    self.continue_download = False

        self.finished.emit()

    def stop_execution(self):
        self.stop = True
