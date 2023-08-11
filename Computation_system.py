import os
import json
import logging
import argparse
from datetime import datetime, timedelta
from collections import defaultdict, Counter

DAILY_LOGS_FOLDER = '/Users/joseph/Desktop/daily_logs_folder'
INTERMEDIARY_FOLDER = '/Users/joseph/Desktop/intermediary_files'
OUTPUT_FOLDER = '/Users/joseph/Desktop/Deezer_output'

logging.basicConfig(level=logging.INFO, filename=os.path.join(OUTPUT_FOLDER, 'corrupted_rows.log'), filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

VALID_ISO_CODES = set(['BL', 'GN', 'BN', 'ST', 'PW', 'HK', 'NL', 'BN', 'HM', 'NR', 'GT', 'GU', 'PA', 'CW', 'GA', 'KG', 'MH', 'GI', 'WS', 'BQ', 'AE', 'IS', 'GI', 'YE', 'NI', 'JO', 'LY', 'OM', 'ZM', 'BF', 'ID', 'BQ', 'RS', 'GL', 'IE', 'LK', 'DZ', 'UM', 'GB', 'SA', 'MO', 'HN', 'ZA', 'HU', 'DM', 'MO', 'GU', 'LV', 'GD', 'WF', 'PY', 'MM', 'VE', 'PH', 'KZ', 'NE', 'IQ', 'HN', 'NU', 'KH', 'HN', 'KN', 'MN', 'BL', 'AU', 'MM', 'CL', 'MV', 'CN', 'BW', 'SY', 'LR', 'MT', 'ZA', 'BS', 'PR', 'GQ', 'TV', 'HK', 'AF', 'GF', 'BN', 'SH', 'MS', 'YT', 'FI', 'BG', 'BI', 'AW', 'TO', 'PM', 'IQ', 'HR', 'JE', 'GA', 'NG', 'CL', 'CW', 'BI', 'TT'])

# Read the daily log, aggregate song data by country and user
def read_daily_log(file_path):
    daily_country_data = defaultdict(lambda: defaultdict(int))
    daily_user_data = defaultdict(lambda: defaultdict(int))

    with open(file_path, 'r') as file:
        for line in file:
            corrupted, reason = is_row_corrupted(line)
            if corrupted:
                logging.warning(f"Corrupted row found ({reason}): {line.strip()}")
                continue

            sng_id, user_id, country = line.strip().split(' | ')
            daily_country_data[country][sng_id] += 1
            daily_user_data[user_id][sng_id] += 1

    return daily_country_data, daily_user_data

def is_row_corrupted(row):
    elements = row.strip().split(' | ')  # Splitting based on the given delimiter
    if len(elements) != 3:
        return True, "Number of elements is not 3"
    
    sng_id, user_id, country = elements

    # Check if sng_id and user_id are integers
    if not sng_id.isdigit() or not user_id.isdigit():
        return True, "sng_id or user_id is not an integer"

    # Check if country code is in VALID_ISO_CODES
    if country not in VALID_ISO_CODES:
        return True, "Invalid country code"

    return False, ""

# Save aggregated data as intermediary JSON files
def save_intermediary_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

# Process the daily log for a given date and save the results as intermediary files
def process_daily_log_and_save_intermediary_files(date_str):
    file_name = f"listen-{date_str}.log"
    file_path = os.path.join(DAILY_LOGS_FOLDER, file_name)

    # If the file for the given date doesn't exist, skip the process
    if not os.path.exists(file_path):
        print(f"File {file_name} not found!")
        return
    
    daily_country_data, daily_user_data = read_daily_log(file_path)

    country_data_file = os.path.join(INTERMEDIARY_FOLDER, f"country_data_{date_str}.json")
    user_data_file = os.path.join(INTERMEDIARY_FOLDER, f"user_data_{date_str}.json")

    save_intermediary_data(daily_country_data, country_data_file)
    save_intermediary_data(daily_user_data, user_data_file)


# Compute top 50 songs based on the aggregated data from the past 7 days
def compute_top_songs_for_past_seven_days(output_date=None):
    if output_date is None:
        current_date = datetime.now()
    else:
        current_date = datetime.strptime(output_date, '%Y-%m-%d') # Convert to datetime here
        
    past_seven_dates = [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 8)]
    
    print("Processing the following dates:", past_seven_dates)

    aggregated_country_data = defaultdict(Counter)
    aggregated_user_data = defaultdict(Counter)

    # Aggregating song data from past seven days
    for date_str in past_seven_dates:
        country_data_file = os.path.join(INTERMEDIARY_FOLDER, f"country_data_{date_str}.json")
        user_data_file = os.path.join(INTERMEDIARY_FOLDER, f"user_data_{date_str}.json")
        
        with open(country_data_file, 'r') as file:
            daily_country_data = json.load(file)
            for country, data in daily_country_data.items():
                aggregated_country_data[country].update(data)

        with open(user_data_file, 'r') as file:
            daily_user_data = json.load(file)
            for user, data in daily_user_data.items():
                aggregated_user_data[user].update(data)

    # Writing top 50 songs data to output files
    output_date = current_date.strftime('%Y%m%d')
    with open(os.path.join(OUTPUT_FOLDER, f"country_top50_{output_date}.txt"), 'w') as file:
        for country, data in aggregated_country_data.items():
            top_songs = ",".join([f"{sng_id}:{count}" for sng_id, count in data.most_common(50)])
            file.write(f"{country}|{top_songs}\n")

    with open(os.path.join(OUTPUT_FOLDER, f"user_top50_{output_date}.txt"), 'w') as file:
        for user, data in aggregated_user_data.items():
            top_songs = ",".join([f"{sng_id}:{count}" for sng_id, count in data.most_common(50)])
            file.write(f"{user}|{top_songs}\n")

def main():
    parser = argparse.ArgumentParser(description="Compute Top 50 Songs")
    parser.add_argument('--date', type=str, help="Specify a date in 'YYYY-MM-DD' format to calculate the 7-day period ending on the day before the specified date. Defaults to processing the 7-day period ending yesterday.")
    args = parser.parse_args()
    
    if args.date is None:
        output_date = datetime.now().strftime('%Y-%m-%d')
    else:
        output_date = datetime.strptime(args.date, '%Y-%m-%d').strftime('%Y-%m-%d') # Convert to string here


    process_daily_log_and_save_intermediary_files(output_date)
    compute_top_songs_for_past_seven_days(output_date)

if __name__ == "__main__":
    main()




