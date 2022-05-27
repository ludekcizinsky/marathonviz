from utils import (
    working_on,
    finished,
    gpx_to_df,
    plot_grid,
    list_activities,
    get_laps_info,
    get_activity_info,
    get_zones_info
)
from timeit import default_timer as timer
import argparse
import pandas as pd
from datetime import datetime
from pprint import pprint
import json
from tqdm import tqdm

# CLI
parser = argparse.ArgumentParser(
    description='Control run flow of main.py'
)

parser.add_argument(
    '-PRE',
    '--preprocess',
    action='store_true',
    help='Preprocess input data.'
)

parser.add_argument(
    '-PLT',
    '--plot',
    action='store_true',
    help='Generate plots.'
)

parser.add_argument(
    '-FT',
    '--fetch',
    action='store_true',
    help='Fetch data from strava api.'
)


args = parser.parse_args()

def main(): 

  if args.fetch:
    s = working_on('Fetching data via Strava API')
    # All marathon activities
    after = datetime.strptime('2022-02-27', '%Y-%m-%d').timestamp()
    before = datetime.strptime('2022-05-16', '%Y-%m-%d').timestamp()
    activities = list_activities(after, before)
    with open("data/raw/activities_list/marathon_runs_list.json", "w") as f:
      json.dump(activities, f)

    # All activities details
    for activity in tqdm(activities, desc='Fetching data'):
      activity_id = activity['id']

      activity_detail = get_activity_info(activity_id)
      with open(f"data/raw/activities_detail/{activity_id}.json", "w") as f:
        json.dump(activity_detail, f)

      zone_info = get_zones_info(activity_id)
      with open(f"data/raw/activities_zones/{activity_id}.json", "w") as f:
        json.dump(zone_info, f)

    finished('Fetching done.', timer() - s)

  if args.preprocess:
    s = working_on('Preprocessing data')
    running_tracks = gpx_to_df('data/raw/activities')
    running_tracks.to_csv('data/processed/running_tracks.csv', index=False) 
    finished('Preprocessing of data done.', timer() - s)
  else:
    try:
      running_tracks = pd.read_csv('data/processed/running_tracks.csv')
    except FileNotFoundError as e:
      print(e)
      return

  if args.plot:
    plot_grid(running_tracks, '../figures/grid.png')

if __name__ == '__main__':
  main()

