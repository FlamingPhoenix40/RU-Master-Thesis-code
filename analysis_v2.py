import json
import matplotlib.pyplot as plt
import pandas as pd
import os


ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
#json_filename = '1_mil_no_ublock.json'


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
    
        plt.close()

def plot_metric_boxplot(values, metric_name, output_file=None):
    for sub_metric, values in values.items():
        df = pd.DataFrame({sub_metric: values})

        plt.figure(figsize=(10, 6))
        plt.boxplot(df[sub_metric], vert = False)
        plt.title(f'Boxplot of {metric_name} - {sub_metric}')
        plt.xlabel('Values')
        plt.yticks([])

        if output_file:
            file_name, file_ext = os.path.splitext(output_file)
            plt.savefig(f"{file_name}_{sub_metric}{file_ext}")
        else:
            plt.show()

        plt.close()

def plot_all_metrics_boxplot(data, output_file=None):
    """Plots a boxplot of all metrics and saves it as a PNG file."""
    all_data = []
    labels = []
    
    # Extract data for all metrics
    for metric_name in data['sites'].values()[0].keys():  # Get metrics from the first site
        values = extract_metric_values(data, metric_name)
        if values:
            if isinstance(values, dict):  # Handle sub-metrics
                for sub_metric, sub_values in values.items():
                    all_data.append(sub_values)
                    labels.append(f"{metric_name} - {sub_metric}")
            else:
                all_data.append(values)
                labels.append(metric_name)
    
    plt.figure(figsize=(12, 8))  # Adjust figure size as needed
    plt.boxplot(all_data, vert=False, labels=labels)
    plt.title('Boxplot of All Metrics')
    plt.xlabel('Values')
    plt.yticks([])  # Hide y-axis ticks and labels

    plt.savefig(output_file)


def main_plot_function(json_filename, which_graphs, output_subfolder):
    json_file_path = os.path.join(ROOT_DIR, 'json_files', json_filename)  # Use ROOT_DIR
    data = load_json_data(json_file_path)

    metrics = list(data['sites'].values())[0].keys()
    
    

    for metric in metrics:
        values = extract_metric_values(data, metric)
        if values:
            
            if not os.path.exists(os.path.join(ROOT_DIR, 'graphs', output_subfolder)):
                os.makedirs(os.path.join(ROOT_DIR, 'graphs', output_subfolder), exist_ok=True)

            output_file = os.path.join(ROOT_DIR, 'graphs', output_subfolder, f'{which_graphs}_{output_subfolder}.png')
            
            
            match which_graphs:
                case "histogram":
                    plot_metric_histogram(values, metric, output_file)
                case "boxplot":
                    plot_metric_boxplot(values, metric, output_file)
                case "boxplot_all":
                    plot_all_metrics_boxplot(data, output_file)
                case "all":
                    plot_metric_histogram(values, metric, output_file)
                    plot_metric_boxplot(values, metric, output_file)
                    plot_all_metrics_boxplot(data, output_file)
                case _:
                    exit('invalid input for graph type, exiting...')

            

def main():
    json_filename = input("Use JSON file with or without ublock? ('w' or 'wo' or 'both'): ")
    which_graphs = input("Which graphs would you like to generate? (histogram, boxplot, all): ")
    
    match json_filename:
        case "wo":
            json_filename = '1000_aug_without_ublock.json'
            output_subfolder = 'no_ublock'
            main_plot_function(json_filename, which_graphs, output_subfolder)
        case "w":
            json_filename = '1000_aug_with_ublock.json'
            output_subfolder = 'with_ublock'
            main_plot_function(json_filename, which_graphs, output_subfolder)
        case "both":
            output_subfolder_wo = 'no_ublock'
            json_filename = '1000_aug_without_ublock.json'
            main_plot_function(json_filename, which_graphs, output_subfolder_wo)
            output_subfolder_w = 'with_ublock'
            json_filename = '1000_aug_with_ublock.json'
            main_plot_function(json_filename, which_graphs, output_subfolder_w)
        case _:
            exit('invalid input for json file type, exiting...')

    

if __name__ == '__main__':
    main()
