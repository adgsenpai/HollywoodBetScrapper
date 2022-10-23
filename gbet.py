import time
from tkinter import BROWSE
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
driver = uc.Chrome(use_subprocess=True)

driver.get('https://www.gbets.co.za/sports')

# save html content
time.sleep(15)
html = driver.page_source
driver.close()

import bs4 as bs

soup = bs.BeautifulSoup(html, 'html.parser')

 
accordionCont = soup.find_all('div', class_='sb-accordion-container')

matches = []

for accDOM in accordionCont:
    # find eventListBody
    eventListBody = accDOM.find('div', id='eventListBody')
    if eventListBody == None:
        pass
    else:
        # find event-header -header event-header-layout2
        eventHeaders = eventListBody.find('div', class_='event-header -header event-header-layout2')        
        try:
            match = eventHeaders['title']
            #split by - and make all uppercase
            team = [team.upper() for team in match.split('-')]                
            matches.append(team)
        except:
            pass
 
odds = []
for accDOM in accordionCont:
    # find coeficiente-layout2 sb-game-bet-coeficiente  
    coeficientes = accDOM.find_all('div', class_='coeficiente-layout2 sb-game-bet-coeficiente')
    for i,coeficiente in enumerate(coeficientes):
        odds.append(coeficiente.text.strip())


# for every 3 odds append to matches
currentIndex= 0
for i in range(0, len(odds), 3):
    try:
        matches[currentIndex].append(odds[i])
        matches[currentIndex].append(odds[i+1])
        matches[currentIndex].append(odds[i+2])
        currentIndex += 1
    except:
        pass


# iterate matches and check if len is 5 if greater then print
for i,match in enumerate(matches):
    if len(match) > 5:
        #drop element
        matches[i].pop(0)

import pandas as pd
df = pd.DataFrame(matches, columns=['t1','t2','o1','o2','o3'])
df

# calculate arb
df['o1'] = df['o1'].astype(float)
df['o2'] = df['o2'].astype(float)
df['o3'] = df['o3'].astype(float)

df['arb'] = df.apply(lambda row: 1/row['o1'] + 1/row['o2'] + 1/row['o3'], axis=1)

# sort by arb
df.sort_values(by=['arb'], ascending=True)

# save as excel file
df.to_excel('gbets.xlsx', index=False)