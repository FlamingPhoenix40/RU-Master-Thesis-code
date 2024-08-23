import json
import os

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

def filter_sites(no_ublock_json, with_ublock_json, output_file):

    no_ublock_path = os.path.join(ROOT_DIR, 'json_files', no_ublock_json)
    with_ublock_path = os.path.join(ROOT_DIR, 'json_files', with_ublock_json)
    output_path = os.path.join(ROOT_DIR, 'json_files', output_file)

    with open(no_ublock_path, 'r') as f1, open(with_ublock_path, 'r') as f2:
        no_ublock_data = json.load(f1)
        smaller_sites = json.load(f2).get('sites', {}).keys()

    filtered_sites = {site: metrics for site, metrics in no_ublock_data['sites'].items()
                      if site in smaller_sites}

    no_ublock_data['sites'] = filtered_sites

    with open(output_path, 'w') as outfile:
        json.dump(no_ublock_data, outfile, indent=2)  # Add indentation for readability



no_ublock_json = '5000_no_ublock.json'
with_ublock_json = '5000_with_ublock.json'
output_file = 'filtered_data_no_ublock.json'

filter_sites(no_ublock_json, with_ublock_json, output_file)
