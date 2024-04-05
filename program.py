import tbselenium.common as cm
from tbselenium.tbdriver import TorBrowserDriver
from tbselenium.utils import launch_tbb_tor_with_stem
from selenium.common.exceptions import WebDriverException
from time import sleep
import os
import csv
import psutil
import re



###Paths of files and directories ###

# Store path of program as root path
ROOT_DIR = os.path.realpath(os.path.dirname(__file__))
# Set path to tor browser
tbb_dir = "/home/gilbert/tor-browser"
csv_file = 'top-1.csv'

### End of pahts and directories ###



def main():
    print('Main function started')
    
    # Tranco file to load. As seen from the directory where program.py lives, csv should be in the 'tranco' folder.
    tranco_data = load_tranco_file(csv_file)
    tranco_looper(tranco_data)

    #tor_process.kill()
    
def launch_tor_process():
    # Try to launch tor process with stem. If tor process is already running, catch the exception and print a message which asks the user to kill the process in system monitor.
    try:
        tor_process = launch_tbb_tor_with_stem(tbb_path=tbb_dir)
    except OSError:
        print('Tor process already running, please kill it in system monitor')
    
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
    tranco_count = 0
    # Debug to check how long tranco data is
    print("tranco data is " + str(len(tranco_data)) + " long")
    # For each entry in the tranco data, do the stuff. Note: first column is the rank, second is the domain as a string.
    while tranco_count <= (len(tranco_data)-1):
        url = tranco_data[tranco_count]
        
        # Load the site using the load_site function and increase the tranco count
        # to keep track at how far we are in the tranco list.
        load_site(url)
        tranco_count += 1

    print('Last site loaded, exiting program...')
        

def load_site(url):
    # Format the url to be correct
    url_checked = format_url(url[1])

    tor_process = launch_tor_process()
    print(f'Trying to load: {url_checked}')

    # Load the site using the TorBrowserDriver
    with TorBrowserDriver(tbb_dir, tor_cfg=cm.USE_STEM) as driver:
        # try:
        #     driver.load_url(url_checked)
        #     # sleep(15)
        #     #measure_fcp_and_lcp(driver)
        #     #measure_total_blocking_time(driver)
        #     measure_performance(driver)
            
        #     # For debugging, only continue after pressing enter in terminal or after waiting x seconds
        #     # Uncomment line for the behaviour you want
        #     input("Press Enter to continue...")
        #     # sleep(10)
        # except WebDriverException as e:
        #     print(f'Couldn\'t load {url_checked}. Error: {e}')
        #     print('Continuing with next site...')
        driver.load_url(url_checked)
        measure_performance(driver)
        input("Press Enter to continue...")

    # Close the tor process after each crawl
    tor_process.kill()
    #return True

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
        return f'https://{url}'
    else:
        print('URL already formatted correctly')
        return url
        




if __name__ == '__main__':
    main()