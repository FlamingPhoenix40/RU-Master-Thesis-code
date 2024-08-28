import json
import csv
import os

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

def extract_urls_to_csv(json_file_path, csv_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        for index, url in enumerate(data['sites'].keys()):
            writer.writerow([index + 1, url])


json_file_path = os.path.join(ROOT_DIR, 'json_files', '5000_with_ublock.json')
csv_file_path = os.path.join(ROOT_DIR, 'tranco', 'Z3WXG', '1000_run_august.csv')

extract_urls_to_csv(json_file_path, csv_file_path)