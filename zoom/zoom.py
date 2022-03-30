import datetime
import requests
import json


from django_zoom_meetings import ZoomMeetings

class Zoom(ZoomMeetings):
    def __init__(self, api_key = None, secret_key = None, user_email = None):
        if not api_key and not secret_key and not user_email:
            with open('zoomkey.txt') as f:
                data = json.load(f)
                super().__init__(data["api_key"],data["secret_key"],data["user_email"])
        else:
            super().__init__(api_key,secret_key,user_email)

    def getlist(self):
        date = datetime.datetime.now()
        required_date_format = date
        url = 'https://api.zoom.us/v2/users/' + self.email + '/meetings'
        params = {"type": "upcoming", "page_size": 100}
        header = {'authorization': 'Bearer ' + self.request_token.decode()}
        zoom_create_meeting = requests.get(url, params=params, headers=header)
        return json.loads(zoom_create_meeting.text)

    def create(self, date:datetime.datetime, topic:str, duration:int, password:str='5025', **kwargs):
        required_date_format = date.strftime("%Y-%m-%dT%H:%M:%SZ")
        url = 'https://api.zoom.us/v2/users/' + self.email + '/meetings'
        jsonObj = {"topic": topic, "start_time": required_date_format, "duration": duration,
                   "password": password}
        header = {'authorization': 'Bearer ' + self.request_token}
        zoom_create_meeting = requests.post(url, json=jsonObj, headers=header)
        return json.loads(zoom_create_meeting.text)




