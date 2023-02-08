import os
import time
import pandas as pd
from datetime import timedelta

from .date import string_to_date, date_to_string


def filter_country(data_dir, requirements):

    countries = os.listdir(data_dir)

    filtered_countries = []
    for country in countries:
        tables = [t[:-4] for t in os.listdir(os.path.join(data_dir, country))]

        if all([r in tables for r in requirements]):
            filtered_countries.append(country)

    return filtered_countries


def get_sorted_date_list(data_dir, countries, tables):
    date_list = []

    for country in countries:
        for t in tables:
            path = os.path.join(data_dir, country, '{}.csv'.format(t))
            df = pd.read_csv(path)

            date_list.extend(df['date'].to_list())

    date_list = sorted([string_to_date(d) for d in set(date_list)])

    return date_list


def gather_data(data_dir, countries, date_list, table_mapping, dest_path):

    # init
    tables = list(table_mapping.keys())
    all_data = []

    print("Start preprocess data...")
    for i, date in enumerate(date_list):

        date = date_to_string(date)

        print('\t[{:>4}/{:>4}] Process date {}'.format(i +
              1, len(date_list), date))

        start = time.time()
        for country in countries:
            data = {}
            data['Date'] = date
            data['Country'] = country.replace('-', ' ').title()

            for table in tables:

                # Read csv file
                path = os.path.join(data_dir, country, '{}.csv'.format(table))
                df = pd.read_csv(path)

                # Check if date in df
                dates = df['date'].to_list()
                counts = df['count'].to_list()
                if date in dates:
                    index = dates.index(date)
                    data[table_mapping[table]] = counts[index]

                else:
                    data[table_mapping[table]] = 0

            # Add data to all data
            all_data.append(data)

        print('\t-> Done after {}s!'.format(
            timedelta(seconds=int(time.time() - start))))

    # Save to csv
    pd.DataFrame(all_data).to_csv(dest_path, index=False)
    print('Saved to {}!'.format(dest_path))
