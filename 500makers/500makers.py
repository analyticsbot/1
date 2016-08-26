from selenium import webdriver
import re, time
import pandas as pd

df = pd.DataFrame(columns = ['id', 'Name of Maker' , 'Product Hunt profile url' , 'Twitter handle' , 'Most upvoted Product' , 'How many votes'])

url = 'http://500makers.com/'

driver = webdriver.Firefox()
driver.get(url)

makers = driver.find_elements_by_class_name('maker')

#Name of Maker | Product Hunt profile url | Twitter handle | Most upvoted Product | How many votes

urls = []

for maker in makers:
    url = maker.get_attribute('href')
    urls.append(url)
    #twitter_id = re.findall(r'@\w+', url)[0]

count = 0
for url in urls:
    driver.get(url)
    time.sleep(5)
    name = driver.find_element_by_css_selector('.page-header--title').find_element_by_tag_name('span').text
    id = driver.find_element_by_css_selector('.page-header--id').text
    url = url
    twitter = driver.find_element_by_css_selector('.page-header--username').text
    most_upvoted_product = driver.find_element_by_css_selector('.name_1U6M1.featured_2W7jd.default_tBeAo.base_3CbW2').text
    upvote_count = driver.find_element_by_css_selector('.post-vote-button--count').text
    df.loc[count] =[id, name, url, twitter, most_upvoted_product,upvote_count ]
    count +=1
    time.sleep(5)
    
