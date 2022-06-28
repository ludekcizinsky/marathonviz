# External libraries
import pandas as pd
import polyline
from haversine import haversine, Unit
from tqdm import tqdm

# Built in libraries
import json
from timeit import default_timer as timer

# Custom
from .output import working_on, finished

def preprocess_marathon():
  
  # --- Coordinates data
  start = timer()
  working_on('Coordinates data.')

  # Load marathon json
  with open('data/raw/activities_detail/7146109879.json') as f:
    raw = json.load(f)
    coordinates = polyline.decode(raw['map']['polyline'])
  
  # Add distance between coordinates
  coordinates = pd.DataFrame(coordinates, columns =['Lat', 'Lon'])
  p0 = None
  distance = []
  for row in tqdm(coordinates[['Lat', 'Lon']].iterrows(), desc='# of coordinates processed'):
      if p0 is not None:
          p1 = row[1]
          distance.append(distance[-1] + haversine(p0, p1, unit=Unit.KILOMETERS))
          p0 = p1
      else:
          p0 = row[1]
          distance.append(0)
  coordinates['distance'] = distance
  coordinates['distance [m]'] = coordinates['distance']*1000
  
  finished('Processing of coordinates data.', timer() - start)
  
  # --- ith Km data
  start = timer()
  working_on('ith Km data.')

  # Approximate where each kilometer was
  exact_distance = [i for i in range(1, 44)]
  i = 0
  current = exact_distance[i]
  reduced_data = []
  for row in tqdm(coordinates[['Lat', 'Lon', 'distance']].iterrows(), desc='# of coordinates processed'):
      lat, lot, d = row[1]
      if abs(d - current) < 0.04:
          reduced_data.append((lat, lot, current, d,))
          i += 1
          current = exact_distance[i]

  reduced_df = pd.DataFrame(reduced_data, columns =['Lat', 'Lon', 'Exact Distance', 'Distance'])
  
  # Get more detailed info about each km
  splits = pd.DataFrame(raw['splits_metric'])
  splits['Exact Distance'] =  splits['split']
  merged = reduced_df.merge(splits, how='inner', on='Exact Distance')
  merged['Time [s]'] = merged['elapsed_time'].cumsum()
  merged['Time [min]'] = merged['Time [s]'].apply(lambda x: x/60)
  ithkm = merged
  
  # Save the data
  coordinates.to_csv('data/processed/coordinates.csv', index=False)
  ithkm.to_csv('data/processed/ithkm.csv', index=False)
  
  finished('Processing of ith km data.', timer() - start)

