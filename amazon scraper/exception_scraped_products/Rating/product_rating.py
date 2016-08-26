from selenium import webdriver
from threading import Thread
from amazon_api_data2 import *
import pandas as pd
import time, re
from bs4 import BeautifulSoup

f = open('exception_scraped_products_rating.txt', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip().split(':')[1] for d in data]
num_threads = 2
dd = []

def downloadData(i, data_thread, amzn):
    df = pd.DataFrame(columns = ['SKU', 'Rating'])
    driver = webdriver.Firefox()
    count = 0
    for sku in data_thread:
        #print sku
        count +=1
        if count%100==0:
            print count
        time.sleep(2)
        Stars_and_numbers = {}
        try:
            product = amzn.lookup(ItemId = sku)
            url =  product.reviews[1]      
            
            driver.get(url)
            soup1 = BeautifulSoup(driver.page_source)
            time.sleep(1)
            ratings_ = soup1.find(attrs={'class':'txtsmaller histogramPPD'}).findAll('div')
                
            Stars_and_numbers = {}
            for i in ratings_:
                try:
                    f = i['title'].replace('of rating','').strip().split('represent')
                    key = f[0]
                    value= f[1]
                    Stars_and_numbers[key] = value
                except:
                    pass
        except:
            try:
                url = 'http://www.amazon.com/reviews/' + sku + '/'
                driver.get(url)
                time.sleep(1)
                Stars_and_numbers = {}
                rows = driver.find_elements_by_css_selector('.a-histogram-row')
                for row in rows:
                    try:
                        star_ratings = row.find_elements_by_css_selector('.a-text-right.aok-nowrap')
                        key = star_ratings[0].text
                        value = star_ratings[1].text
                        Stars_and_numbers[key] = value
                    except:
                        pass
                
            except:
                Stars_and_numbers = {}
            
        nrows = df.shape[0]
        df.loc[nrows+1] = [sku, str(Stars_and_numbers)]
        print df.shape
    dd.append(df)
    df.to_csv('updatedRating_' +  str(i) + '.csv', index = False)
    driver.close()
    
data_per_thread = len(data)/(num_threads-1)+1
threads = []
for i in range(num_threads):
    data_thread= data[i*data_per_thread:(i+1)*data_per_thread]
    #print data_thread
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
