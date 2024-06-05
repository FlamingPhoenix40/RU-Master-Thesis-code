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

    fpc_times = extract_fcp_data(json_data)

    output_file_json = os.path.join(ROOT_DIR, 'graphs', 'fcp_times_histogram.json')
    output_file_png = os.path.join(ROOT_DIR, 'graphs', 'fcp_times_histogram.png')

    generate_fcp_histogram(fpc_times, output_file_json, output_file_png)



def generate_fcp_histogram(fcp_times, output_file_json, output_file_png):
    df = pd.DataFrame({'FCP Time (ms)': fcp_times})

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('FCP Time (ms):Q', bin=True, title = 'FCP Times (ms)'),
        y=alt.Y('count()', title = 'Frequency'),
        tooltip=[alt.Tooltip('FCP Time (ms):Q', bin=True), 'count()']
    ).properties(
        title='Distribution of FCP Times'
    ).interactive()

    chart.save(output_file_json)

    vl_spec = chart.to_dict()
    png_data = vlc.vegalite_to_png(vl_spec=vl_spec, scale=3)
    with open(output_file_png, 'wb') as file:
        file.write(png_data)

def load_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data


def extract_fcp_data(json_data):
    fcp_times=[]
    for site_data in json_data['sites'].values():
        fcp_times.append(site_data['fcp'])
    return fcp_times


if __name__ == '__main__':
    main()