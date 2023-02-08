import os
import time
import argparse
from datetime import timedelta
from pathlib import Path

import pandas as pd
from utils import get_soup, extract_scripts, filter_scipts
from utils import get_date_data, get_count_data, get_table_name


BASE_URL = 'https://www.worldometers.info/coronavirus/country'
EXAMPLES_PATH = 'assets/examples'


def crawl_from(base_url, country, save_dir):
    global EXAMPLES_PATH

    url = '{}/{}'.format(base_url, country)

    # Request HTML
    soup = get_soup(url)

    # Get all script data
    scripts = extract_scripts(soup)
    filtered_scripts = filter_scipts(scripts)

    if len(filtered_scripts) > len(os.listdir(EXAMPLES_PATH)):

        for file in os.listdir(EXAMPLES_PATH):
            os.remove(os.path.join(EXAMPLES_PATH, file))

        for i, script in enumerate(filtered_scripts):
            with open(os.path.join(EXAMPLES_PATH, '{}_{}.txt'.format(country, i)), 'w') as f:
                f.write(script.text)

    # Get table name
    for script in filtered_scripts:

        # Extract data
        names = get_table_name(script)
        dates = get_date_data(script)
        counts = get_count_data(script)

        if len(counts) > len(dates):
            if len(dates) == 1:
                last_name = names.pop()
                last_date = dates.pop()

                for i in range(len(counts) - len(dates)):
                    names.append('{}-{}'.format(last_name, i+1))
                    dates.append(last_date)
            else:
                print('=========== SOS ===========')

        for i, name in enumerate(names):
            data = {
                'date': dates[i],
                'count': counts[i]
            }

            dataframe = pd.DataFrame(data)

            df_dir = os.path.join(save_dir, country)
            Path(df_dir).mkdir(parents=True, exist_ok=True)
            # Save data
            save_path = os.path.join(df_dir, '{}.csv').format(name)
            dataframe.to_csv(save_path, index=False)
            print('\tSaved data to {}!'.format(save_path))


def main(args):
    global BASE_URL

    since = time.time()

    print('=== Crawling from {} ==='.format(BASE_URL))

    # Extract contry list
    print('1. Get country list')
    with open(args.country_path, 'r') as f:
        countries = [line.strip() for line in f.readlines()]
    n_countries = len(countries)

    print('2. Start crawling...')
    for i, country in enumerate(countries):
        start = time.time()

        print('[{:>3}/{:>3}] Crawling country {}...'.format(i +
              1, n_countries, country))
        crawl_from(BASE_URL, country, args.save_dir)

        print('\tDone after {}s!'.format(
            timedelta(seconds=int(time.time() - start))))

    print('All done after {}s!'.format(
        timedelta(seconds=int(time.time() - since))))


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--save_dir', default='assets/data',
                        type=str, help='Path to save dir')
    parser.add_argument('--country_path', default='assets/countries.txt',
                        type=str, help='Path to country file')

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    main(args)
