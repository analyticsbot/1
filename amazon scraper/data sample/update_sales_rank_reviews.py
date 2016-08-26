from selenium import webdriver
import os, time,re
from amazon.api import AmazonAPI
import pandas as pd
from amazon_api_data import *
from text_unidecode import unidecode

all_files = os.listdir(".")
all_files = [f for f in all_files if f.endswith('.csv')]
all_files = all_files[:1]
print all_files
drivers = []
data_df = {}

for i in range(16):
    drivers.append(webdriver.Firefox())
    time.sleep(1)

def downloadData(filename, amazon_api_list):
    df = pd.read_csv(filename)
    data_df['df'] = df
    threads = []
    for i, row in df.iterrows():
        amzn = amazon_api_list[i]
        d = drivers[i]
        threads.append(Thread(target = dataUpdate, args=(i, amzn, d, )))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    df = data_df['df']
    df.to_csv(filename+'.__', index = False, encoding = 'utf-8')
        
def dataUpdate(i, amzn_, driver_):
    df =data_df['df']
    Average_Customer_Review = df.iloc[i]['Average_Customer_Review']
    Stars_and_numbers = df.iloc[i]['Stars_and_numbers']
    Amazon_Best_Seller_Rank = df.iloc[i]['Amazon_Best_Seller_Rank']
    Num_of_reviews = df.iloc[i]['Num_of_reviews']
    url = df.iloc[i]['Product_Link']
    asin = re.findall(r'dp/(.*?)$', url)[0]

    if Amazon_Best_Seller_Rank in ['', 'NA']:
        driver_.get(url)
        s = driver_.find_element_by_id('SalesRank').text
        sales_rank = re.findall(r'Amazon Best Sellers Rank:\s*(.*?)\sin', s)
        df.iloc[i]['Amazon_Best_Seller_Rank'] = sales_rank
        df.iloc[i]['Num_of_reviews'] =  driver_.find_element_by_id('acrCustomerReviewText').text

    if (Average_Customer_Review in ['', 'NA']) or (Stars_and_numbers in ['', 'NA']):
        product = amzn_.lookup(ItemId = asin)
        review_url = product.review[1]
        driver_.get(review_url)
        try:
            Average_Customer_Review = driver_.find_element_by_css_selector('.asinReviewsSummary').find_element_by_tag_name('img').get_attribute('title')
        except:
            Average_Customer_Review = 'NA'
        df.iloc[i]['Average_Customer_Review'] = Average_Customer_Review
        try:
            ratings_ = driver_.find_element_by_css_selector('.txtsmaller.histogramPPD').find_elements_by_tag_name('div')
            
            Stars_and_numbers = {}
            for i in ratings_:
                try:
                    f = i.get_attribute['title'].replace('of rating','').strip().split('represent')
                    key = f[0]
                    value= f[1]
                    Stars_and_numbers[key] = value
                except:
                    pass
        except:
            Stars_and_numbers = {}
        df.iloc[i]['Stars_and_numbers'] = Stars_and_numbers

    data_df['df'] = df


for file_ in all_files:
    downloadData(filename, amazon_api_list)
