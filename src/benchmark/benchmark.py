import csv
import json
from collections import defaultdict

# Define file paths
csv_file_path = '../data/opp-115-dataset/consolidation/threshold-1.0-overlap-similarity/20_theatlantic.com.csv'
json_file_path = '../data/benchmark/key.json'

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
