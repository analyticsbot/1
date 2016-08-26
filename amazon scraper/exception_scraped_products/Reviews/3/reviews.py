from selenium import webdriver
from threading import Thread
from amazon_api_data3 import *
import pandas as pd
import time, re, requests
from bs4 import BeautifulSoup

f = open('ASIN_3.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]
num_threads = 16
dd = []

def downloadData(i, data_thread, amzn):
    df = pd.DataFrame(columns = ['SKU', 'Average_Customer_Review', 'Num_of_reviews'])
    driver = webdriver.Firefox()
    count = 0
    for sku in data_thread:
        count +=1
        if count%100==0:
            print count
        time.sleep(1)
        
        try:
            product = amzn.lookup(ItemId = sku)
            url =  product.reviews[1]      
            
            #driver.get(url)
            while True:
                response = requests.get(url)
                if response.status_code==200:
                    break
                time.sleep(2)
            #soup1 = BeautifulSoup(driver.page_source)
            soup1 = BeautifulSoup(response.text)
            #time.sleep(1)
            try:
                Average_Customer_Review = soup1.find(attrs={'class':'asinReviewsSummary'}).find('img')['title']
            except:
                Average_Customer_Review = 'NA'
            try:
                Num_of_reviews = soup1.find(attrs={'class':'crIFrameHeaderHistogram'}).find('b').getText()
            except:
                Num_of_reviews = 'NA'
        except:
            url = 'http://www.amazon.com/reviews/' + sku + '/'
            driver.get(url)
            time.sleep(1)
            try:
                Average_Customer_Review = driver.find_element_by_css_selector('.arp-rating-out-of-text').text
            except:
                Average_Customer_Review = 'NA'
            try:
                Num_of_reviews = driver.find_element_by_css_selector('.a-size-medium.a-text-beside-button.totalReviewCount').text
            except:
                Num_of_reviews = 'NA'
            
        nrows = df.shape[0]
        df.loc[nrows+1] = [sku, Average_Customer_Review, Num_of_reviews]
    dd.append(df)
    df.to_csv('updatedReviews' +  str(i) + '.csv', index = False)
    driver.close()
    
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
    time.sleep(2)
    thread.start()

for thread in threads:
    thread.join()
