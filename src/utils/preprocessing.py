import pandas as pd
import polyline
import json
from haversine import haversine, Unit


def get_map_data():
  
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
 
  # Create a mapping from a minute to pace
  minutes = [i for i in range(1, 225)]
  min_to_pace = dict()
  for m in minutes:
      for row in merged[['Time [min]', 'elapsed_time']].iterrows():
          t, pace_s = row[1]
          if m <= t:
              min_to_pace[m] = pace_s
              break
  
  # Create a mapping from minute in race to distance
  minutes_distance = None
  for m in minutes:
      pace = min_to_pace.get(m)
      if pace is not None:
          meters_per_sec = 1000/pace
          if minutes_distance is None:
              minutes_distance = [round(meters_per_sec*60, 2)]
          else:
              minutes_distance.append(minutes_distance[-1] + round(meters_per_sec*60, 2))
      else:
          break
  
  # Create a mapping from distance to location on map
  dm_to_loc = dict()
  for dm in minutes_distance:
      options = []
      for row in df[['Lat', 'Lon', 'distance [m]']].iterrows():
          lat, lot, dm2 = row[1]
          diff = abs(dm - dm2)
          if diff < 75:
              options.append((diff, lat, lot,))
      best = sorted(options, key=lambda x: x[0], reverse=False)[0]
      dm_to_loc[dm] = (best[1], best[2],)
  
  # Save the data
  df.to_csv('data/processed/df.csv', index=False)
  reduced_df.to_csv('data/processed/reduced_df.csv' , index=False)
  with open('data/processed/minutes_distance.csv', 'w') as f:
    f.write(",".join([str(m) for m in minutes_distance]))
  with open('data/processed/dm_to_loc.json', 'w') as f:
    json.dump(dm_to_loc, f) 

