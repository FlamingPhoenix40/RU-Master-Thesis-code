import json
import matplotlib.pyplot as plt
import os

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))

def load_json_data(file_path):
    """Loads JSON data from a file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_metric_values(data, metric):
    """Extracts values of a specified metric or sub-metric from the data."""
    values = []
    for site_data in data['sites'].values():
        if metric in site_data:
            values.append(site_data[metric])
        elif 'navigationTiming' in site_data and metric in site_data['navigationTiming']:
            values.append(site_data['navigationTiming'][metric])
        else:
            # Handle cases where the metric is not found
            print(f"Warning: Metric '{metric}' not found for some sites.")
    return values

def sbs_boxplot(values1, values2, metric, axis_max=None, output_file=None):
    """Creates a box plot of the given metric values."""
    values1 = [v for v in values1 if v is not None]
    values2 = [v for v in values2 if v is not None]
    # print(values1)

    plt.figure(figsize=(10, 6))
    plt.boxplot([values1, values2], labels=['Without uBO', 'With uBO'], vert=False)
    plt.title(f'Boxplot of {metric}')
    plt.ylabel(metric)
    
    if axis_max:
        plt.xlim(-2000, axis_max)  # Set the y-axis limit if provided
    
    if output_file == None:
        plt.show()
    else:
        plt.savefig(output_file)

def main():
    file_wo_ublock = os.path.join(ROOT_DIR, 'json_files', '1000_aug_without_ublock.json')
    file_w_ublock = os.path.join(ROOT_DIR, 'json_files', '1000_aug_with_ublock.json')

    data_with = load_json_data(file_w_ublock)
    data_without = load_json_data(file_wo_ublock)

    metric = input("Enter the metric or sub-metric to extract: ")

    axis_mode = input("Set axis limits manually? (y/n): ")
    axis_max = None

    if axis_mode.lower() == 'y':
        try:
            axis_max = float(input("Enter the maximum value for the x-axis: "))
        except ValueError:
            exit('invalid input for maximum value, please try again...')
            return

    values1 = extract_metric_values(data_without, metric)
    values2 = extract_metric_values(data_with, metric)
    output_file = os.path.join(ROOT_DIR, 'graphs', 'sbs', f'{metric}_sbs_boxplot.png')

    sbs_boxplot(values1, values2, metric, axis_max, output_file)
    # sbs_boxplot(values1, values2, metric, axis_max)

if __name__ == '__main__':
    main()