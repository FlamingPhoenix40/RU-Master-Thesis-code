#import psutil



# Currently not used; consolidated in tranco_looper
# because we now work with 1 window where we open and close tabs 
# instead of killing and restarting the browser for each site.
def load_site(url):
    global tranco_count
    print('We are now using the load_site function')
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



# Between control port and savelogging in launch_tor_process()

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