# import the Flask class from the flask module and other required modules
from bs4 import BeautifulSoup
import requests, threading, re, os, Queue, mechanize, logging, gc, json,time
from random import choice 
from threading import Thread
from mechanize import Browser
from logging import FileHandler
from amazon.api import AmazonAPI
from selenium import webdriver
from text_unidecode import unidecode

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

try:
    from captcha_solver import CaptchaBreakerWrapper
except Exception as e:
    print '!!!!!!!!Captcha breaker is not available due to: %s' % e
    class CaptchaBreakerWrapper(object):
        @staticmethod
        def solve_captcha(url):
            msg("CaptchaBreaker in not available for url: %s" % url,
                level=WARNING)
            return None
        
_cbw = CaptchaBreakerWrapper()

def _has_captcha(response):
    return '.images-amazon.com/captcha/' in response.content

def _solve_captcha(response):
    soup = BeautifulSoup(response.content, "html.parser")
    forms = soup.findAll(itemprop="image")
    assert len(forms) == 1, "More than one form found."

    captcha_img = forms[0]['src']

    return _cbw.solve_captcha(captcha_img)
    
def _handle_captcha(session, response):
    response.meta = {}
    captcha_solve_try = response.meta.get('captcha_solve_try', 0)
    url = response.url
    
    captcha = _solve_captcha(response)

    if captcha is None:            
        response = response
    else:
        meta = response.meta.copy()
        meta['captcha_solve_try'] = captcha_solve_try + 1
        response = session.post(url, params = {'field-keywords': captcha})

    return response

def getProxies():
    proxy = []
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    html = response.content

    templs = re.findall(r'<tr><td>(.*?)</td><td>', html)
    templs2 = re.findall(r'</td><td>[1-99999].*?</td><td>', html)

    for i in range(len(templs)):
        proxy.append('http://' + (templs[i] + ":" + templs2[i].replace('</td><td>', '')))
    return proxy
    
proxies = getProxies()

def random_proxy():
    """ method to return a random proxy """
    return choice(proxies)

# list of available user agents
user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7"]

def random_user_agent():
    """ method to return a random user agent from the above list """
    return choice(user_agents)
        
def getAmazonProducts(searchterm, pg_max =2):
    url = 'http://www.amazon.co.uk/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' + '+'.join(searchterm.split())
    pg_num = 1
    prod = {}
    prod['numProducts'] = 0
    count = 0
    continue_ = True
    while continue_:
             
        if pg_num == 1:
            url = url
            pg_num += 1
        else:
            if pg_num == pg_max + 1:
                break
            url = 'http://www.amazon.co.uk/s/ref=sr_pg_' + str(pg_num) + '?rh=i%3Aaps%2Ck%3A' + '+'.join(searchterm.split()) + '&page=' + str(pg_num) + '&keywords'+  '+'.join(searchterm.split())
            pg_num += 1

        session = requests.Session()
        session.headers = random_user_agent()
        
##        proxy = random_proxy() # checks for a working proxy, else proceeds with the current ip
##        session.proxies = {'http': proxy}

        # retreived the response and pass to beautifulsoup
        response = session.get(url)
        print response.status_code
        if response.status_code !=200:
            break

##        while True:
##            # handle captcha if present
##            if _has_captcha(response):
##                response = _handle_captcha(session, response)
##            else:
##                break
        soup = BeautifulSoup(response.content, "html.parser")
        
        # get all the products on the search page
        elements = soup.findAll(attrs = {'class': 's-result-item'})
        prod['numProducts'] += len(elements) # increment the number of products

        # loop through the elements and get title, url, price_old, price_new, image url, asin and add to a dict object
        for elem in elements:
            print count   
            count +=1
            if count==15:
                continue_ = False
                break
            
            try:
                title = elem.find(attrs = {'class' : 'a-size-medium a-color-null s-inline s-access-title a-text-normal'}).getText()
            except Exception,e:
                try:
                    title = elem.find(attrs = {'class' : 'a-link-normal s-access-detail-page  a-text-normal'}).getText()
                except:
                    title = 'NA'
            try:
                url = elem.find(attrs = {'class' : 'a-link-normal s-access-detail-page  a-text-normal'}).attrs['href']
            except Exception,e:
                url = 'NA'
            try:
                price_old = re.findall(r'\d+.\d+', elem.find(attrs = {'class' : 'a-size-small a-color-secondary a-text-strike'}).getText())[0]
            except Exception,e:
                price_old = 'NA'
            
            try:
                image = elem.find(attrs = {'class' : 's-access-image cfMarker'}).attrs['src']
            except Exception,e:
                image = 'NA'
                
            try:
                asin = re.findall(r'dp\/(.*?)\/', url)[0]
            except Exception,e:
                asin =  'NA'
            try:
                price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-size-base a-color-price s-price a-text-bold'}).getText())[0]
            except Exception,e:
                try:
                    product = amazon_uk.lookup(ItemId=unidecode(asin))
                    price_new = str(product.price_and_currency[0])
                    if price_new is not None:
                        price_new = price_new
                    else:
                        price_new = 'NA'
                except:
                    try:
                        product = amazon_uk1.lookup(ItemId=unidecode(asin))
                        price_new = str(product.price_and_currency[0])
                        if price_new is not None:
                            price_new = price_new
                        else:
                            price_new = 'NA'
                    except:
                        try:
                            price_new = re.findall(r'\d+.\d+', elem.find(attrs = {'class': 'a-color-price'}).getText())[0]
                        except:
                            price_new = 'NA'

            prod['product' + str(count)] = {'title':title, 'url':url, 'price_old':price_old, 'price_new':price_new, 'image':image,\
                                                       'asin': asin}
            
            
            
    return prod

def getSKUData(prod, queue):
    data = []
    asin = (prod['asin'])
    image = prod['image']
    title = prod['title']
    price = prod['price_new']
    url = 'http://www.amazon.com/dp/' + (asin)
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
    try:
        Main_Image = driver.find_element_by_id('imgTagWrapperId').find_element_by_tag_name('img').get_attribute('src')
    except:
        Main_Image = 'NA'
    try:
        Num_Images =  len(driver.find_element_by_id('altImages').find_elements_by_css_selector('.a-spacing-small.item'))
    except:
        Num_Images = 'NA'
    Title = title
    Price = price
    try:
        Average_Customer_Review = driver.find_element_by_css_selector('.reviewCountTextLinkedHistogram.noUnderline').get_attribute('title')
    except:
        Average_Customer_Review = 'NA'
    Stars_and_numbers = {}
    try:
        Ratings = driver.find_elements_by_css_selector('.a-histogram-row')    
        for rating in Ratings:
            try:
                key = rating.find_elements_by_css_selector('.a-text-right.aok-nowrap')[0].text
                value = rating.find_elements_by_css_selector('.a-text-right.aok-nowrap')[1].text
                Stars_and_numbers[key] = value
            except:
                key = rating.find_elements_by_css_selector('.a-nowrap')[0].text
                value = rating.find_elements_by_css_selector('.a-nowrap')[1].text
                Stars_and_numbers[key] = value
    except:
        pass
        
    Product_Link = url
    product_0 = amazon.lookup(ItemId=unidecode(asin))
    try:
        Description = driver.find_element_by_id('productDescription').text
    except:
        try:
            Description = product_0.editorial_review
        except:
            Description = 'NA'
    features = ['NA']*7
    try:
        features = driver.find_element_by_id('feature-bullets').find_elements_by_tag_name('li')
    except:
        features = ['NA']*7
    try:
        Feature1 = features[1].text
    except:
        Feature1 = features[1]
    try:
        Feature2 = features[2].text
    except:
        Feature2 = features[2]
    try:
        Feature3 = features[3].text
    except:
        Feature3 = features[3]
    try:
        Feature4 = features[4].text
    except:
        Feature4 = features[4]
    try:
        Feature5 = features[5].text
    except:
        Feature5 = features[5]
    try:
        brand = product_0.brand
    except:
        brand = 'NA'

    try:
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
    except:
        Main_Cat = 'NA'
        Category_Tree = 'NA'
    ##product_1 = amazon1.lookup(ItemId=asin)
    ##product_2 = amazon2.lookup(ItemId=asin)
    try:
        Dimensions = {}
    except:
        try:
            Dimensions = product_0.get_attributes(['ItemDimensions.Width', 'ItemDimensions.Height', 'ItemDimensions.Length', 'ItemDimensions.Weight'])
        except:
            Dimensions = 'NA'
    #product_3 = amazon3.lookup(ItemId=asin)
    try:
        Shipping_Weight = float(product_0.get_attribute('PackageDimensions.Weight'))/100.00
    except:
        Shipping_Weight = 'NA'
    ASIN = asin
    #product_4 = amazon3.lookup(ItemId=asin)

    try:
        Sold_and_shipped_by = driver.find_element_by_id('merchant-info').text.replace('\n','').strip()
    except:
        Sold_and_shipped_by = 'NA'
    Amazon_Best_Seller_Rank = salesRank
    try:
        Num_of_reviews = driver.find_element_by_id('acrCustomerReviewText').text
    except:
        Num_of_reviews = 'NA'
    try:
        Item_Model_Number = product_0.mpn
    except:
        Item_Model_Number = 'NA'
    driver.close()

    queue.put(data)

def main(products):
    queue_list = []
    numProducts = len(products.keys())
    for i in range(numProducts):
        queue_list.append(Queue.Queue())

    threads= []
    
    for i in products.keys():
        threads.append(Thread(target = getSKUData, args=(products[i], queue_list[products.keys().index(i)])))
     
    for t in threads[:4]:
        t.start()
        time.sleep(2)
    for t in threads[:4]:
        t.join()
    for t in threads[4:8]:
        t.start()
        time.sleep(2)
    for t in threads[4:8]:
        t.join()
    for t in threads[8:12]:
        t.start()
        time.sleep(2)
    for t in threads[8:12]:
        t.join()
    for t in threads[12:16]:
        t.start()
        time.sleep(2)
    for t in threads[12:16]:
        t.join()

    queue_data = []
    for q in queue_list:
        queue_data.append(q.get())
        
    return queue_data

searchterm = 'dog mat'
products = getAmazonProducts(searchterm)
print len(products.keys())
data = main(products)
print len(data), data[0]
##prod = {}
##prod['asin'] = 'B00267T9LG'
##prod['image'] = 'http://ecx.images-amazon.com/images/I/61sgsDW2hbL._SX425_.jpg'
##prod['title'] = 'Motegi Racing MR107 Gloss Black Wheel With Machined Face (17x7.5"/5x114.3mm, +45mm offset)'
##prod['price'] = '115.89'
##getSKUData(prod, Queue.Queue())

  

