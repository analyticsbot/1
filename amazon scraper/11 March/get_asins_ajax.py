from selenium import webdriver
from bs4 import BeautifulSoup
from threading import Thread
from text_unidecode import unidecode
from amazon.api import AmazonAPI
from selenium import webdriver
import pandas as pd
from amazon_api_data2 import *
import time, requests, csv,os

driver = webdriver.Firefox()

keyword = 'Clear Plastic Cups'
keyword = keyword.replace(' ','%20')
url = 'http://www.amazon.com/mn/search/ajax/ref=nb_sb_noss_2?url=search-alias%20aps&field-keywords=' +keyword + '&rh=i%20aps%20k%20Clear%20Plastic%20Cup&fromHash=&section=BTF&fromApp=gp%20search&fromPage=results&fromPageConstruction=auisearch&version=2&oqid=1458291095&atfLayout=list'
driver.get(url)
asin_elems = driver.find_elements_by_css_selector('.s-result-item.celwidget')

for elem in asin_elems:
    asin = elem.get_attribute('data-asin')

f=open('Keywords_1.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]
num_threads = 16

directory = 'Keyword2'
if not os.path.exists(directory):
    os.makedirs(directory)
    
def downloadData(i, data_, amz):
    f = open('downloaded_keywords_' +str(i)+'.csv', 'wb')
    writer = csv.writer(f)
    f1 = open('not_downloaded_keywords_' +str(i)+'.csv', 'wb')
    writer1 = csv.writer(f1)
    data_ = data_[::-1]
    for d in data_:
        time.sleep(1)
        searchterm = d.strip().replace('"','').replace("'",'').replace("/",' ')
        #print 'getting data for ', searchterm, ' using thread', i, '\n'      
        if os.path.exists(directory + '/'+ searchterm + '.csv'):
            continue
        try:
            data = getAmazonProducts(asin, amz)
            if len(data)>25:
                writer.writerow([searchterm])
                df = pd.DataFrame(columns = ['Main_Image' , 'Num_Images' , 'Title' , 'Price' , 'Average_Customer_Review' , \
                                         'Stars_and_numbers' , 'Product_Link' , 'Description' , 'Feature1' , 'Feature2' ,\
                                         'Feature3' , 'Feature4' , 'Feature5' , 'Category_Tree' , 'Main_Cat' , 'brand' , \
                                         'Dimensions' , 'Shipping_Weight_Ounces' , 'Item_Model_Number' , 'Sold_and_shipped_by' , \
                                         'Amazon_Best_Seller_Rank' , 'Num_of_reviews'])

                count = 1
                for d in data:
                    df.loc[count] = d
                    count +=1  

                df.to_csv(directory + '/'+ searchterm + '.csv', index = False, encoding = 'utf-8')
            else:
                writer1.writerow([searchterm])
        
        except Exception,e:
            print str(e)
            print 'no data for ', searchterm
            writer1.writerow([searchterm])

        
    f.close()
    f1.close()
    print 'work completed by scraper', i

data_per_thread = len(data)/(num_threads-1)+1
threads = []
for i in range(num_threads):
    data_thread= data[i*data_per_thread:(i+1)*data_per_thread]
    amzn = amazon_api_list1[i]
    threads.append(Thread(target = downloadData, args=(i+1, data_thread,amzn, )))

j=1
for thread in threads:
    print 'starting scraper ##', j
    j+=1
    thread.start()

for thread in threads:
    thread.join()
