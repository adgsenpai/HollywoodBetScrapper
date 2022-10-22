from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

broswer = webdriver.Chrome(
    executable_path='./chromedriver_win32/chromedriver.exe')

broswer.get('https://adgstudios.co.za/')