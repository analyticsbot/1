# import all required modules
from selenium import webdriver
import time, re, hashlib, csv, usaddress, logging, datetime, sys
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
LOGGER.setLevel(logging.ERROR)
from config_parser import *
from helper import getQuery,getRightSideData

# log file initialize
logging.basicConfig(level=logging.DEBUG, 
                    filename='logfile_' + username+'.log', # log to this file
                    format='%(asctime)s -- %(message)s') # include timestamp
logging.info("Sentences will following keywords will be ignored -- " + ', '.join(ignore_keywords))
logging.info("Process started for " + salutation  + ' ' +client_name + ', address = '+ client_address)
logging.info("Billing details, billing_card_number = " + billing_card_number  + ', card_cvv_number: ' +card_cvv_number + \
             ', billing_address = '+ billing_address + ', billing_expiry_date = ' + billing_expiry_date)
logging.info("Starting the process. Variables are state = " + state + ", county = " + county + ",keyword = " + keyword + \
             ", document types selected are " + '; '.join(doc_types) + ", for year(s)" + '; '.join(years))

try:
    writer = pd.ExcelWriter('client_log_'+ username +'.xlsx')
    df_data = pd.read_excel('client_log_'+ username +'.xlsx','Sheet1')
    print("Opened the client log file. Read the contents into a dataframe!")
    logging.info("Opened the client log file. Read the contents into a dataframe!")
    #change these 
    stop_last_document_left = df_data.iloc[df_data.shape[0]-1]['last_document_left']
    stop_right_side_name = df_data.iloc[df_data.shape[0]-1]['right_side_name']
    stop_right_side_address = df_data.iloc[df_data.shape[0]-1]['right_side_address']
    stop_right_side_date = df_data.iloc[df_data.shape[0]-1]['right_side_date']
except:
    writer = pd.ExcelWriter('client_log_'+ username +'.xlsx', engine='xlsxwriter')
    df_data = pd.DataFrame(columns=headers)
    stop_last_document_left = ''
    stop_right_side_name = ''
    stop_right_side_address = ''
    stop_right_side_date = ''

try:
    df_past = pd.read_csv(input_file_name)
    logging.info("Successfully read last file : " + input_file_name)
except:
    df_past = False
    logging.error("Cannot read last file : " + input_file_name)

# initialize pandas
df = pd.DataFrame(columns = headers)

# start the firefox instance
driver = webdriver.Firefox()
#driver = webdriver.Chrome('chromedriver.exe')
driver.maximize_window()
driver.get(url_login)

# username handling on the website
username_elem = driver.find_element_by_id('UserName')
username_elem.send_keys(username)

# password handling
pwd_elem = driver.find_element_by_id('Password')
pwd_elem.send_keys(pwd)

# press enter to login
pwd_elem.submit()

logging.info("Successfully logged into account : " + username)

# waiting for 5 second before proceeding
time.sleep(5)
driver.get(flexi_search_url)

# waiting for 5 second before proceeding
time.sleep(10)
driver.find_element_by_name('Advanced').click()
query = getQuery(state, keyword, county, doc_types, years)
logging.info("Query for this search : " + query)
             
textarea = driver.find_element_by_xpath('//*[@id="flex"]/ng-switch/advanced-flex-search/div/div[3]/div/textarea')
textarea.send_keys(query)
driver.find_element_by_css_selector('.runflexsrch-btncntnr').click()

time.sleep(30)
##driver.find_element_by_xpath('//*[@id="body"]/div[7]/div/div').click()
##time.sleep(15)
logging.info("Starting parsing data................!!")
count = 0
post_count = 0
stop_post_count = 0
doc_count = 0
cur_date = str(datetime.datetime.now().strftime ("%Y-%m-%d"))
text_box_left = ''
continue_ = True

while True:
    if count == 0:
        doc_count = driver.find_element_by_css_selector('.doc-count.ng-binding').text
        logging.info("Total document available -- " + str(doc_count) + '-- Parsing page 1')
    else:
        driver.find_element_by_link_text('Next').click()
        logging.info("Parsing page "+  str(count+1))
    count +=1
        
    if MAX_PAGES_SCRAPE !='ALL' and count> MAX_PAGES_SCRAPE:
        break
    
    results =  driver.find_elements_by_id('flexSearchResults')
    try:
        driver.execute_script("return arguments[0].scrollIntoView();", results[0])
        time.sleep(2)
    except:
        pass   

    for result in results:
        post_count +=1
        rightSideDataGood = 0
        leftSideParseGood = 0
        ignoreKeywordsPresent = 0
        if (results.index(result)+1) %2 == 0:
            driver.execute_script("return arguments[0].scrollIntoView();", result)
            time.sleep(3)
        try:
            text_box_left = result.find_element_by_css_selector('.col-md-10.flexsearch-highlights').text
        except:
            continue
        try:
            DOCUMENT_TYPE_LEFT = result.find_element_by_css_selector('.doc-title-textdecoration').get_attribute('title')
        except:
            DOCUMENT_TYPE_LEFT = 'NA'
        
        try:
            x = result.find_elements_by_css_selector('.doc-data-style.ng-binding')
        except:
            pass            
        DOCUMENT_TYPE_RIGHT, RECORDING_DATE, APN,ADDRESS, address_number_right,streetName_right,\
                PlaceName_right,  StateName_right, ZipCode_right, OWNER_BORROWER,\
                SELLER_LENDER = getRightSideData(x)

        if ((OWNER_BORROWER.strip() not in ['NA','']) and (ADDRESS.strip() not in ['NA','']) and\
             (DOCUMENT_TYPE_RIGHT.strip() not in ['NA',''])  and (APN.strip() not in ['NA',''])):
            rightSideDataGood = 1
                
        try:
            data_from_left = text_box_left.lower().split(keyword.replace('"',''))[-1]
            name_address = re.findall(r'\s([a-z][a-z]+.*?)$', data_from_left)[0]
            try:
                name_address = re.findall(r'(\w\w.*?\s\w\w\.?\s*\d\d\d\d\d)', name_address)[0]
            except:
                name_address = ''
                
            name_address_split = name_address.split()
            b = 0
            for i in name_address_split:
                b+=1
                try:
                    i = int(i)
                    isinstance(i, int)
                    break
                except Exception,e:
                    pass

            name = ' '.join(name_address_split[:b-1]).title()
            name = name.split()
            name = ' '.join([i for i in name if len(i)>1])
            address = ' '.join(name_address_split[b-1:]).title()
            parse_address = usaddress.parse(address)
            parse_address_dict = {}
            for i in parse_address:
                if i[1] not in parse_address_dict.keys():
                    parse_address_dict[i[1]] = i[0]
                    logging.info("parse start - " + parse_address_dict[i[1]])
                else:
                    parse_address_dict[i[1]] += ' '+ i[0]
                    logging.info("parse end - " + parse_address_dict[i[1]])
            try:
                address_number = str(parse_address_dict['AddressNumber']).title()
            except:
                address_number = 'NA'
            try:
                streetName = str(parse_address_dict['StreetName']).title()
            except:
                streetName = 'NA'
            try:
                StreetNamePostType = str(parse_address_dict['StreetNamePostType']).title()
            except:
                StreetNamePostType = 'NA'
            try:
                PlaceName = str(parse_address_dict['PlaceName']).title()
            except:
                PlaceName = 'NA'
            try:
                StateName = str(parse_address_dict['StateName']).upper()
            except:
                StateName = 'NA'
            try:
                ZipCode = parse_address_dict['ZipCode']
            except:
                ZipCode = 'NA'
            try:
                StreetNamePostType = str(parse_address_dict['StreetNamePostType']).title()
            except:
                StreetNamePostType = 'NA'
            try:
                StreetNamePreDirectional = str(parse_address_dict['StreetNamePreDirectional']).title()
            except:
                StreetNamePreDirectional = 'NA'
            is_parsed = 1
            leftSideParseGood = 1
        except:
            is_parsed = 0

        if not any(word in text_box_left.lower() for word in ignore_keywords):
            ignoreKeywordsPresent = 1

        logging.info("Record number - " + str(post_count) + "; Right hand name and address present. Parsed full address -- " + address \
                              + '; streetName = ' + streetName + '; PlaceName = '+ PlaceName + '; StateName = ' + StateName\
                              + '; ZipCode = ' + ZipCode)
                
        df.loc[post_count] = [cur_date, text_box_left, DOCUMENT_TYPE_LEFT, DOCUMENT_TYPE_RIGHT, RECORDING_DATE, APN, \
                          ADDRESS, address_number_right, streetName_right, PlaceName_right, StateName_right, ZipCode_right, OWNER_BORROWER, SELLER_LENDER, data_from_left, name_address, name, address,\
                          address_number, streetName, StreetNamePostType, PlaceName, StateName,\
                     ZipCode, StreetNamePostType, StreetNamePreDirectional, is_parsed]                    
            
    
##nrow = df_data.shape[0]
##parsed_rows_total = sum(list(df['is_parsed']))
##df_data.loc[nrow+1] = [str(datetime.datetime.now()), username, state, county, keyword, ', '.join(years),\
##                       last_document_type, last_document_left, right_side_name, right_side_address,\
##                       right_side_date , ','.join(doc_types), doc_count, text_box_left_parsed,\
##                       parsed_rows_total,client_name, client_address, billing_card_number, \
##                       card_cvv_number, billing_address, billing_expiry_date]
##df_data.to_excel(writer,'Sheet1', index = False, header = headers)
##writer.save()
##logging.info("Client log file generated as excel")
##logging.info("Total number of rows parsed successfully :: " + str(parsed_rows_total))
##driver.close()
##logging.info("Total pages scraped : " + str(count))
##logging.info("Total records scraped : " +  str(df.shape[0]))
##df.to_csv(output_file_name[:-4]+'_testing.csv', index = True)
##new_df = df[['OWNER_BORROWER','ADDRESS','address_number_right', 'streetName_right', 'PlaceName_right', 'StateName_right',
##                             'ZipCode_right','parsed_name', 'parsed_address', 'address_number', 'streetName','StreetNamePostType', 'PlaceName', 'StateName',\
##                             'ZipCode', 'DOCUMENT_TYPE_LEFT']]
##new_df.to_csv(output_file_name, index = False)
##logging.info("Output written to file : " + output_file_name)
##df_bad.to_csv(output_file_name[:-4] + '_bad_data.csv', index = True)
##logging.info("Bad Output written to file : " + output_file_name[:-4] + '_bad_data.csv')
##logging.shutdown()
