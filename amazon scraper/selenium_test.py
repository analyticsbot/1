from amazon.api import AmazonAPI
from selenium import webdriver
from unidecode import unidecode

AMAZON_ACCESS_KEY='AKIAIRGYI76BYPQZXAQQ'
AMAZON_SECRET_KEY ='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'
AMAZON_ASSOC_TAG =273589934636

AMAZON_ACCESS_KEY1='AKIAIYWGSVATZRMKAIRA'
AMAZON_SECRET_KEY1 ='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'
AMAZON_ASSOC_TAG1 =289838321798

AMAZON_ACCESS_KEY2='AKIAIUQZELPFNH3SZAYQ'
AMAZON_SECRET_KEY2 ='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'
AMAZON_ASSOC_TAG2 =475686369796

AMAZON_ACCESS_KEY3='AKIAJAAPCES4ASHEUTWA'
AMAZON_SECRET_KEY3 ='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'
AMAZON_ASSOC_TAG3 =901668519877

AMAZON_ACCESS_KEY4='AKIAJR7PJTLKOHW3LFUA'
AMAZON_SECRET_KEY4 ='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'
AMAZON_ASSOC_TAG4 =389369032532 

amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, region="US")
amazon1 = AmazonAPI(AMAZON_ACCESS_KEY1, AMAZON_SECRET_KEY1, AMAZON_ASSOC_TAG1, region="US")
amazon2 = AmazonAPI(AMAZON_ACCESS_KEY2, AMAZON_SECRET_KEY2, AMAZON_ASSOC_TAG2, region="US")
amazon3 = AmazonAPI(AMAZON_ACCESS_KEY3, AMAZON_SECRET_KEY3, AMAZON_ASSOC_TAG3, region="US")
amazon4 = AmazonAPI(AMAZON_ACCESS_KEY4, AMAZON_SECRET_KEY4, AMAZON_ASSOC_TAG4, region="US")

prod = {}
prod['asin'] = 'B00267T9LG'
prod['image'] = 'http://ecx.images-amazon.com/images/I/61sgsDW2hbL._SX425_.jpg'
prod['title'] = 'Motegi Racing MR107 Gloss Black Wheel With Machined Face (17x7.5"/5x114.3mm, +45mm offset)'
prod['price_new'] = '115.89'
data = []
asin = (prod['asin'])
image = prod['image']
title = prod['title']
price = prod['price_new']
url = 'http://www.amazon.com/dp/' + unidecode(asin)
driver = webdriver.Firefox()
driver.get(url)

# try to get the sales rank else return True. Does not work sometimes. Need to be more robust.
try:        
    salesRankElem = driver.find_element_by_id('SalesRank').text.strip()
except Exception,e:
    try:
        salesRankElem = driver.find_element_by_css_selector('.zg_hrsr_item').text.strip()
    except:
        try:
            product = amazon.lookup(ItemId=unidecode(asin))
            salesRank = product.sales_rank
        except:
            salesRank = 'NA'
Main_Image = driver.find_element_by_id('imgTagWrapperId').find_element_by_tag_name('img').get_attribute('src')
Num_Images =  len(driver.find_element_by_id('altImages').find_elements_by_css_selector('.a-spacing-small.item'))
Title = title
Price = price
Average_Customer_Review = driver.find_element_by_css_selector('.reviewCountTextLinkedHistogram.noUnderline').get_attribute('title')
Ratings = driver.find_elements_by_css_selector('.a-histogram-row')
Stars_and_numbers = {}
for rating in Ratings:
    try:
        key = rating.find_elements_by_css_selector('.a-text-right.aok-nowrap')[0].text
        value = rating.find_elements_by_css_selector('.a-text-right.aok-nowrap')[1].text
        Stars_and_numbers[key] = value
    except:
        key = rating.find_elements_by_css_selector('.a-nowrap')[0].text
        value = rating.find_elements_by_css_selector('.a-nowrap')[1].text
        Stars_and_numbers[key] = value
    
Product_Link = url
product_0 = amazon.lookup(ItemId=asin)
Description = product_0.editorial_review
features = driver.find_element_by_id('feature-bullets').find_elements_by_tag_name('li')
Feature1 = features[1].text
Feature2 = features[2].text
Feature3 = features[3].text
Feature4 = features[4].text
Feature5 = features[5].text
brand = product_0.brand

breadcrums = driver.find_element_by_css_selector('.a-subheader.a-breadcrumb.feature').find_elements_by_tag_name('li')
b = ''
i = 0
for bread in breadcrums:
    if i%2==0:
        b = b + '|' + bread.text.strip()
        if i==0:
            Main_Cat = b[1:]
    i+=1
Category_Tree = b.replace('|||','|')[1:]
##product_1 = amazon1.lookup(ItemId=asin)
##product_2 = amazon2.lookup(ItemId=asin)
Dimensions = product_0.get_attributes(['ItemDimensions.Width', 'ItemDimensions.Height', 'ItemDimensions.Length', 'ItemDimensions.Weight'])
#product_3 = amazon3.lookup(ItemId=asin)
Shipping_Weight = float(product_0.get_attribute('PackageDimensions.Weight'))/100.00
ASIN = asin
#product_4 = amazon3.lookup(ItemId=asin)

Sold_and_shipped_by = driver.find_element_by_id('merchant-info').text.replace('\n','').strip()
Amazon_Best_Seller_Rank = salesRank
Num_of_reviews = driver.find_element_by_id('acrCustomerReviewText').text
Item_Model_Number = product_0.mpn
driver.close()
