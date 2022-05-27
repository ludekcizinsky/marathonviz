import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from .config import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN


def _get_access_token():
  """
  Adapted from:
  https://github.com/franchyze923/Code_From_Tutorials/blob/master/Strava_Api/strava_api.py
  """

  auth_url = "https://www.strava.com/oauth/token" 

  payload = {
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
      'refresh_token':  REFRESH_TOKEN,
      'grant_type': "refresh_token",
      'f': 'json'
  }

  
  res = requests.post(auth_url, data=payload, verify=False)
  access_token = res.json()['access_token']

  return access_token


def list_activities(after, before):
 
  access_token = _get_access_token()

  url = "https://www.strava.com/api/v3/athlete/activities"
  header = {'Authorization': 'Bearer ' + access_token}
  param = {'per_page': 200, 'page': 1, 'after': after, 'before': before}
  activities = requests.get(url, headers=header, params=param).json()

  return activities

def get_activity_info(activity_id):

  access_token = _get_access_token()

  url = f"https://www.strava.com/api/v3/activities/{activity_id}"
  header = {'Authorization': 'Bearer ' + access_token}
  param = {'include_all_efforts': True}
  activity = requests.get(url, headers=header, params=param).json()

  return activity

def get_laps_info(activity_id):

  access_token = _get_access_token()

  url = f"https://www.strava.com/api/v3/activities/{activity_id}/laps"
  header = {'Authorization': 'Bearer ' + access_token}
  laps = requests.get(url, headers=header).json()

  return laps

def get_zones_info(activity_id):

  access_token = _get_access_token()

  url = f"https://www.strava.com/api/v3/activities/{activity_id}/zones"
  header = {'Authorization': 'Bearer ' + access_token}
  zones = requests.get(url, headers=header).json()

  return zones

