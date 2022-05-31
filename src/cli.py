import argparse
from utils import fetch_marathon_data, preprocess_marathon


parser = argparse.ArgumentParser(
    description='CLI for data preprocessing tasks'
)

parser.add_argument(
    '-PRE',
    '--preprocess',
    action='store_true',
    help='Preprocess input data.'
)

parser.add_argument(
    '-FT',
    '--fetch',
    action='store_true',
    help='Fetch data from strava api.'
)


args = parser.parse_args()

def main():

  if args.preprocess:
    preprocess_marathon()

if __name__ == '__main__':
  main()

