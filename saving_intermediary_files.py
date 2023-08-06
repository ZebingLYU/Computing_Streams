#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
from collections import defaultdict
from datetime import date, timedelta

DAILY_LOGS_FOLDER = '/Users/joseph/Desktop/daily_logs_folder'
INTERMEDIARY_FOLDER = '/Users/joseph/Desktop/intermediary_files'

# Read the daily log and extract stream data grouped by country and user
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

# Save the provided data in JSON format which can reduce the size of daily log.
def save_intermediary_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)
        
# Process the daily log for the given date and save the intermediary data files.
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
    
if __name__ == "__main__":
    # Compute dynamic date range for the past 7 days
    today = date.today()
    date_range = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, 8)][::-1]

    # Process each day in the date range
    for date_str in date_range:
        process_daily_log_and_save_intermediary_files(date_str)


# In[ ]:




