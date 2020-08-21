from selenium import webdriver
import get_head as gh
from selenium.webdriver.chrome.options import Options
from  multiprocessing import Process
import multiprocessing
import numpy as np
import pandas as pd
import sys
import os
#import time


url0 = pd.read_csv(r"C:\Users\Jonat\Documents\Polit\isds\Isds47\Ex\scraping\bots\chunk0.csv")
url1 = pd.read_csv(r"C:\Users\Jonat\Documents\Polit\isds\Isds47\Ex\scraping\bots\chunk1.csv")
url2 = pd.read_csv(r"C:\Users\Jonat\Documents\Polit\isds\Isds47\Ex\scraping\bots\chunk2.csv")
url3 = pd.read_csv(r"C:\Users\Jonat\Documents\Polit\isds\Isds47\Ex\scraping\bots\chunk3.csv")

urls = []
urls.append(list(url0['0']))
urls.append(list(url1['0']))
urls.append(list(url2['0']))
urls.append(list(url3['0']))

processes = []
if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    for i, urls in enumerate(urls):
        p = Process(target=gh.get_head, args=(urls,1000000,i,return_dict))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    chunk0_head = pd.DataFrame(data=return_dict.values()[0])
    chunk0_head.to_csv("chunk0_head.csv", index=False)
    chunk2_head = pd.DataFrame(data=return_dict.values()[2])
    chunk2_head.to_csv("chunk2_head.csv", index=False)
    chunk3_head = pd.DataFrame(data=return_dict.values()[3])
    chunk3_head.to_csv("chunk3_head.csv", index=False)
    chunk1_head = pd.DataFrame(data=return_dict.values()[1])
    chunk1_head.to_csv("chunk1_head.csv", index=False)