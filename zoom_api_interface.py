import requests
import json
import datetime
import webbrowser
import time
import subprocess
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://api.zoom.us/v2"


# To read the zoom api, check https://marketplace.zoom.us/docs/api-reference/zoom-api/methods/

# The get_all_users function uses the get users part of the api
# You can read the parameters needed from the documentation
def get_all_users(token):
    payload = {'authorization': "Bearer " + token, 'content-type': "application/json"}
    # r = requests.get()
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    r = session.get(BASE_URL + "/users?status=active&page_size=300", headers=payload)
    result = json.loads(r.text)
    users = []

    for user in result["users"]:
        name = " ".join([user["first_name"], user["last_name"]])
        if name.strip() == "": name = user["email"]
        users.append({"id": user["id"], "name": name})

    return users


def get_recording_download_link(token, users, start_datetime, end_datetime):
    # This function gets all the links when given the list of user_ids
    # start_datetime and end_datetime have to be datetime objects

    diff_datetime = end_datetime - start_datetime
    payload = {'authorization': "Bearer " + token, 'content-type': "application/json"}

    recording_links = []
    for user in users:
        days_diff = divmod(diff_datetime.days, 30)
        for itertn in range(days_diff[0]):
            frm = datetime.datetime.strftime(start_datetime + datetime.timedelta(days=(itertn * 30)), "%Y-%m-%d")
            to = datetime.datetime.strftime(start_datetime + datetime.timedelta(days=((itertn + 1) * 30) - 1),
                                            "%Y-%m-%d")

            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            r = session.get(
                BASE_URL + f"/users/{user['id']}/recordings?page_size=300&mc=false&trash=false&from={frm}&to={to}&trash_type=meeting_recordings",
                headers=payload)
            result = json.loads(r.text)

            for meeting in result["meetings"]:
                name = user["name"].split(" ")[1]
                recording_dict = {"recording_name": name + ": " + meeting["topic"]}
                for file in meeting["recording_files"]:
                    if file["file_type"] == "MP4":
                        recording_dict["MP4_link"] = file["download_url"]
                    elif file["file_type"] == "M4A":
                        recording_dict["M4A_link"] = file["download_url"]
                recording_links.append(recording_dict)

        # Remainder
        if days_diff[1] != 0:
            frm = (datetime.datetime.strftime(start_datetime + datetime.timedelta(days=days_diff[0] * 30), "%Y-%m-%d"))
            to = datetime.datetime.strftime(start_datetime + datetime.timedelta(days=days_diff[0] * 30 + days_diff[1]),
                                            "%Y-%m-%d")

            r = requests.get(
                BASE_URL + f"/users/{user['id']}/recordings?page_size=300&mc=false&trash=false&from={frm}&to={to}&trash_type=meeting_recordings",
                headers=payload)
            result = json.loads(r.text)
            for meeting in result["meetings"]:
                name = user["name"].split(" ")[1]
                recording_dict = {"recording_name": name + ": " + meeting["topic"]}
                for file in meeting["recording_files"]:
                    if file["file_type"] == "MP4":
                        recording_dict["MP4_link"] = file["download_url"]
                    elif file["file_type"] == "M4A":
                        recording_dict["M4A_link"] = file["download_url"]
                recording_links.append(recording_dict)
    return recording_links


def get_sing_user_rec(token, user, start_datetime, end_datetime):
    # This function gets all the recordings when given the list of user_ids
    # start_datetime and end_datetime have to be datetime objects

    # start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    # end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    recording_links = []

    diff_datetime = end_datetime - start_datetime
    payload = {'authorization': "Bearer " + token, 'content-type': "application/json"}
    days_diff = divmod(diff_datetime.days, 30)
    for itertn in range(days_diff[0]):
        frm = datetime.datetime.strftime(start_datetime + datetime.timedelta(days=(itertn * 30)), "%Y-%m-%d")
        to = datetime.datetime.strftime(start_datetime + datetime.timedelta(days=((itertn + 1) * 30) - 1),
                                        "%Y-%m-%d")

        result = get_link_from_zoom(frm, payload, to, user)
        recording_links.extend(result)

    # Remainder
    if days_diff[1] != 0:
        frm = (
            datetime.datetime.strftime(start_datetime + datetime.timedelta(days=days_diff[0] * 30), "%Y-%m-%d"))
        to = datetime.datetime.strftime(
            start_datetime + datetime.timedelta(days=days_diff[0] * 30 + days_diff[1]),
            "%Y-%m-%d")

        result = get_link_from_zoom(frm, payload, to, user)
        recording_links.extend(result)

    return recording_links
    # url = "{{baseUrl}}/users/:userId/recordings?page_size=300&mc=false&trash=false&from=2022-09-01&to=2022-10-1&trash_type=meeting_recordings"


def get_link_from_zoom(start_datetime, payload, end_datetime, user):
    recording_links = []
    # r = requests.get(
    #     BASE_URL + f"/users/{user['id']}/recordings?page_size=300&mc=false&trash=false&from={start_datetime}&to={end_datetime}&trash_type=meeting_recordings",
    #     headers=payload)

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    r = session.get(
        BASE_URL + f"/users/{user['id']}/recordings?page_size=300&mc=false&trash=false&from={start_datetime}&to={end_datetime}&trash_type=meeting_recordings",
        headers=payload)
    result = json.loads(r.text)
    for meeting in result["meetings"]:
        name = user["name"].split(" ")[1]
        recording_dict = {"recording_name": name + ": " + meeting["topic"]}
        for file in meeting["recording_files"]:
            if file["file_type"] == "MP4":
                recording_dict["MP4_link"] = file["download_url"]
            elif file["file_type"] == "M4A":
                recording_dict["M4A_link"] = file["download_url"]
        recording_links.append(recording_dict)

    return recording_links


def download_single_rec(recording, key, get_mp4=True, get_m4a=False, client="Browser"):
    """

    :param recording: A dictionary in the format with keys -  name, MP4_link, M4A_link
    :param key: This is the api key
    :param get_mp4:
    :param get_m4a:
    :param client: Should be Browser or FDM
    """
    if get_mp4 and "MP4_link" in recording:
        if client == "Browser":
            webbrowser.open(url=recording["MP4_link"] + "?access_token=" + key, new=2)
            time.sleep(1)
        elif client == "FDM":
            subprocess.call(['C:/Program Files/Softdeluxe/Free Download Manager/fdm.exe',
                             recording["MP4_link"] + "?access_token=" + key])

    if get_m4a and "M4A_link" in recording:
        if client == "Browser":
            webbrowser.open(url=recording["M4A_link"] + "?access_token=" + key, new=2)
            time.sleep(1)
        elif client == "FDM":
            subprocess.call(['C:/Program Files/Softdeluxe/Free Download Manager/fdm.exe',
                             recording["M4A_link"] + "?access_token=" + key])


def export_links_to_file(recordings, export_location="", get_mp4=True, get_m4a=False):
    links = ["recording,file_type,link"]
    for recording in recordings:
        recording['recording_name'] = recording['recording_name'].replace(",", " ")
        if get_mp4:
            if "MP4_link" in recording:
                links.append(f"{recording['recording_name']},MP4,{recording['MP4_link']}")
        if get_m4a:
            if "M4A_link" in recording:
                links.append(f"{recording['recording_name']},M4A,{recording['M4A_link']}")

    if export_location == "":
        raise Exception("No Location specified")

    with open(export_location, 'w') as fp:
        for item in links:
            # write each item on a new line
            fp.write("%s\n" % item)
        print('Done')
