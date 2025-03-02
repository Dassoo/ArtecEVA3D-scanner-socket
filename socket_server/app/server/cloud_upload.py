import sys
import os
import requests
from datetime import date

sys.path.append('.')


def sweethive_upload(folder, path_to_current_project, headers):
    url = f'http://localhost:3001/task?isAppCall=true'
    payload = {
        "user_id": 17564,  # fixed value
        "device_id": "1",  # fixed value
        "hive_id": "27912",  # fixed value
        "project_context_id": "28145",  # fixed value
        "project_title": f"{folder}",  # project name
        "local_file_path": f"{os.getcwd()}/{path_to_current_project}",  # folder to upload
        "scan_on": str(date.today()),  # current date
        "scan_at": "MUSEUM",  # scan location (optional)
        "note": ""  # additional notes (optional)
    }

    try:
        req = requests.post(url, json=payload, headers=headers)
        req.raise_for_status()
        print(req.text)
        print(f"Upload successful!")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
