import pandas as pd
import polyline
import json
from haversine import haversine, Unit


def preprocess_marathon():
  
  # Load marathon json
  with open('data/raw/activities_detail/7146109879.json') as f:
    dd = json.load(f)
    data = polyline.decode(dd['map']['polyline'])
  
  # Add distance between coordinates
  df = pd.DataFrame(data, columns =['Lat', 'Lon'])
  p0 = None
  distance = []
  for row in df[['Lat', 'Lon']].iterrows():
      if p0 is not None:
          p1 = row[1]
          distance.append(distance[-1] + haversine(p0, p1, unit=Unit.KILOMETERS))
          p0 = p1
      else:
          p0 = row[1]
          distance.append(0)
  df['distance'] = distance
  df['distance [m]'] = df['distance']*1000
  
  # Approximate where each kilemeter was
  exact_distance = [i for i in range(1, 44)]
  i = 0
  current = exact_distance[i]
  reduced_data = []
  for row in df[['Lat', 'Lon', 'distance']].iterrows():
      lat, lot, d = row[1]
      if abs(d - current) < 0.04:
          reduced_data.append((lat, lot, current, d,))
          i += 1
          current = exact_distance[i]

  reduced_df = pd.DataFrame(reduced_data, columns =['Lat', 'Lon', 'Exact Distance', 'Distance'])
  
  # Get more detailed info about each km
  splits = pd.DataFrame(dd['splits_metric'])
  splits['Exact Distance'] =  splits['split']
  merged = reduced_df.merge(splits, how='inner', on='Exact Distance')
  merged['Time [s]'] = merged['elapsed_time'].cumsum()
  merged['Time [min]'] = merged['Time [s]'].apply(lambda x: x/60)
  
  # Save the data
  df.to_csv('data/processed/df.csv', index=False)
  reduced_df.to_csv('data/processed/reduced_df.csv' , index=False)
  merged.to_csv('data/processed/merged.csv', index=False)

