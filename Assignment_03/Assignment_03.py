from selenium import webdriver
from selenium.webdriver.support.select import Select
import random
import time
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
import random
import time

driver = webdriver.Firefox(executable_path=r'C:\Users\anees\geckodriver.exe')
html=driver.get('https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM')


start_time = time.time()
normal_delay = random.normalvariate(2, 0.5)
time.sleep(normal_delay)
print("--- %.5f seconds ---" % (time.time() - start_time))

def delay(t):
    normal_delay = random.normalvariate(t, 0.5)
    time.sleep(normal_delay)

    delay(3)
html="https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM"
soup = bs4.BeautifulSoup(requests.get(html).text, 'lxml')
big_box = soup.find('div', attrs={'class': 'a-expander-content a-expander-partial-collapse-content'})
print (big_box.prettify())

