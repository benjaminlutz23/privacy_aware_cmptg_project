import csv
import json
import os
from collections import defaultdict

# This script converts the CSV files containing policy data to more readable JSON files.

# Define directories
csv_dir_path = '../data/opp-115-dataset/consolidation/threshold-1.0-overlap-similarity'
json_dir_path = '../data/benchmark/annotated_policies'

# Ensure the JSON directory exists
os.makedirs(json_dir_path, exist_ok=True)

# Loop through all CSV files in the directory
for csv_filename in os.listdir(csv_dir_path):
    if csv_filename.endswith('.csv'):
        csv_file_path = os.path.join(csv_dir_path, csv_filename)
        json_file_path = os.path.join(json_dir_path, csv_filename.replace('.csv', '.json'))

        # Initialize a dictionary to hold the JSON structure
        data = defaultdict(list)

        # Read the CSV file
        with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                # Extract relevant fields
                section_number = row[4]
                entry = {
                    "id": row[0],
                    "label": row[1],
                    "start_index": row[2],
                    "end_index": row[3],
                    "category": row[5],
                    "details": json.loads(row[6]),
                    "date": row[7],
                    "url": row[8]
                }
                # Append the entry to the corresponding section number
                data[section_number].append(entry)

        # Write the JSON data to the file
        with open(json_file_path, mode='w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4)
