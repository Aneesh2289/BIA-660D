from selenium import webdriver
from selenium.webdriver.support.select import Select
import random
import time
import pandas as pd

def extract_review(html, get_player_url=False):
    soup = BeautifulSoup(data_html, 'lxml')


driver = webdriver.Firefox(executable_path=r'C:\Users\anees\geckodriver.exe')
driver.get('https://www.amazon.com/RockBirds-Flashlights-Bright-Aluminum-Flashlight/product-reviews/B00X61AJYM')