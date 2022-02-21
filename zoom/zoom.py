import datetime
import requests
import json
from django_zoom_meetings import ZoomMeetings

class Zoom(ZoomMeetings):
    def __init__(self):
        with open('zoomkey.txt') as f:
            data = json.load(f)
            super.__init__(data["api_key"],data["secret_key"],data["user_email"])

    def getlist(self):
        date = datetime.datetime.now()
        required_date_format = date
        url = 'https://api.zoom.us/v2/users/' + self.email + '/meetings'
        params = {"type": "upcoming", "page_size": 100}
        header = {'authorization': 'Bearer ' + self.request_token}
        zoom_create_meeting = requests.get(url, params=params, headers=header)
        return json.loads(zoom_create_meeting.text)
