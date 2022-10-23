import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

broswer = webdriver.Chrome(
    executable_path='./chromedriver_win32/chromedriver.exe')

broswer.get(
    'https://m.hollywoodbets.net/Menu/Betting/TodaySportCoupon.aspx?sn=Soccer&s=1&bti=15')

# get the table ctl00_MainContent_popularCouponTable
table = broswer.find_element(By.ID, 'ctl00_MainContent_couponTable')

# get the rows markets-row
rows = table.find_elements(By.CLASS_NAME, 'markets-row')

buffer = []

for row in rows:
    buffer.append(row.text)

broswer.get(
    'https://m.hollywoodbets.net/Menu/Betting/TodaySportCoupon.aspx?sn=Soccer&s=1&bti=15')

# get the table ctl00_MainContent_popularCouponTable
table = broswer.find_element(By.ID, 'ctl00_MainContent_popularCouponTable')

# get the rows markets-row
rows = table.find_elements(By.CLASS_NAME, 'markets-row')

for row in rows:
    buffer.append(row.text)

broswer.close()
matches = []

for item in buffer:
    matches.append(item.split('\n'))

# dataframe with columns m1 o1 draw o2 m3 o3
df = pd.DataFrame(matches, columns=['t1', 'o1', 'draw', 'o2', 't2', 'o3'])
# remove draw column
df = df.drop(columns=['draw'])



df['o1'] = df['o1'].astype(float)+1
df['o2'] = df['o2'].astype(float)+1
df['o3'] = df['o3'].astype(float)+1



for index, row in df.iterrows():
    # get the odds
    o1 = float(row['o1'])
    o2 = float(row['o2'])
    o3 = float(row['o3'])
    # calculate the arbitrage
    arb = (1/o1 + 1/o2 + 1/o3)
    # add the arbitrage to the dataframe
    df.loc[index, 'arb'] = arb

# set t1 , t2 uppercase
df['t1'] = df['t1'].str.upper()
df['t2'] = df['t2'].str.upper()


# sort the dataframe by arbitrage
df = df.sort_values(by=['arb'], ascending=True)

# save the dataframe to a excel file
df.to_excel('hollywood.xlsx')
