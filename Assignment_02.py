from bs4 import BeautifulSoup
import urllib.request
import requests
from pandas.io.sas.sas7bdat import _column
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
import random
import time
import pandas as pd


def extract_table_data(html, get_player_url=False):
    soup = BeautifulSoup(data_html, 'html5lib')

    # get the column names from thead
    column_names = []
    for th in soup.thead.findAll('th'):
        column_names.append(th.abbr.text if th.abbr else th.text)

    # get the data from tbody
    list_of_rows = []
    list_of_urls = []
    for tr in soup.tbody.findAll('tr'):
        row = []
        for td in tr.findAll('td'):
            # if get_player_url and 'dg-name_display_last_init' in td['class']:
            #     list_of_urls.append(td.a['href'])
            row.append(td.text)

        list_of_rows.append(row)

    df = pd.DataFrame(data=list_of_rows, columns=column_names)

    if get_player_url:
        df['player_url'] = list_of_urls

    for col in ['HR', 'AVG', 'AB']:
        df[col] = pd.to_numeric(df[col])

    return df


def reset_driver():
    driver = webdriver.Firefox(executable_path=r'C:\Users\anees\geckodriver.exe')
    driver.get('http://mlb.mlb.com/stats/')
    return driver


def random_delay():
    time.sleep(random.uniform(0.5, 3))


def Reg_Season():
    select_season = Select(driver.find_element_by_class_name('game_type_select'))
    select_season.select_by_visible_text('Regular Season')
    time.sleep(random.normalvariate(3, 0.5))


# def initialize():
# sauce = urllib.request.urlopen('http://www.mlb.com/stats').read()


driver = webdriver.Firefox(executable_path=r'C:\Users\anees\geckodriver.exe')
driver.get('http://www.mlb.com/stats')
select_year = Select(driver.find_element_by_class_name('season_select'))
select_year.select_by_visible_text('2015')
time.sleep(random.normalvariate(3, 0.5))
Reg_Season()

# select_season = Select(driver.find_element_by_class_name('game_type_select'))
# select_season.select_by_visible_text('Regular Season')
# time.sleep(random.normalvariate(3, 0.5))
Team = (driver.find_element_by_css_selector('#st_parent')).click()
time.sleep(random.normalvariate(3, 0.5))
HR = (driver.find_element_by_css_selector('th.dg-hr > abbr:nth-child(1)')).click()
data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
df = extract_table_data(data_html)

# Q1 Team Name with most HRs
print('The highest home run Scoring team is')
print(df.sort_values('HR', ascending=False).iloc[0]['Team'])
df.to_csv('Question_1.csv')

# Q2 Which league (AL or NL) had the greatest average number of homeruns…
# Q2 a: in the regular season of 2015? Please give the league name and the average number of homeruns
# average number of HRs for AL
AL_mean = df[df.League == 'AL']['HR'].mean()
NL_mean = df[df.League == 'NL']['HR'].mean()

if AL_mean > NL_mean:
    print('AL: ', AL_mean)
else:
    print('NL: ', NL_mean)
driver.close()

# Q2 b: in the regular season of 2015 in the first inning? Please give the league name and the average number of homeruns.
driver = reset_driver()
random_delay()
select_year = Select(driver.find_element_by_class_name('season_select'))
select_year.select_by_visible_text('2015')
random_delay()
Reg_Season()
# select_season = Select(driver.find_element_by_class_name('game_type_select'))
# select_season.select_by_visible_text('Regular Season')
random_delay()
# select_inning = Select(driver.find_element_by_id('#st_hitting_hitting_splits')).click()
# select_inning.select_by_visible_text('First Inning')# select_innings=Select(driver.find_element_by_css_selector('#sp_hitting_hitting_splits > optgroup:nth-child(13)')
# options = [option.get_attribute("innerText") for option in driver.find_elements_by_css_selector("#sp_hitting_hitting_splits > optgroup:nth-child(13) > option:nth-child(1)")[1:]]
# print(options)


random_delay()
driver.close()
# Al_leg=(driver.find_element_by_css_selector('#st_parent')).click()

# df[df['Team'].isin(['Toronto Blue Jays', 'New York Yankees'])]


# Q3. What is the name of the player with the best overall batting average in the 2017 regular season that played for the New York Yankees, who
#     a) had at least 30 at bats? Please give his full name and position.
#     b) played in the outfield (RF, CF, LF)? Please give his full name and position.
driver = reset_driver()
select_year = Select(driver.find_element_by_class_name('season_select'))
select_year.select_by_visible_text('2017')
time.sleep(random.normalvariate(3,0.5))
select_navbar_class = driver.find_element_by_id('top_nav')
nav_bar = select_navbar_class.find_elements_by_tag_name('li')
nav_bar[4].click()
time.sleep(random.normalvariate(2,0.5))
driver.find_element_by_css_selector('tr.odd:nth-child(12) > td:nth-child(2) > a:nth-child(1)').click()
random_delay()
Reg_Season()
data_div = driver.find_element_by_id('datagrid')
data_html = data_div.get_attribute('innerHTML')
df1=extract_table_data(data_html)
1+1
# df_player_ny_yank = read_data_stats(driver)
#
#
#     df_accepted = df_player_ny_yank[bats_ov_30]
#     df_accepted_sorted = df_accepted.sort_values('AVG',ascending=False)
#     df_accepted_sorted.to_csv('Question_3a.csv')
#
#     max_avg_player = df_accepted_sorted['Player'].iloc[0]
#     max_avg_player_pos = df_accepted_sorted['Pos'].iloc[0]
#
#     driver.find_element_by_link_text(max_avg_player).click()
#     max_avg_full_name = driver.find_element_by_css_selector('.player-name').text
#     print('The player with the highest average having bats more than 30 is {} and the position he plays is {}'.format(max_avg_full_name,max_avg_player_pos))
#     random_delay()
#     driver.back()
#     random_delay()
#     reset_list()
#     positions = ['RF','CF','LF']
#
#     df_accepted_pos = df_player_ny_yank[df_player_ny_yank['Pos'].isin(positions)]
#     df_accepted_avg = pd.to_numeric(df_accepted_pos['AVG'])
#
#     df_player_avg = pd.concat([df_accepted_pos['Player'],df_accepted_avg], axis=1)
#     df_player_pos = pd.concat([df_accepted_pos['Player'],df_accepted_pos['Pos']],axis=1)
#
#     df_player_avg_pos = pd.merge(df_player_avg,df_player_pos,on='Player')
#     df_accepted_pos_sorted = df_player_avg_pos.sort_values('AVG', ascending=False)
#
#     df_player_avg_pos.to_csv('Question_3b.csv')
#
#     max_outfield_player = df_accepted_pos_sorted['Player'].iloc[0]
#     max_outfield_player_pos = df_accepted_pos_sorted['Pos'].iloc[0]
#
#     driver.find_element_by_link_text(max_outfield_player).click()
#     max_avg_out_name = driver.find_element_by_css_selector('.full-name').text
#
#     print('The outfield player who has the highest average is {} and plays in {} postion'.format(max_avg_out_name,max_outfield_player_pos))
#
#     driver.close()
# get the row in
df.iloc[0]

normal_delay = random.normalvariate(4, 0.5)
print('Sleeping for {} seconds'.format(normal_delay))
# with open() as fp:
#     soup = BeautifulSoup(fp)
#
# soup = BeautifulSoup('<b class="dg-team_full">')
# team_name= soup.find('div', attrs='views-field-title')
#
# tag = soup.b
# type(tag)


# print(team_name)
# print(HR)


'''

stats_header_bar.click()

stats_line_items = stats_header_bar.find_elements_by_tag_name('li')
# Why would we need to wait when running this script? Try copying the above code and running at once.


print('The stats dropdown in the header was loaded successfully. The mouse will move over the element after a short delay')
normal_delay = random.normalvariate(2, 0.5)
print('Sleeping for {} seconds'.format(normal_delay))
time.sleep(normal_delay)
print('Now moving mouse...')
ActionChains(driver).move_to_element(stats_header_bar).perform()
reg_season_stats_2017 = select_element_by_text(stats_line_items, '2017 Regular Season Stats')
ActionChains(driver).move_to_element(reg_season_stats_2017).click().perform()
# Use delays wisely to look more human. Check out the other distributions that you have available to use.
'''
