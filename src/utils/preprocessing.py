import gpxpy
import glob
import pandas as pd
from tqdm import tqdm

def gpx_to_df(folderpath):

  """
  Code adapted from:
  https://github.com/nidhaloff/gpx-converter/blob/master/gpx_converter/base.py
  """
  
  # Get all runs
  all_runs_files = glob.glob(folderpath + '/*.gpx')

  # Save everything to pandas dataframe
  df = pd.DataFrame(columns=['RunId', 'Time', 'Lon', 'Lat', 'Altitude'])
    
  for file in tqdm(all_runs_files, desc='Gpx runs info to datframe'):

    # Save all needed attributes
    longs, lats, times, alts = [], [], [], []

    with open(file, 'r') as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        for run in gpx.tracks:
            for segment in run.segments:
                for point in segment.points:
                    lats.append(point.latitude)
                    longs.append(point.longitude)
                    times.append(point.time)
                    alts.append(point.elevation)

    # Save it as df
    runids = [file.split('/')[-1][:-4]]*len(longs)
    data = {'RunId': runids, 'Lon': longs, 'Lat': lats, 'Time': times, 'Altitude': alts}
    run_df = pd.DataFrame.from_dict(data)
    
    # Append to global df
    df = pd.concat([df, run_df], ignore_index=True)
 
  return df

