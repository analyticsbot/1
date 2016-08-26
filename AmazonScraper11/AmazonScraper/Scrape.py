#!/usr/bin/python2


import csv
import os.path
from random import randint
import socket
from time import sleep
#from urllib import urlopen

from amazon.api import AsinNotFound
from amazon_scraper import AmazonScraper
import requests
import socks


# Ensuring that ProxyMesh works fine:
resp = requests.get('http://icanhazip.com')
print "My current IP address:", resp.content.strip()

AUTH = requests.auth.HTTPProxyAuth('manutd0707', 'manutd0707')
PROXIES = {'http': 'http://us-dc.proxymesh.com:31280'}
resp = requests.get('http://icanhazip.com', proxies=PROXIES, auth=AUTH, verify=False)
print "My new IP address via ProxyMesh:", resp.content.strip()
 
AMAZON_ACCESS_KEY = "AMAZON_ACCESS_KEY"
AMAZON_SECRET_KEY = "AMAZON_SECRET_KEY"
AMAZON_ASSOCIATE_TAG = "AMAZON_ASSOCIATE_TAG"

amzn = AmazonScraper(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOCIATE_TAG)
# You need 3 things for the above keys: AWS account (first two codes above), 
# Amazon Associates account (final code), and then you need to sign up to use 
# the Product Advertising API within the Associates account

filename = "reviews_allinfo.csv"
filename2 = "reviews_notext.csv"

save_path = 'c:/output/'
 
with open('product_ids.csv', 'rb') as f:
    csv_f = csv.reader(f)
    items = [row[0].strip() for row in csv_f]
    
    
for number in items:
    
    try:
        p = amzn.lookup(ItemId=number)
    except AsinNotFound as e:
        print "Product {} was not found".format(number)
        continue
     
    rs = p.reviews()
    counter = 0    
    
    try:
        for review in rs:
            print review.asin
            print review.url
            print review.soup            
            counter += 1
            
            if (counter%80) == 0:
                sleep(randint(3,4))
            
            # you have to encode it to some encodeing because it comes
            # as unicode
            review_text = review.text
            if isinstance(review_text, unicode):                
                review_text = review_text.encode('ascii', 'replace')
                
            if review.user_id is not None:
                name_of_file = "%s_%s.txt" % (review.asin, review.user_id)
                completeName = os.path.join(save_path, name_of_file)
                file3 = open(completeName, "w")
                file3.write(review_text)     
                
                with open(filename, "a") as myfile:
                    myfile.write("%s," % (review.asin))
                    myfile.write("%s," % (review.user_id))
                    myfile.write("%s," % (review.id))
                    myfile.write("%s," % (review.date))
                    myfile.write("%s," % (review.rating))
                    myfile.write("%s," % (review.helprate))
                    myfile.write('"%s"\n' % review_text)
                    
                with open(filename2, "a") as myfile2:
                    myfile2.write("%s," % (review.asin))
                    myfile2.write("%s," % (review.user_id))
                    myfile2.write("%s," % (review.id))
                    myfile2.write("%s," % (review.date))
                    myfile2.write("%s," % (review.rating))
                    myfile2.write("%s\n" % (review.helprate))
                    
            if review.user_id is None:
                name_of_file = "%s_%s_%s.txt" % (review.asin, review.user_id, counter)
                completeName = os.path.join(save_path, name_of_file)
                file3 = open(completeName,"w")
                file3.write('%s\n' % review_text) 
                
                with open(filename, "a") as myfile:
                    myfile.write("%s," % (review.asin))
                    myfile.write("none_%s," % (counter))
                    myfile.write("%s," % (review.id))
                    myfile.write("%s," % (review.date))
                    myfile.write("%s," % (review.rating))
                    myfile.write("%s," % (review.helprate))
                    myfile.write('"%s"\n' % review_text)
                    
                with open(filename2, "a") as myfile2:
                    myfile2.write("%s," % (review.asin))
                    myfile2.write("none_%s," % (counter))
                    myfile2.write("%s," % (review.id))
                    myfile2.write("%s," % (review.date))
                    myfile2.write("%s," % (review.rating))
                    myfile2.write("%s\n" % (review.helprate))
    except UnicodeEncodeError as e:
        print "Skipping undecodeable prduct URI"
        print e            
    except requests.exceptions.HTTPError as e:
        print e
    except requests.exceptions.ConnectTimeout as e:
        print e

print "All done"                