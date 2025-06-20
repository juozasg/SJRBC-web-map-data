# read all files from datasets/*.csv except usgs.csv and tolthawk.csv
# each file format: siteId,date,variable1,variable2,variable3,...
# excat all dates from all files
# convert dates from MM/DD/YYYY format to YYYY-MM-DD format
# sort and print all unique dates
import os
import csv
from datetime import datetime
from glob import glob
from collections import defaultdict

def get_unique_dates():
    # Get all csv files in datasets directory
    csv_files = glob(os.path.join('datasets', '*.csv'))

    # Filter out usgs.csv and tolthawk.csv
    csv_files = [f for f in csv_files if not (f.endswith('usgs.csv') or f.endswith('tolthawk.csv'))]

    # Set to store unique dates
    unique_dates = set()

    # Process each CSV file
    for csv_file in csv_files:
        print(f"Processing {csv_file}...")

        with open(csv_file, 'r', newline='') as f:
            reader = csv.reader(f)

            # Get the header to determine the column index for date
            header = next(reader, None)
            if not header:
                continue

            # Date is typically in the second column (index 1)
            date_index = 1

            for row in reader:
                if len(row) > date_index:
                    date_str = row[date_index].strip()

                    # Skip empty dates
                    if not date_str:
                        continue

                    try:

                        # Try to convert from MM/DD/YYYY format to datetime
                        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                        # Convert to YYYY-MM-DD format
                        formatted_date = date_obj.strftime('%Y-%m-%d')
                        unique_dates.add(formatted_date)
                    except ValueError:
                        # If the date is already in YYYY-MM-DD format
                        try:
                            datetime.strptime(date_str, '%Y-%m-%d')
                            unique_dates.add(date_str)
                        except ValueError:
                            print(f"Skipping invalid date format: {date_str}")


    # for each year from 1989 add 04-01 and 10-01 to the unique dates
    for year in range(1989, datetime.now().year + 1):
        unique_dates.add(f"{year}-04-01")
        unique_dates.add(f"{year}-10-01")

    # Sort the unique dates
    sorted_dates = sorted(unique_dates)

    return sorted_dates



# # Print the sorted unique dates
# print("\nUnique dates in YYYY-MM-DD format:")
# for date in sorted_dates:
#     print(date)

# print(f"\nTotal unique dates: {len(sorted_dates)}")