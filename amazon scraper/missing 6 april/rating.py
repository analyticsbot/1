from selenium import webdriver
from threading import Thread
#from amazon_api_data2 import *
import pandas as pd
import time, re
from bs4 import BeautifulSoup

f = open('ratings.csv', 'rb')
data = f.read().split('\n')[:-1]
data = [d.strip().split(':')[1] for d in data]
num_threads = 16
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
        url = 'http://www.amazon.com/reviews/' + sku + '/'
        while True:
            driver.get(url)
            if 'robot check' not in driver.title.lower():
                break
            time.sleep(2)
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
            
        nrows = df.shape[0]
        df.loc[nrows+1] = [sku, str(Stars_and_numbers)]
        print df.shape
    dd.append(df)
    df.to_csv('updatedRating_' +  str(i) + '.csv', index = False)
    driver.close()
    
def split(a, n):
    k, m = len(a) / n, len(a) % n
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))


distributed_data = list(split(data, num_threads))
threads = []
for i in range(num_threads):
    data_thread = distributed_data[i]
    amzn = ''
    threads.append(Thread(target = downloadData, args=(i+1, data_thread, amzn, )))

j=1
for thread in threads:
    print 'starting scraper ##', j
    j+=1
    time.sleep(2)
    thread.start()

for thread in threads:
    thread.join()
