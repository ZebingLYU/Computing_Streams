#!/usr/bin/env python
# coding: utf-8


import os
import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter

DAILY_LOGS_FOLDER = '/Users/joseph/Desktop/daily_logs_folder'
INTERMEDIARY_FOLDER = '/Users/joseph/Desktop/intermediary_files'
OUTPUT_FOLDER = '/Users/joseph/Desktop/Deezer_output'

# Read the daily log, aggregate song data by country and user
def read_daily_log(file_path):
    daily_country_data = defaultdict(lambda: defaultdict(int))
    daily_user_data = defaultdict(lambda: defaultdict(int))
    
    with open(file_path, 'r') as file:
        for line in file:
            try:
                sng_id, user_id, country = line.strip().split('|')
                daily_country_data[country][sng_id] += 1
                daily_user_data[user_id][sng_id] += 1
            except ValueError:
                print(f"Corrupted row found: {line.strip()}")
                continue
                
    return daily_country_data, daily_user_data

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
def compute_top_songs_for_past_seven_days():
    current_date = datetime.now()
    past_seven_dates = [(current_date - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 8)]

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

if __name__ == "__main__":
    # Process yesterday's log file and create intermediary files
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    process_daily_log_and_save_intermediary_files(yesterday)

    # Compute top 50 songs for past 7 days and write to output
    compute_top_songs_for_past_seven_days()





