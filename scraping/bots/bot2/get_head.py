import scraping_class
import requests
import random
import tqdm
import pandas as pd
import time
import numpy as np
import datetime
import pytest
from connector import Connector
logfile = 'log.csv'## name your log file. 
connector = scraping_class.Connector(logfile)

from multiprocessing import Queue, cpu_count
from threading import Thread
from numpy.random import randint
import logging

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

# start chrome driver
dirname = os.getcwd()
path = os.path.join(dirname, 'chromedriver')
driver = webdriver.Chrome(executable_path=path)

'''
Scrape headlines, number of comments, and time.
'''
def get_head(url_list):
    #i = 0
    list1 = []
    for url in url_list:

        # log and header
        headers = {'email': 'smg158@alumni.ku.dk', 'name': 'Jonathan Isaksen', 'message': 'Students from university of Copenhagen - doing a project on machine learning'}
        connector = Connector('log_get_head.csv')
        # to save log not used by selenium
        response,call_id = connector.get(url, 'urls_get')
        # sending headers, as we don't think connectors can send headers.
        requests.get(url, headers=headers)


        
        no_comments = False
        data_list = []
        #i +=1
        #if i%100 == 0:
        #    print(f'{i} out of {len(url_list)}')
        #if i == n: # break after n articles
        #    break

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

        # get subtitle
        while True:
            try:
                subtitle = url_soup.find_all(class_='art-subtitle') 
                data_list.append(subtitle[0].text)
                break
            except:
                data_list.append(np.nan)
                break
        
        # get body text
        while True:
            try:
                bread = url_soup.find_all(class_='article-bodytext') # div with the comment link
                bread = re.sub(r'\n','',bread[0].text)
                bread = re.sub(r'      .*$','',bread)
                data_list.append(bread)
                break
            except:
                data_list.append(np.nan)
                break
                
        # get date
        while True:
            try:
                date = url_soup.find(class_='eb-row article-timestamp').get_text()
                date=re.findall("\d{1,2}. \w+. \d{4}",date)
                data_list.append(date[0])
                break
            except:
                data_list.append(np.nan)
                break

        # save to list of lists
        list1.append(data_list)
    return list1