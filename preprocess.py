import argparse
import time

from utils import filter_country, get_sorted_date_list, gather_data
from utils import string_to_date, date_to_string


def main(args):

    print("=== Start preprocessing ===")

    table_mapping = {
        'coronavirus-cases-linear': 'Total cases',
        'coronavirus-deaths-linear': 'Total deaths',
        'graph-active-cases-total': 'Total active cases',
        'graph-cases-daily-1': 'Daily cases',
        'graph-deaths-daily-1': 'Daily deaths'
    }

    requirements = list(table_mapping.keys())

    print('1. Filtering countries...')
    filtered_countries = filter_country(args.data_dir, requirements)

    print('2. Get date range...')
    date_list = get_sorted_date_list(
        args.data_dir, filtered_countries, requirements)

    print('3. Gathering data...')
    gather_data(
        args.data_dir,
        filtered_countries,
        date_list,
        table_mapping,
        args.save_path
    )


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--data_dir', default='assets/data',
                        type=str, help='Path to data dir')
    parser.add_argument('--save_path', default='assets/all_data.csv',
                        type=str, help='Path to save data')

    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    main(args)
