import time
from tkinter import BROWSE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

broswer = webdriver.Chrome(
    executable_path='./chromedriver_win32/chromedriver.exe')

broswer.get('https://www.betway.co.za/sport')
# save html content
html = broswer.page_source
broswer.close()

import bs4 as bs

soup = bs.BeautifulSoup(html, 'html.parser')

rowEventRows = soup.find_all('div', class_='row eventRow')

matches = []

for rowEventRow in rowEventRows:    
    currentMatch = []
    eventTitle = rowEventRow['data-eventtitle']       
    teams = [team.upper() for team in eventTitle.split(' v ')]    

    for team in teams:
        currentMatch.append(team)

    #find outcome-pricedecimal
    outcomePriceDecimals = rowEventRow.find_all('div', class_='outcome-pricedecimal')
    for outcomePriceDecimal in outcomePriceDecimals:
        # remove '\n' from string
        currentMatch.append(outcomePriceDecimal.text.strip())        

    matches.append(currentMatch)



import pandas as pd

# create a dataframe with columns t1,t2,o1,o2,o3
df = pd.DataFrame(matches, columns=['t1','t2','o1','o2','o3'])
df

# iterate row by row add 1/o1,1/o2,1/o3 and create new column arb
# convert to float
df['o1'] = df['o1'].astype(float)
df['o2'] = df['o2'].astype(float)
df['o3'] = df['o3'].astype(float)

df['arb'] = df.apply(lambda row: 1/row['o1'] + 1/row['o2'] + 1/row['o3'], axis=1)

# sort by arb
df.sort_values(by=['arb'], ascending=True)

# remove duplicates
df.drop_duplicates(subset=['t1','t2'], keep='first', inplace=True)
df

# save as xlsx
df.to_excel('betway.xlsx', index=False)