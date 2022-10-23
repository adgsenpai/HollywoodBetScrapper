from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

broswer = webdriver.Chrome(
    executable_path='./chromedriver_win32/chromedriver.exe')

broswer.get('https://m.hollywoodbets.net/Menu/Betting/TodaySportCoupon.aspx?sn=Soccer&s=1&bti=15')

# get the table ctl00_MainContent_popularCouponTable
table = broswer.find_element(By.ID, 'ctl00_MainContent_couponTable')

# get the rows markets-row
rows = table.find_elements(By.CLASS_NAME, 'markets-row')

buffer = []

for row in rows:
    buffer.append(row.text)

for item in buffer:
    print(item)