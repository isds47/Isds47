import scraping_class
import requests
import random
import tqdm
import pandas as pd
import time
import numpy as np
logfile = 'log.csv'## name your log file.
connector = scraping_class.Connector(logfile)

# similarity/distance measures
from scipy.spatial import distance
from sklearn.metrics.pairwise import linear_kernel

# for vectorization 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from selenium import webdriver
import re
import os
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

dirname = "C:\Users\Jonat\Documents\Polit\isds\Isds47\Ex\scraping"
path = os.path.join(dirname, 'chromedriver')
driver = webdriver.Chrome(executable_path=path)

# load urls
urls = pd.read_csv("urls.csv")

# remove plus articles
urls_no_plus = [ url for url in urls['0'] if "https://ekstrabladet.dk/plus" not in url ]

'''
Scrape headlines, number of comments, and time.
'''
def get_head(list, n):
    for url in urls_no_plus:
        global i
        no_comments = False
        data_list = []
        i +=1
        if i%100 == 0:
            print(f'{i} out of {len(urls_no_plus)}')
        if i == n: # break after n articles
            break

        data_list.append(url) # save url to df
        driver.get(url) # open the current url
        time.sleep(0.5)
        url_soup = BeautifulSoup(driver.page_source, 'lxml') # save soup


        # get ammount of comments
        while True:
            try:
                comments = url_soup.find_all(id='fnTalkCommentText') # div with the comment link
                comments = re.findall('\d+',comments[0].text)
                data_list.append(int(comments[0]))
                break
            except:
                data_list.append(np.nan)
                no_comments = True
                break

        # skips url if no comments
        if no_comments: 
            continue


        # get headline
        while True:
            try:
                headline = url_soup.find_all(class_='art-title') # div with the comment link
                headline = re.sub('\\n {16}','',headline[0].text)
                data_list.append(headline)
                break
            except:
                data_list.append(np.nan)
                break

        # get date
        while True:
            try:
                date = url_soup.find(class_='eb-row article-timestamp').get_text()
                date=re.findall("\d{2}. \w+. \d{4}",date)
                data_list.append(date[0])
                break
            except:
                data_list.append(np.nan)
                break

        # save to list of lists
        list1.append(data_list)
    return list1


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

chunks = list(chunks(urls_no_plus, 2000))

from multiprocessing import Process
import sys

list1 = []
i = 0
n = 10 # number of articles to run through


def func0():
    print('start chunk0')
    list0 = get_head(chunks[0])

def func1():
    print('start chunk1')
    list1 = get_head(chunks[1])

if __name__=='__main__':
    p0 = Process(target = func0)
    p0.start()
    p1 = Process(target = func1)
    p1.start()

