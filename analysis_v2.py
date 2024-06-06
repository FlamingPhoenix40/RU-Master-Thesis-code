import json
import matplotlib.pyplot as plt
import pandas as pd
import os

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
json_filename = '1_mil_no_ublock.json'

def load_json_data(file_path):
    """Loads JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_metric_values(data, metric_name):
    """Extracts values for a given metric from the JSON data."""
    metric_values = {}
    for site_data in data['sites'].values():
        value = site_data.get(metric_name)  
        if isinstance(value, dict):
            for sub_metric, sub_value in value.items():
                if sub_value is not None:
                    metric_values.setdefault(sub_metric, []).append(sub_value) 
        elif value is not None:  
            metric_values.setdefault(metric_name, []).append(value)
    return metric_values  

def plot_metric_histogram(values, metric_name, output_file=None):
    """Plots a histogram of metric values and saves it as a PNG file."""
    for sub_metric, values in values.items():
        df = pd.DataFrame({sub_metric: values})

        plt.figure(figsize=(10, 6))
        counts, bins, bars = plt.hist(df[sub_metric], bins=20, color='skyblue', edgecolor='black')

        # Add text labels above each bar
        for bar in bars:
            height = bar.get_height()
            if height > 0:  # Only label bars with a count
                plt.text(bar.get_x() + bar.get_width() / 2, height,
                         str(int(height)), ha='center', va='bottom')

        plt.title(f'Distribution of {metric_name} - {sub_metric}')
        plt.xlabel(sub_metric)
        plt.ylabel('Frequency')
        plt.grid(axis='y', alpha=0.5)

        if output_file:
            file_name, file_ext = os.path.splitext(output_file)
            plt.savefig(f"{file_name}_{sub_metric}{file_ext}")
        else:
            plt.show()

def main():
    """The main function to execute the script's logic."""
    json_file_path = os.path.join(ROOT_DIR, 'json_files', json_filename)  # Use ROOT_DIR
    data = load_json_data(json_file_path)

    metrics = list(data['sites'].values())[0].keys()

    for metric in metrics:
        values = extract_metric_values(data, metric)
        if values:
            output_file = os.path.join(ROOT_DIR, 'graphs_testing', f'histogram.png')
            plot_metric_histogram(values, metric, output_file)

if __name__ == '__main__':
    main()
