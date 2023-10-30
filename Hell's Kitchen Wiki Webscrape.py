#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 22:51:04 2023

@author: corinamccullough
"""


import time
import numpy as np
import openpyxl
import pandas as pd
import lxml
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd 
pd.set_option('display.max_columns', None)


# Web scrape one seaon
hk_url = "https://en.wikipedia.org/wiki/Hell%27s_Kitchen_(American_season_1)"
hk = requests.get(url = hk_url).text
soup = BeautifulSoup(hk, 'html.parser')
table = soup.find('table', class_="wikitable sortable")


contestants = pd.read_html(str(table))
contestants  = pd.concat(contestants)
contestants.columns = ["Contestant", "Age", "Occupation", "Hometown","Result"]

# Web scrape mutlple seasons
hk_headers = ["Contestant", "Age", "Occupation", "Hometown","Result"]

hk_cols = ['Season'] + hk_headers

df = pd.DataFrame(columns = hk_cols)

Season = ['1', '2', '3', '4', '5']

# Automatically pull data from each season
for y in Season:
        hk_url = 'https://en.wikipedia.org/wiki/Hell%27s_Kitchen_(American_season_'+y+')'
        hk = requests.get(url = hk_url).text
        soup = BeautifulSoup(hk, 'html.parser')
        table = soup.find('table', class_="wikitable sortable")
        contestants = pd.read_html(str(table))
        contestants  = pd.concat(contestants)
        contestants.set_axis(["Contestant", "Age", "Occupation", "Hometown","Result"], axis="columns", inplace=True)
        temp_df1 = pd.DataFrame({'Season':[y for i in range(len(contestants))]})
        temp_df2 = pd.concat([temp_df1, contestants], axis = 1)
        df = pd.concat([df, temp_df2], axis = 0)
        print(f"Finished scraping for Hell's Kitchen Season {y}")
        lag = np.random.uniform(5,10) # every 5 to 10 seconds
        time.sleep(lag) 
print(f'Task Completed.')

# Save to Excel
df.to_excel('Hells_Kitchen_data.xlsx', index = False)
