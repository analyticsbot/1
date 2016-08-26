from selenium import webdriver
import os, time,re, requests
from amazon.api import AmazonAPI
import pandas as pd
from amazon_api_data import *
from text_unidecode import unidecode
from threading import Thread
import numpy as np
from bs4 import BeautifulSoup

all_files = os.listdir(".")
all_files = [f for f in all_files if f.endswith('.csv')]
print len(all_files)
#all_files = all_files[:1]
drivers = []
data_df = {}

def downloadData(filename, amazon_api_list):
    df = pd.read_csv(filename)
    data_df['df'] = df
    threads = []
    results = [None]
    for i, row in df.iterrows():
        amzn = amazon_api_list[i]
        threads.append(Thread(target = dataUpdate, args=(i, amzn, results, )))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    data_df.pop("df", None)
    #print data_df
    for i in range(df.shape[0]):
        values = data_df[str(i)]
        Amazon_Best_Seller_Rank = values[0]
        Num_of_reviews = values[1]
        Average_Customer_Review = values[2]
        Stars_and_numbers = values[3]
        df.ix[i, 'Average_Customer_Review'] = Average_Customer_Review
        df.ix[i, 'Stars_and_numbers'] = str(Stars_and_numbers)
        df.ix[i, 'Num_of_reviews'] = Num_of_reviews
        df.ix[i, 'Amazon_Best_Seller_Rank'] = Amazon_Best_Seller_Rank      
                         
        
    df.to_csv(filename+'__', index = False, encoding = 'utf-8')
        
def dataUpdate(i, amzn_, results):
    #print 'dataUpdated'
    df =data_df['df']
    Average_Customer_Review = df.iloc[i]['Average_Customer_Review']
    Stars_and_numbers = df.iloc[i]['Stars_and_numbers']
    Amazon_Best_Seller_Rank = df.iloc[i]['Amazon_Best_Seller_Rank']
    Num_of_reviews = df.iloc[i]['Num_of_reviews']
    url = df.iloc[i]['Product_Link']
    asin = re.findall(r'dp/(.*?)$', url)[0]
    values = []

    if Amazon_Best_Seller_Rank in ['', 'NA']:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text)
        s = soup.find(attrs = {'id':'SalesRank'}).getText()
        Amazon_Best_Seller_Rank = re.findall(r'Amazon Best Sellers Rank:\s*(.*?)\sin', s)

        
    values.append(Amazon_Best_Seller_Rank)
    

    if (Average_Customer_Review in [np.nan, '', 'NA']) or (Stars_and_numbers in [np.nan, '{}', 'NA']) or\
       Num_of_reviews in [np.nan, '', 'NA']:
        product = amzn_.lookup(ItemId = asin)
        review_url = product.reviews[1]
        #print review_url
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        response = requests.get(review_url, headers=headers)
        soup = BeautifulSoup(response.text)
        try:
            Average_Customer_Review = soup.find(attrs = {'class':'asinReviewsSummary'}).find('img')['title']
        except:
            Average_Customer_Review = 'NA'
        try:
            ratings_ = soup.find(attrs= {'class':'txtsmaller histogramPPD'}).findAll('div')
            
            Stars_and_numbers = {}
            for j in ratings_:
                try:
                    f = j['title'].replace('of rating','').strip().split('represent')
                    key = f[0]
                    value= f[1]
                    Stars_and_numbers[key] = value
                except:
                    pass
        except:
            Stars_and_numbers = {}
        try:
            Num_of_reviews = soup.find(attrs = {'class':'crIFrameHeaderHistogram'}).find('b').getText()
        except:
            Num_of_reviews = 'NA'

    values.append(Num_of_reviews)
    values.append(Average_Customer_Review)
    values.append(Stars_and_numbers)

    data_df[str(i)] = values


for file_ in all_files:
    
    filename =  file_ + '__'
    if not os.path.exists(filename):
        time.sleep(2)
        print file_
        downloadData(file_, amazon_api_list)

