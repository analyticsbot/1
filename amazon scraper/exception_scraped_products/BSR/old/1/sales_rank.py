from selenium import webdriver
from threading import Thread
from amazon_api_data1 import *
import pandas as pd
import time, re

f = open('ASIN_BSR_1.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]
num_threads = 16
dd = []

def getElement(product_details, element):    
    for product_detail in product_details:
        name = product_detail.find_element_by_tag_name('th').text.strip()
        if name == element:
            return product_detail.find_element_by_tag_name('td').text.strip()
        
def downloadData(i, data_thread, amzn):
    df = pd.DataFrame(columns = ['SKU', 'Sales Rank'])
    driver = webdriver.Firefox()
    count = 0
    for sku in data_thread:
        count +=1
        if count%100==0:
            print count
        time.sleep(1)
        try:
            product = amzn.lookup(ItemId = sku)
            sales_rank =  product.sales_rank
        except:
            sales_rank = None
        if not sales_rank:
            url = 'http://www.amazon.com/dp/' + sku + '/'
            while True:
                driver.get(url)
                if 'robot' not in driver.title.lower():
                    break
                time.sleep(2)
            time.sleep(1)
            try:
                sales_rank = driver.find_element_by_css_selector('#SalesRank').text
                sales_rank = re.findall(r'\#(.*?)\sin', sales_rank)[0].replace(',','')
            except:
                try:
                    try:
                        product_details = driver.find_element_by_css_selector('#productDetails_techSpec_section_1').find_elements_by_tag_name('tr')
                    except:
                        product_details = []
                    try:
                        product_details += driver.find_element_by_css_selector('#productDetails_detailBullets_sections1').find_elements_by_tag_name('tr')
                    except:
                        pass
                    try:
                        product_details += driver.find_element_by_css_selector('#productDetails_techSpec_section_2').find_elements_by_tag_name('tr')
                    except:
                        pass
                    sales_rank = getElement(product_details, 'Best Sellers Rank').strip()
                    sales_rank = re.findall(r'\#(.*?)\sin', sales_rank)[0].replace(',','')
                except:
                    sales_rank = 'NA'
        nrows = df.shape[0]
        df.loc[nrows+1] = [sku, sales_rank]
    dd.append(df)
    df.to_csv('updatedSalesRank' +  str(i) + '.csv', index = False)
    
data_per_thread = len(data)/(num_threads-1)+1
threads = []
for i in range(num_threads):
    data_thread= data[i*data_per_thread:(i+1)*data_per_thread]
    amzn = amazon_api_list1[i]
    threads.append(Thread(target = downloadData, args=(i+1, data_thread, amzn, )))

j=1
for thread in threads:
    print 'starting scraper ##', j
    j+=1
    thread.start()
    time.sleep(2)

for thread in threads:
    thread.join()
