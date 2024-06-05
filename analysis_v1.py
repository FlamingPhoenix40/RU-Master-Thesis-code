import json
import altair as alt
alt.data_transformers.disable_max_rows()
import pandas as pd
import os
import vl_convert as vlc

ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
json_name = '1_mil_no_ublock.json'

def main():
    json_path = os.path.join(ROOT_DIR, 'json_files', json_name)

    json_data = load_json_file(json_path)

    metric_data = extract_metric_data(json_data)

    output_dir = os.path.join(ROOT_DIR, "graphs_testing")
    os.makedirs(output_dir, exist_ok=True)

    generate_histograms(metric_data, output_dir)


# def generate_histograms(metric_data, output_dir):
#     for metric, values in metric_data.items():
#         df = pd.DataFrame({f"{metric} (ms)": values})
#         chart = alt.Chart(df).mark_bar().encode(
#             x=alt.X(f"{metric} (ms):Q", bin=True, title=f"{metric} (ms)"),
#             y=alt.Y("count()", title="Frequency"),
#             tooltip=[alt.Tooltip(f"{metric} (ms):Q", bin=True), "count()"]
#         ).properties(
#             title=f"Distribution of {metric} Times"
#         ).interactive()

#         output_file_json = os.path.join(output_dir, f"{metric}_histogram.json")
#         output_file_png = os.path.join(output_dir, f"{metric}_histogram.png")

#         chart.save(output_file_json)

#         vl_spec = chart.to_dict()
#         png_data = vlc.vegalite_to_png(vl_spec=vl_spec, scale=3)
#         with open(output_file_png, "wb") as file:
#             file.write(png_data)

def generate_histograms(metric_data, output_dir):
    for metric, values in metric_data.items():
        df = pd.DataFrame({f"{metric} (ms)": values})

        # Base chart (bars)
        base = alt.Chart(df).encode(
            x=alt.X(f"{metric} (ms):Q", bin=True, title=f"{metric} (ms)"),
            y=alt.Y("count()", title="Frequency")
        )

        # Bars
        bars = base.mark_bar().encode(
            tooltip=[alt.Tooltip(f"{metric} (ms):Q", bin=True), "count()"]
        )

        # Text labels above bars
        text = base.mark_text(
            align='center',
            baseline='bottom',
            dy=-5
        ).encode(
            text='count()'
        )

        # Combine the bars and text into a layered chart
        chart = alt.layer(bars, text).properties(
            title=f"Distribution of {metric} Times"
        ).interactive()

        output_file_json = os.path.join(output_dir, f"{metric}_histogram.json")
        output_file_png = os.path.join(output_dir, f"{metric}_histogram.png")

        # Save as interactive JSON
        chart.save(output_file_json)

        # Save as static PNG using vl-convert
        vl_spec = chart.to_dict()
        png_data = vlc.vegalite_to_png(vl_spec=vl_spec, scale=5)
        with open(output_file_png, "wb") as f:
            f.write(png_data)



def load_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data


def extract_metric_data(json_data, excluded_metrics=["dnsLookupTimes", "domLoading", "navigationStart"]):
    metrics = {}
    for site_data in json_data['sites'].values():
        for metric, value in site_data.items():
            if metric == "navigationTiming":
                for sub_metric, sub_value in value.items():
                    if sub_metric not in excluded_metrics and sub_value is not None:
                        metrics.setdefault(sub_metric, []).append(sub_value)


            elif metric not in excluded_metrics and value is not None:
                metrics.setdefault(metric, []).append(value)
    return metrics


if __name__ == '__main__':
    main()