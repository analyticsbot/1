# import all required modules
from selenium import webdriver
import time, re, hashlib, csv
import pandas as pd
from selenium.webdriver.common.keys import Keys
import usaddress
import logging, datetime, sys
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)

# static variables
username = 'Allenbruns'
url_login = 'https://web.datatree.com/Account/Login?ReturnUrl=%2f'
pwd = 'billie54'
state = 'CA'
county = 'ORANGE'
keyword = '"mail to"'
inputFile = 'dataoutput.csv'
output_file_name = 'dataoutput_' + username + '.csv'

MAX_PAGES_SCRAPE = 1

DOCUMENT_TYPE_LEFT_CHECK = ['Memorandum of Lease', 'Assignment',\
                            'Quit Claim',  'Grant Deed', 'Transfer',\
                            'Deed Of Reconveyance', 'Full Reconveyance',\
                            'Deed of Trust', 'Substitution of Trustee and Reconveyance']
DOCUMENT_TYPE_LEFT_CHECK = [d.upper() for d in DOCUMENT_TYPE_LEFT_CHECK]

BROWSER = 'FIREFOX' # 'CHROME'

def login(driver):    
    driver.maximize_window()
    driver.get(url_login)

    # username handling on the website
    while True:
        try:
            username_elem = driver.find_element_by_id('UserName')
            username_elem.send_keys(username)
            break
        except:
            pass
        
    # password handling
    pwd_elem = driver.find_element_by_id('Password')
    pwd_elem.send_keys(pwd)

    # press enter to login
    pwd_elem.submit()

    logging.info("Successfully logged into account : " + username)


def get_status(driver, address, state, county, DOCUMENT_TYPE_LEFT_CHECK ):
    # waiting for 5 second before proceeding
    time.sleep(5)
    flexi_search_url = 'https://web.datatree.com/flexsearch'
    driver.get(flexi_search_url)

    # waiting for 5 second before proceeding
    time.sleep(5)
    driver.find_element_by_name('Advanced').click()

    query = '(state:"' + state + ') AND (doc_full_text:"' + address + \
            ') AND (county:"' + county + '") '

    print query

    logging.info("Query for this search : " + query)
             
    textarea = driver.find_element_by_xpath('//*[@id="flex"]/ng-switch/advanced-flex-search/div/div[3]/div/textarea')
    textarea.send_keys(query)
    driver.find_element_by_css_selector('.runflexsrch-btncntnr').click()

    time.sleep(30)
    ##driver.find_element_by_xpath('//*[@id="body"]/div[7]/div/div').click()
    ##time.sleep(15)
    logging.info("Starting parsing data")
    time.sleep(10)
    results =  driver.find_elements_by_id('flexSearchResults')
    time.sleep(10)
    try:
        driver.execute_script("return arguments[0].scrollIntoView();", results[0])
    except:
        pass
    time.sleep(10)
    post_count = 0
    status = 'OFF MARKET'
    for result in results:
        post_count +=1
        if (results.index(result)+1) %2 == 0:
            driver.execute_script("return arguments[0].scrollIntoView();", result)
            time.sleep(1)
            
            try:
                DOCUMENT_TYPE_LEFT = result.find_element_by_css_selector('.doc-title-textdecoration').get_attribute('title')
                last_document_type = DOCUMENT_TYPE_LEFT.upper()
            except:
                DOCUMENT_TYPE_LEFT = 'NA'

            try:
                x = result.find_elements_by_css_selector('.doc-data-style.ng-binding')
            except:
                pass
            try:
                DOCUMENT_TYPE_RIGHT = x[0].text.upper()
            except:
                DOCUMENT_TYPE_RIGHT = 'NA'

    if DOCUMENT_TYPE_LEFT in DOCUMENT_TYPE_LEFT_CHECK or DOCUMENT_TYPE_RIGHT in DOCUMENT_TYPE_LEFT_CHECK:
        status = 'SOLD'

    return status

# start the firefox instance
if BROWSER == 'FIREFOX':
    driver = webdriver.Firefox()
else:
    driver = webdriver.Chrome('chromedriver.exe')
login(driver)
df = pd.read_csv(inputFile)
df['status'] = ''
for i, row in df.iterrows():
    address = row['ADDRESS']
    status = get_status(driver, address, state, county, DOCUMENT_TYPE_LEFT_CHECK)
    df.loc[i, 'status'] = status
    print address, status
driver.close()
    
logging.shutdown()
