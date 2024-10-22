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

def plot_metric_boxplot(values, metric_name, axis_max, output_file=None):
    for sub_metric, values in values.items():
        df = pd.DataFrame({sub_metric: values})

        plt.figure(figsize=(10, 6))
        if axis_max is not None:
            ax = plt.gca()
            ax.set_xlim([0, axis_max])
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

def plot_all_metrics_boxplot(data, axis_max, output_file=None):
    """Plots a boxplot of all metrics and saves it as a PNG file."""
    
    

    # Metrics to exclude from the plot
    excluded_metrics = ['estimatedTBT', 'dnsLookupTimes']
    # Create a list of all metrics
    all_metrics = [metric for metric in list(data['sites'].values())[0].keys() if metric not in excluded_metrics]

    # Prepare data for plotting
    data_to_plot = []
    labels = []
    for metric in all_metrics:
        values = extract_metric_values(data, metric)
        if values:  # Skip empty metrics
            for sub_metric, sub_values in values.items():
                data_to_plot.append(sub_values)
                labels.append(f"{metric} - {sub_metric}")

    plt.figure(figsize=(15, 8))  # Adjust figure size as needed
    if axis_max is not None:
        ax = plt.gca()
        ax.set_xlim([0, axis_max])
    plt.boxplot(data_to_plot, vert=False, labels=labels)
    plt.title('Boxplot of All Metrics')
    plt.xlabel('Values')
    plt.yticks(fontsize=8)  # Adjust font size if labels overlap
    plt.tight_layout()  # Prevent labels from being cut off

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

    plt.close()


def plot_side_by_side_boxplot(metric_name, data1, data2, axis_max, output_file=None):
    values1 = extract_metric_values(data1, metric_name)
    values2 = extract_metric_values(data2, metric_name)

    if not values1 or not values2:
        print(f'Error: No data found for metric: {metric_name} in one or both files')
        return
    
    plt.figure(figsize=(10, 6))

    data_to_plot = []
    labels = []
    for sub_metric, sub_values in values1.items():
        data_to_plot.append(sub_values)
        labels.append(f"Without uBO - {sub_metric}")
    
    for sub_metric, sub_values in values2.items():
        data_to_plot.append(sub_values)
        labels.append(f"With uBO - {sub_metric}")

    if axis_max is not None:
        ax = plt.gca()
        ax.set_xlim([0, axis_max])
    
    plt.boxplot(data_to_plot, vert=False, labels=labels)
    plt.title(f'Side-by-side boxplot of {metric_name}')
    plt.xlabel('Values')
    plt.yticks(fontsize=8)
    plt.tight_layout()

    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
    
    plt.close()
    

def main_plot_function(json_filename, which_graphs, output_subfolder, axis_max):
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
                    plot_metric_boxplot(values, metric, axis_max, output_file)
                case "boxplot_all":
                    plot_all_metrics_boxplot(data, axis_max, output_file)
                case "all":
                    plot_metric_histogram(values, metric, output_file)
                    plot_metric_boxplot(values, metric, axis_max, output_file)
                    plot_all_metrics_boxplot(data, axis_max, output_file)
                case _:
                    exit('invalid input for graph type, exiting...')

            

def main():
    json_filename = input("Use JSON file with or without ublock? ('w', 'wo', 'both', sbs): ")
    which_graphs = input("Which graphs would you like to generate? (histogram, boxplot, boxplot_all, all): ")
    axis_mode = input("Set axis limits manually? (y/n): ")

    axis_max = None

    if axis_mode.lower() == 'y':
        try:
            axis_max = float(input("Enter the maximum value for the x-axis: "))
        except ValueError:
            exit('invalid input for maximum value, please try again...')
            return

    match json_filename:
        case "wo":
            json_filename = '1000_aug_without_ublock.json'
            output_subfolder = 'no_ublock'
            main_plot_function(json_filename, which_graphs, output_subfolder, axis_max)
        case "w":
            json_filename = '1000_aug_with_ublock.json'
            output_subfolder = 'with_ublock'
            main_plot_function(json_filename, which_graphs, output_subfolder, axis_max)
        case "both":
            output_subfolder_wo = 'no_ublock'
            json_filename = '1000_aug_without_ublock.json'
            main_plot_function(json_filename, which_graphs, output_subfolder_wo, axis_max)
            output_subfolder_w = 'with_ublock'
            json_filename = '1000_aug_with_ublock.json'
            main_plot_function(json_filename, which_graphs, output_subfolder_w, axis_max)
        case "sbs": # sbs = sided by side
            output_subfolder_wo = 'no_ublock'
            data_wo = load_json_data(os.path.join(ROOT_DIR, 'json_files', '1000_aug_without_ublock.json'))
            data_w = load_json_data(os.path.join(ROOT_DIR, 'json_files', '1000_aug_with_ublock.json'))
            metric_to_plot = input("Enter the metric you would like to plot: ")
            output_file = os.path.join(ROOT_DIR, 'graphs', 'sbs', f'{metric_to_plot}_sbs.png')
            plot_side_by_side_boxplot(metric_to_plot, data_wo, data_w, axis_max, output_file)
        case _:
            exit('invalid input for json file type, exiting...')

    

if __name__ == '__main__':
    main()
