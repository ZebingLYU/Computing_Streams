#!/usr/bin/env python
# coding: utf-8

# In[11]:


import random
from datetime import datetime, timedelta

def generate_random_data(file_prefix, num_rows_per_day, num_days):
    countries = ['BL', 'GN', 'BN', 'ST', 'PW', 'HK', 'NL', 'BN', 'HM', 'NR', 'GT', 'GU', 'PA', 'CW', 'GA', 'KG', 'MH', 'GI', 'WS', 'BQ', 'AE', 'IS', 'GI', 'YE', 'NI', 'JO', 'LY', 'OM', 'ZM', 'BF', 'ID', 'BQ', 'RS', 'GL', 'IE', 'LK', 'DZ', 'UM', 'GB', 'SA', 'MO', 'HN', 'ZA', 'HU', 'DM', 'MO', 'GU', 'LV', 'GD', 'WF', 'PY', 'MM', 'VE', 'PH', 'KZ', 'NE', 'IQ', 'HN', 'NU', 'KH', 'HN', 'KN', 'MN', 'BL', 'AU', 'MM', 'CL', 'MV', 'CN', 'BW', 'SY', 'LR', 'MT', 'ZA', 'BS', 'PR', 'GQ', 'TV', 'HK', 'AF', 'GF', 'BN', 'SH', 'MS', 'YT', 'FI', 'BG', 'BI', 'AW', 'TO', 'PM', 'IQ', 'HR', 'JE', 'GA', 'NG', 'CL', 'CW', 'BI', 'TT']

    today = datetime.today()
    start_date = today - timedelta(days=num_days)
    
    for day in range(num_days):
        date_str = (start_date + timedelta(days=day)).strftime('%Y-%m-%d')
        file_path = f"{file_prefix}-{date_str}.log"

        with open(file_path, 'w') as file:
            # Add more data from previous days to the current day's data
            for prev_day in range(day):
                with open(f"{file_prefix}-{(start_date + timedelta(days=prev_day)).strftime('%Y-%m-%d')}.log", 'r') as prev_file:
                    lines = prev_file.readlines()
                    num_lines_to_copy = min(len(lines), num_rows_per_day // (day - prev_day))
                    selected_lines = random.sample(lines, num_lines_to_copy)
                    file.writelines(selected_lines)

            # Generate new random data for the current day
            for _ in range(num_rows_per_day - file.tell()):
                sng_id = random.randint(15000000, 25000000)
                user_id = random.randint(3500000, 8500000)
                country = random.choice(countries)
                file.write(f"{sng_id} | {user_id} | {country}\n")

generate_random_data("/Users/joseph/Desktop/daily_logs_folder/listen", 15000000, 7)







