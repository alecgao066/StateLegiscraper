import os
import requests
import re
import time
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager

def nv_scrape(webscrape_links, dir_chrome_webdriver, dir_save_folder):

    """ 
    Webscrape function for Nevada State Legislature Website 
    - webscrape_links: [List] of direct link(s) to NV committee webpage, 
        see nv_weblinks.py for lists organized by chamber and committee 
    - dir_chrome_webdriver: [String] Local directory that has Chrome Webdriver
    - dir_save_folder: [String] Local directory to save pdfs (need to figure out file management)
    
    """
    for link_index in range(len(webscrape_links)):
        driver=webdriver.Chrome(dir_chrome_webdriver)
        time.sleep(5)
        driver.get(webscrape_links[link_index]) 
        time.sleep(5)
        
        arrow01 = driver.find_element_by_id('divCommitteePageMeetings')
        arrow01.click()
        time.sleep(5)
    
        arrow02 = driver.find_element_by_id('divMeetings')
        arrow02.click()

        url = driver.page_source
        REGEX_PATTERN = r'https.*Minutes.*\.pdf'
        lines = url.split()
        meeting_regex = re.compile(REGEX_PATTERN)
        all_files = []
        
        for l in lines:
            hit = meeting_regex.findall(l)
            if hit:
                all_files.extend(hit)
                
        for filename in all_files:
            print(filename)
    
        folder_location = dir_save_folder

        for link in all_files:
            filename = os.path.join(folder_location,"_".join(link.split('/')[4:]))
            urllib.request.urlretrieve(link, filename)
        time.sleep(30)
        
        driver.close()
        

""" UNIT TEST

K NOTES (11/8): 
    Need to check Chrome version and download the right Chromedriver. 
    Need to print chrome version and direct people to find the right driver
    https://chromedriver.chromium.org/downloads
    I'm running Chrome Version 95 
    
    Func runs and works, I'm gettting depreciation warnings. Look into updating the functions 
    
    v_scrape(ed_test, chrome_webdriver, save_folder)
/var/folders/vp/kyx63ql12dggnl_3zsdqpsh80000gn/T/ipykernel_4733/575717094.py:11: 
    DeprecationWarning: executable_path has been deprecated, please pass in a Service object
  driver=webdriver.Chrome(dir_chrome_webdriver)
/var/folders/vp/kyx63ql12dggnl_3zsdqpsh80000gn/T/ipykernel_4733/575717094.py:16: 
    DeprecationWarning: find_element_by_* commands are deprecated. Please use find_element() instead
  arrow01 = driver.find_element_by_id('divCommitteePageMeetings')
/var/folders/vp/kyx63ql12dggnl_3zsdqpsh80000gn/T/ipykernel_4733/575717094.py:20: 
    DeprecationWarning: find_element_by_* commands are deprecated. Please use find_element() instead
  arrow02 = driver.find_element_by_id('divMeetings')

"""

ed_test=["https://www.leg.state.nv.us/App/NELIS/REL/81st2021/Committee/342/Meetings"]
chrome_webdriver="/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/chromedriver"
save_folder="/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/toy"

nv_scrape(ed_test, chrome_webdriver, save_folder)

#Next steps: Import nv_weblinks.py and test with one of the available lists