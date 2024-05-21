import tbselenium.common as cm
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem
from selenium.common.exceptions import WebDriverException
import os
import csv
#import psutil
import re
import json
import time
from selenium.webdriver.common.utils import free_port
import tempfile
from os.path import join




###Paths of files and directories, as well as global variables ###

# Store path of program as root path
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
# Set path to tor browser
tbb_dir = "/home/gilbert/tor-browser"
# torrc_path = "/home/gilbert/GitKraken/RU-Master-Thesis-Code/torrc_custom"
csv_file = 'top-1000.csv'
tranco_count = 0
socks_port = free_port()
# json_name = input('Enter name of json file to store metrics in: ')
json_name = '1000-testrun.json'
log_file = 'debug file /home/gilbert/tor_logs/tor_1000test.log'
### End of pahts and directories ###



def main():
    print('Main function started')
    
    
    # Tranco file to load. As seen from the directory where program.py lives, csv should be in the 'tranco' folder.
    tranco_data = load_tranco_file(csv_file)
    print('Tranco data loaded')
    tranco_looper(tranco_data)
    
    #tor_process.kill()
    
def launch_tor_process(log=log_file):
    # Try to launch tor process with stem. If tor process is already running, catch the exception and print a message which asks the user to kill the process in system monitor.
    
    control_port = free_port()
    # tor_data_dir = tempfile.mkdtemp()
    # tor_binary = join(tbb_dir, cm.DEFAULT_TOR_BINARY_PATH)
    # print("SOCKS port: %s, Control port: %s" % (socks_port, control_port))

    # torrc = {'ControlPort': str(control_port),
    #          'SOCKSPort': str(socks_port),
    #          'DataDirectory': tor_data_dir}

    # torrc = {'Log': 'debug file /home/gilbert/tor_logs/tor_selenium.log',
    #          'SafeLogging': str(0),
    #          'LogTimeGranularity': str(1)}
    # print(torrc)
    # log = 'debug file /home/gilbert/tor_logs/tor_selenium.log'
    safelogging = 0
    logtimegranularity = 1
    tor_binary = join(tbb_dir, cm.DEFAULT_TOR_BINARY_PATH)
    clientonionauthdir = '/home/gilbert/tor-browser/Browser/TorBrowser/Data/Tor/onion-auth'
    datadirectory = '/home/gilbert/tor-browser/Browser/TorBrowser/Data/Tor'
    geoipfile = '/home/gilbert/tor-browser/Browser/TorBrowser/Data/Tor/geoip'
    geoipv6file = '/home/gilbert/tor-browser/Browser/TorBrowser/Data/Tor/geoip6'
    torrc = {'Log': str(log),
             'SafeLogging': str(safelogging),
             'LogTimeGranularity': str(logtimegranularity),
             'SOCKSPort': str(socks_port),
             'ControlPort': str(control_port),
             'ClientOnionAuthDir': str(clientonionauthdir),
             'DataDirectory': str(datadirectory),
             'GeoIPFile': str(geoipfile),
             'GeoIPv6File': str(geoipv6file)}

    

    try:
        tor_process = launch_tbb_tor_with_stem(tbb_path=tbb_dir, torrc=torrc, tor_binary=tor_binary)
    except OSError:
        #print('Tor process already running, please kill it in system monitor')
        print('Tor process seemingly already running, retrying...')
        tor_process = None

     
    
    return tor_process


def load_tranco_file(csv_file):
    csv_data = []
    # Read all the entries with urls from the tranco csv file, and put them in a list.
    with open(os.path.join(ROOT_DIR, 'tranco', csv_file), mode='r') as file:
        csv_fileread = csv.reader(file)

        for entry in csv_fileread:
            csv_data.append(entry)
    
    return csv_data


def tranco_looper(tranco_data):
    # Debug to check how long tranco data is
    global tranco_count
    print("tranco data is " + str(len(tranco_data)) + " long")
    # For each entry in the tranco data, do the stuff. Note: first column is the rank, second is the domain as a string.
    while tranco_count <= (len(tranco_data)-1):
        url = tranco_data[tranco_count]
        
        # Load the site using the load_site function and increase the tranco count
        # to keep track at how far we are in the tranco list.
        tranco_count += 1
        load_site(url)
        

    print('Last site loaded, exiting program...')
        

def load_site(url):
    global tranco_count
    # Format the url to be correct
    url_checked = format_url(url[1])

    tor_process = launch_tor_process()
    if tor_process is None:
        print('Could not launch Tor, retrying...')
        tranco_count -= 1
        return tranco_count
    
    print(f'Trying to load: {url_checked}')

    # Load the site using the TorBrowserDriver
    with TorBrowserDriver(tbb_dir, tor_cfg=cm.USE_STEM, socks_port=socks_port) as driver:
        try:
            driver.load_url(url_checked)
            # sleep(15)
            #measure_fcp_and_lcp(driver)
            #measure_total_blocking_time(driver)
            metrics = measure_performance(driver)
            store_perf_metrics_in_json(url_checked, metrics)
            
            # For debugging, only continue after pressing enter in terminal or after waiting x seconds
            # Uncomment line for the behaviour you want
            # input("Press Enter to continue...")
            # sleep(10)
        except WebDriverException as e:
            print(f'Couldn\'t load {url_checked}. Error: {e}')
            print('Continuing with next site...')
        # driver.load_url(url_checked)
        # metrics = measure_performance(driver)
        # store_perf_metrics_in_json(url_checked, metrics)
        # input("Press Enter to continue...")

    # Close the tor process after each crawl
    tor_process.kill()
    #return True

def measure_performance(driver):
    
    performance_metrics = driver.execute_script(open(os.path.join(ROOT_DIR, 'JS_scripts', 'performanceMeasuring.js')).read() + " return getPerformanceMetrics(navigationEntry);")
    print(performance_metrics)
    start_time = time.time_ns() / 1000000
    
    print(start_time)
    #response_start = performance_metrics['responseStart']
    #estimated_ttfb = response_start - start_time
    #print(f'Estimated Time to First Byte: {estimated_ttfb} ms')
    return performance_metrics 


def store_perf_metrics_in_json(url_checked, metrics, output_file=json_name):
    
    if os.path.exists(os.path.join(ROOT_DIR, 'json_files', output_file)):
        print(f'\n File {output_file} exists, loading data...\n')
        with open(os.path.join(ROOT_DIR, 'json_files', output_file), 'r') as file:
            data = json.load(file)
    else:
        print('\n No existing json file found, continuing...\n')
        data = {"sites": {}}

    data["sites"][url_checked] = metrics

    with open(os.path.join(ROOT_DIR, 'json_files', output_file), 'w') as file:
        print('Writing json file... \n')
        json.dump(data, file, indent=4)


# Currently not used; consolidated in measure_performance
# Cleanup later, leave for now in case of issues
def measure_fcp_and_lcp(driver):
    metrics = driver.execute_script(open(os.path.join(ROOT_DIR, 'JS_scripts', 'performanceMeasuring.js')).read() + " return getContentfulPaints();")

    if metrics['fcp']:
        print("First Contentful Paint: ", metrics['fcp'])
    else:
        print("First Contentful Paint: No value found")
    


# Currently not used; consolidated in measure_performance
# Cleanup later, leave for now in case of issues
def measure_total_blocking_time(driver):
    tbt_value = driver.execute_script(open(os.path.join(ROOT_DIR, 'JS_scripts', 'performanceMeasuring.js')).read() + " return estimatedTBT;")
    print("Estimated Blocking Time: ", tbt_value)

    
def format_url(url):
    # If the url does not start with http:// or https://, add it to the url
    if not re.match('(?:http|https)://', url):
        return f'https://{url}'
    else:
        print('URL already formatted correctly')
        return url
        




if __name__ == '__main__':
    main()