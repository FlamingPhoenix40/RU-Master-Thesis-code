import json
import matplotlib.pyplot as plt
import pandas as pd
import os

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

def load_json_data(file_path):
    """Loads JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_metric_values(data, metric_name):
    values = []
    for site, metrics in data['sites'].items():
        if metric_name in metrics:
            values.append(metrics[metric_name])
        elif metric_name in metrics.get('navigationTiming', {}):
            values.append(metrics['navigationTiming'][metric_name])
        else:
            print(f'Warning: Metric "{metric_name}" not found for site "{site}"')
    return values

def sbs_boxplot(values1, values2, metric_name):
    df = pd.DataFrame({
        'Without uBO': values1,
        'with uBO': values2
    })

    axis_mode = input('Set axis limits manually? (y/n): ')
    axis_max = None

    if axis_mode.lower() == 'y':
        try:
            axis_max = int(input('Enter maximum value for x-axis: '))
        except ValueError:
            exit('Invalid input for maximum value, please try again...')
            return
    
    
    df.plot.box(title=f'Side-by-side boxplot of {metric_name}')
    plt.ylabel(metric_name)

    if axis_max:
        plt.xlim(0, axis_max)

    plt.show()


def main():
    file_with = os.path.join(ROOT_DIR, 'json_files', '1000_aug_with_ublock.json')
    file_without = os.path.join(ROOT_DIR, 'json_files', '1000_aug_without_ublock.json')

    data_with = load_json_data(file_with)
    data_without = load_json_data(file_without)

    metric_name = input('Enter metric or sub-metric to extract: ')

    values1 = extract_metric_values(data_without, metric_name)
    values2 = extract_metric_values(data_with, metric_name)

    sbs_boxplot(values1, values2, metric_name)



if __name__ == '__main__':
    main()