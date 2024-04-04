import tbselenium.common as cm
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem
from time import sleep
import os
import csv
import psutil
import re





# Store path of program as root path
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
# Set path to tor browser
tbb_dir = "/home/gilbert/tor-browser"


def main():
    print('blub')
    
    # Try to launch tor process with stem. If tor process is already running, catch the exception and print a message which asks the user to kill the process in system monitor.
    try:
        tor_process = launch_tbb_tor_with_stem(tbb_path=tbb_dir)
    except OSError:
        print('Tor process already running, please kill it in system monitor')



    
    # Tranco file to load. As seen from the directory where program.py lives, csv should be in the 'tranco' folder.
    tranco_data = load_tranco_file('top-1.csv')
    tranco_looper(tranco_data, tor_process)

    #tor_process.kill()
    



def load_tranco_file(csv_file):
    csv_data = []
    # Read all the entries with urls from the tranco csv file, and put them in a list.
    with open(os.path.join(ROOT_DIR, 'tranco', csv_file), mode='r') as file:
        csv_fileread = csv.reader(file)

        for entry in csv_fileread:
            csv_data.append(entry)
    
    return csv_data


def tranco_looper(tranco_data, tor_process):
     tranco_count = 0
     # Debug to check how long tranco data is
     print("tranco data is " + str(len(tranco_data)) + " long")
     # For each entry in the tranco data, do the stuff. Note: first column is the rank, second is the domain as a string.
     while tranco_count <= (len(tranco_data)-1):
        url = tranco_data[tranco_count]
        
        # Load the site using the load_site function and increase the tranco count
        # to keep track at how far we are in the tranco list.
        load_site(url, tor_process)
        tranco_count += 1
        

def load_site(url, tor_process):
    # Format the url to be correct
    url_checked = format_url(url[1])

    # Load the site using the TorBrowserDriver
    with TorBrowserDriver(tbb_dir, tor_cfg=cm.USE_STEM) as driver:
        driver.load_url(url_checked)
        # sleep(15)
        #measure_fcp_and_lcp(driver)
        #measure_total_blocking_time(driver)
        measure_performance(driver)
        
        # For debugging, only continue after pressing enter in terminal
        input("Press Enter to continue...")


    # Close the tor process after each crawl
    tor_process.kill()
    return True

def measure_performance(driver):
    performance_metrics = driver.execute_script(open(os.path.join(ROOT_DIR, 'JS_scripts', 'performanceMeasuring.js')).read() + " return getPerformanceMetrics();")
    print(performance_metrics)
    return performance_metrics 


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
        return f'http://{url}'
    else:
        print('URL already formatted correctly')
        return url
        




if __name__ == '__main__':
    main()