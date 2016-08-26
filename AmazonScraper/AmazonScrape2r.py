# -*- coding: utf-8 -*-
import sys
# reload(sys)
# sys.setdefaultencoding('UTF8')
import os
from bs4 import BeautifulSoup as bs
from BeautifulSoup import BeautifulSoup as bs
from text_unidecode import unidecode

import re
import csv
import requests
import urlparse
import random
import time


url = 'http://www.amazon.com'
filename = "reviews_allinfo50.csv"
filename2 = "reviews_notext50.csv"
filename3 = '{}_notfound.csv'
auth = requests.auth.HTTPProxyAuth('manutd0707', 'vbym5o5r80uvaer')
proxies = {'http': 'http://us-fl.proxymesh.com:31280'}
save_path = 'output50/'
user_agents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.85 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.7.01001)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.5.01003)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8',
    'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0']
resp = requests.get('http://icanhazip.com', proxies=proxies, auth=auth)
print "My new IP address via ProxyMesh:", resp.content.strip()


def connect(url):
    pages = ''
    while True:
        pages = requests.get(
            url, proxies=proxies, auth=auth, headers={
                'User-Agent': random.choice(user_agents), 'referer': 'http://www.amazon.com/'})
        try:
            soup = bs(pages.text)
            captcha_title = soup.title.text
            if captcha_title is 'Robot Check' or captcha_title is '500 Service Unavailable Error' or captcha_title is '503 - Service Unavailable Error':
                time.sleep(random.randint(2, 4))
                pass
            else:
                break
        except:
            pass
    return soup


def review(number):
    start_url = 'http://www.amazon.com/product-reviews/{}/ref=cm_cr_arp_d_viewopt_srt?sortBy=helpful&pageNumber=1'.format(
        number)
    time.sleep(random.randint(1, 3))
    soup = connect(start_url)
    captcha_title = ''
    try:
        captcha_title = soup.title.text
    except:
        pass
    if 'Robot Check' in captcha_title:
        print captcha_title, '11'
    while captcha_title is 'Robot Check' or captcha_title is '500 Service Unavailable Error' or captcha_title is '503 - Service Unavailable Error':
        resp = requests.get('http://icanhazip.com', proxies=proxies, auth=auth)
        time.sleep(random.randint(1, 4))
        soup = connect(start_url)
        captcha_title = ''
        try:
            captcha_title = soup.title.text
        except:
            pass
    looking_for_something = ''
    try:
        looking_for_something = soup.find('b', 'h1').text
    except:
        pass
    if 'Looking for something' in looking_for_something:
        with open(filename3.format(number), "a") as myfile3:
            myfile3.write("%s_notfound".format(number))
    next_button = None
    
    number_total_reviews = ''
    try:
        number_total_reviews = soup.find(
            'span', 'a-size-medium a-text-beside-button totalReviewCount').text.strip().replace(',','')
    except:
        pass
    print 'number_total_reviews', number_total_reviews
    helpfulness_rank = 0
    pageNumber = 1
    while True:
        if pageNumber ==50:
            break
        time.sleep(random.randint(1, 3))
        soup = connect(start_url)
        if 'Sorry, no reviews match your current selections'.lower() in str(soup).lower():
            break
        sections = ''
        try:
            sections = soup.findAll('div', 'a-section review')
            print len(sections), 'len of sections'
        except Exception as e:
            pass
            print str(e)
        if not sections:
            continue
        else:
            for section in sections:
                helpfulness_rank += 1
                title = section.find(
                    'a',
                    'a-size-base a-link-normal review-title a-color-base a-text-bold').text.strip()
                rev_link = section.find(
                    'a', 'a-size-base a-link-normal review-title a-color-base a-text-bold')['href']
                print 'rev_link', rev_link
                date = ''
                try:
                    date = section.find(
                        'span', 'a-size-base a-color-secondary review-date').text.replace('on', '').strip()
                except:
                    pass
                review_existing = ''
                try:
                    review_existing = section.find(
                        'span', 'a-size-small a-color-secondary review-votes')
                except:
                    pass
                review_id = ''
                try:
                    review_id = rev_link.split(
                        'customer-reviews/')[-1].split('/')[0]
                except:
                    pass
                print 'review_id', review_id
                text = ''
                try:
                    text = section.find(
                        'span', 'a-size-base review-text').text.strip()
                except:
                    pass
                review_link = urlparse.urljoin(url, rev_link)
                time.sleep(random.randint(1, 3))
                review_soup = connect(review_link)
                captcha_title = ''
                try:
                    captcha_title = soup.title.text
                except:
                    pass
                if 'Robot Check' in captcha_title:
                    print captcha_title, '22'
                while captcha_title is 'Robot Check' or captcha_title is '500 Service Unavailable Error' or captcha_title is '503 - Service Unavailable Error':
                    time.sleep(random.randint(1, 4))
                    review_soup = connect(start_url)
                    captcha_title = ''
                    try:
                        captcha_title = soup.title.text
                    except:
                        pass
                if review_existing:
                    helpfulness_text = ''
                    try:
                        helpfulness_text = review_soup.find('table').find(
                            'td', attrs={'valign': 'top'}).find('div').find('div').text.replace(',','')
                    except:
                        pass
                    print 'helpfulness_text', helpfulness_text
                    pat = re.compile('\d+')
                    helpfulness_votes_total = ''
                    try:
                        helpfulness_votes_total = helpfulness_text.split(
                            'of')[-1]
                    except:
                        pass
                    print 'helpfulness_votes_total', helpfulness_votes_total
                    if pat.search(helpfulness_votes_total):
                        helpfulness_votes_total = pat.search(
                            helpfulness_votes_total).group()
                    helpfulness_votes = ''
                    try:
                        helpfulness_votes = helpfulness_text.split('of')[
                            0].strip()
                    except:
                        pass
                    print 'helpfulness_votes', helpfulness_votes
                else:
                    helpfulness_votes_total = ''
                    helpfulness_votes = ''
                rating = ''
                try:
                    rating = review_soup.find('table').find('span').find('img')[
                        'title'].split('out of')[0].strip()
                except:
                    pass
                user_id = ''
                try:
                    user_id = section.find('div', 'a-row').findNext('div', 'a-row').a[
                        'href'].split('profile/')[-1].split('/')[0].strip()
                except:
                    pass
                if not user_id:
                    user_id = 'none_{}'.format(helpfulness_rank)
                if user_id:
                    name_of_file = "%s_%s.txt" % (number, user_id)
                    if not os.path.exists(os.path.dirname(save_path)):
                        os.makedirs(os.path.dirname(save_path))
                    completeName = os.path.join(save_path, name_of_file)

                    file3 = open(completeName, "a")
                    file3.write(unidecode(text))

                if helpfulness_votes == '' or helpfulness_votes_total == '' or helpfulness_rank == '':
                    continue

                with open(filename, "a") as myfile:
                    myfile.write("%s|" % (number))
                    myfile.write("%s|" % (user_id))
                    myfile.write("%s|" % (review_id))
                    myfile.write("%s|" % (date))
                    myfile.write("%s|" % (rating))
                    myfile.write("%s|" % (helpfulness_votes))
                    myfile.write("%s|" % (helpfulness_votes_total))
                    myfile.write("%s|" % (helpfulness_rank))
                    myfile.write("%s|" % (number_total_reviews))
                    myfile.write("'%s'\n" % unidecode(text.replace(',', ';')))
                
                print number, "||", user_id, "||", review_id, "||", date, "||",\
                      rating, "||", helpfulness_votes, "||", \
                      helpfulness_votes_total, "||", helpfulness_rank, "||", \
                      number_total_reviews
                
                with open(filename2, "a") as myfile2:
                    myfile2.write("%s|" % (number))
                    myfile2.write("%s|" % (user_id))
                    myfile2.write("%s|" % (review_id))
                    myfile2.write("%s|" % (date))
                    myfile2.write("%s|" % (rating))
                    myfile2.write("%s|" % (helpfulness_votes))
                    myfile2.write("%s|" % (helpfulness_votes_total))
                    myfile2.write("%s|" % (helpfulness_rank))
                    myfile2.write('"%s"\n' % (number_total_reviews))

            pageNumber += 1
            start_url = start_url.replace(
                'pageNumber=' + str(pageNumber - 1), 'pageNumber=' + str(pageNumber))
            


def run():
    with open('product_ids.csv', 'rb') as f:
        csv_f = csv.reader(f)
        items = [row[0].strip() for row in csv_f]
        for item in items:
            print item
            review(item)
            break


run()
