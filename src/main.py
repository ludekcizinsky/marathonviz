from utils import working_on, finished, gpx_to_df, plot_grid
from timeit import default_timer as timer
import argparse
import pandas as pd

# CLI
parser = argparse.ArgumentParser(
    description='Control run flow of main.py'
)

parser.add_argument(
    '-PRE',
    '--preprocess',
    action='store_true',
    help='Preprocess input data'
)

parser.add_argument(
    '-PLT',
    '--plot',
    action='store_true',
    help='Generate plots'
)

args = parser.parse_args()

def main():
  
  if args.preprocess:
    s = working_on('Preprocessing data')
    running_tracks = gpx_to_df('data/raw/activities')
    running_tracks.to_csv('data/processed/running_tracks.csv', index=False) 
    finished('Preprocessing of data done.', timer() - s)
  else:
    try:
      running_tracks = pd.read_csv('data/processed/running_tracks.csv')
    except FileNotFoundError as e:
      pass

  if args.plot:
    plot_grid(running_tracks, '../figures/grid.png')


if __name__ == '__main__':
  main()

