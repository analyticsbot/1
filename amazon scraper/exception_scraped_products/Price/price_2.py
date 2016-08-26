from selenium import webdriver
from threading import Thread
from amazon_api_data1 import *
import pandas as pd
import time, re, requests
from bs4 import BeautifulSoup

f = open('asins.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip() for d in data]
num_threads = 16
dd = []

def downloadData(i, data_thread, amzn):
    df = pd.DataFrame(columns = ['SKU', 'Price'])
    #driver = webdriver.Firefox()
    count = 0
    for sku in data_thread:
        count +=1
        if count%100==0:
            print count
        time.sleep(1)
        try:
            product = amzn.lookup(ItemId = sku)
            price =  product.price_and_currency[1]
        except:
            price = None
        if price in [None, 'USD']:
            url = 'http://www.amazon.com/reviews/' + sku + '/'
            #driver.get(url)
            while True:
                response = requests.get(url)
                if response.status_code==200:
                    break
                time.sleep(2)
            time.sleep(1)
            soup = BeautifulSoup(response.text)
            try:
                price = soup.find(attrs = {'class':'a-color-price arp-price'}).getText().strip().replace('$','')
            except:
                try:
                    price = soup.find(attrs = {'class':'a-color-price'}).getText().strip().replace('$','')
                except:
                    price = 'NA'
        nrows = df.shape[0]
        df[nrows+1] = [sku, price]
    dd.append(df)
    df.to_csv('updatedPrice' +  str(i) + '.csv', index = False)
    #driver.close()
    
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
    time.sleep(1)
    thread.start()

for thread in threads:
    thread.join()
