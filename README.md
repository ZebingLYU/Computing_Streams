Overview

This solution comprises three main scripts designed to simulate, aggregate, and compute top song streaming data. Each script plays a specific role in the overall processing flow.

1.	generate_data.py: Simulates daily streaming data to help test the system. Simply executing this script, and it will produce seven daily log files.

2.	saving_intermediary_files.py: Aggregates and saves each day's streaming data in a reduced intermediary format, easing computation for the final step. 
One of the reason why I save past 7days' intermediary files is that now I'm at the beginning of the system building, so I need to process the past 7 days data. In my next script, you can see that, in the daily basis, we just need to save yesterday's intermediary files, since intermediary files of the day before yesterday should have been created before.

3.	Computation_system.py: Processes the previous day's music streaming logs to aggregate song data by country and user and save them as intermediary files. It then compiles the past seven days' intermediary data to identify the top 50 most-streamed songs. Finally, it outputs these rankings into files, organized both by country and by individual user.
In order to automate the computation system daily, we can set up the cron job with schedule and the path to Computation_system.py in the terminal.
