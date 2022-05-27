import math
import matplotlib.pyplot as plt
import seaborn as sns

def plot_grid(df, output_file = 'plot.png'):

  """
  This code was adapted from:
  https://github.com/marcusvolz/strava_py/blob/main/src/stravavis/plot_facets.py
  """
  
  
  fig, ax = plt.subplots() 


  # Compute activity start times (for facet ordering)
  start_times = df.groupby('RunId').agg({'Time': 'min'}).reset_index().sort_values('Time')
  ncol = math.ceil(math.sqrt(len(start_times)))
  
  # Create facets
  p = sns.FacetGrid(
      data = df,
      col = 'RunId',
      col_wrap = ncol,
      col_order = start_times['RunId'],
      sharex = False,
      sharey = False,
      )

  # Add activities
  p = p.map(
      plt.plot, "Lon", "Lat", color = 'black', linewidth = 4
  )

  # Update plot aesthetics
  p.set(xlabel = None)
  p.set(ylabel = None)
  p.set(xticks = [])
  p.set(yticks = [])
  p.set(xticklabels = [])
  p.set(yticklabels = [])
  p.set_titles(col_template = '', row_template = '')
  sns.despine(left = True, bottom = True)
  plt.subplots_adjust(left = 0.05, bottom = 0.05, right = 0.95, top = 0.95)
  plt.savefig(output_file)
