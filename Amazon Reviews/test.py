import requests
from BeautifulSoup import BeautifulSoup
from dateutil.parser import parse
import pandas as pd
from selenium import webdriver

product = 'air purifier'
lowPrice=200
highPrice=300
maxPages = 2
maxReviewPages = 2
asins = []
driver = webdriver.Firefox()

## get all asins
for page in range(1, maxPages):
    url = 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=' + \
      '+'.join(product.split()) + '&low-price=' + str(lowPrice) + '&high-price='+ str(highPrice) +'&page='+str(page)

##    resp = requests.get(url)
##    soup = BeautifulSoup(resp.content)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)
    products = soup.findAll(attrs = {'class':'s-result-item celwidget'})
    print len(products)
    
    for product in products:
        asins.append(product['data-asin'])

## go to the review urls and scrape reviews
df2 = pd.DataFrame()
c=0
for asin in asins:
    df = pd.DataFrame(columns = ['Date', 'Review_Text'])
    df1 = pd.DataFrame(columns = [asin, asin])
    date_dict = {}
    for i in range(1, maxReviewPages):        
        review_url = 'https://www.amazon.com/portal/customer-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_{pgNum}?pageNumber={pgNum}'.replace('{asin}', asin).replace('{pgNum}', str(i))
##        rr = requests.get(review_url)
##        soup2 = BeautifulSoup(rr.content)
        driver.get(review_url)
        soup2 = BeautifulSoup(driver.page_source)
        reviews = soup2.findAll(attrs = {'class':'a-section review'})
        print ';;;', len(reviews)

        ## check if there are reviews on this page
        if len(reviews)>0:
            pass
        else:
            break       
        
        for review in reviews:
            date = str(parse(review.find(attrs = {'class':'a-size-base a-color-secondary review-date'}).getText()))
            review_text = review.find(attrs = {'class':'a-row review-data'}).getText()

            if date not in date_dict.keys():
                date_dict[date] = 1
            else:
                date_dict[date] += 1

            nrow = df.shape[0]

            df.loc[nrow+1] = [date, review_text]

    j=0  
    for key, value  in date_dict.iteritems():
        df1.loc[j] = [key, value]
        j+=1
    df1.columns = [asin, 'count']
    df2 = pd.concat([df2, df1], axis=1)
    df.to_csv('reviews_'+asin+'.csv', index = False, encoding = 'utf-8')
    
    c+=1

df2.to_csv('monthly_review_count'+str(c)+'.csv', index = False, encoding = 'utf-8')
driver.close()
