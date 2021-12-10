"""
NV module for scraping and processing text from https://leg.state.nv.us 

# Status

Current Coverage:
    [X] Committee Hearings (PDF Transcript Links) (2011 - 2021)

Planned Coverage:
    [ ] Floor Speeches 

# NV Work Flow
    
StateLegiscraper has two classes for each state module: Scrape and Process

    Scrape includes 1 function that scrapes PDF transcripts present at a list of weblinks
    This class provides user with raw data saved on a local or mounted drive

    Process includes 3 functions that processes raw data (PDF Transcripts)
    generated by NV_Scrape class functions. 
    This class provides useres with Python objects ready to work with popular
    NLP packages (e.g., nltk, SpaCy)

CLASS Scrape

    - nv_scrape_pdf

CLASS Process

    - nv_pdf_to_text
    - nv_text_clean

"""

import json
import os
import re
import requests
import string
import time

from urllib.parse import urljoin
import urllib.request

import pdfplumber
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Scrape:
    """
    Scrape functions for Nevada State Legislature website
    """
    
    def nv_scrape_pdf(webscrape_links, dir_chrome_webdriver, dir_save):
        
        """
        Webscrape function for Nevada State Legislature Website. 
        
        Parameters
        ----------
        webscrape_links : List
            List of direct link(s) to NV committee webpage.
            see nv_weblinks.py for lists organized by chamber and committee
        dir_chrome_webdriver : String
            Local directory that has Chrome Webdriver.
        dir_save : String
            Local directory to save pdfs (need to figure out file management).
    
        Returns
        -------
        All PDF files found on the webscrape_links, saved on local dir_save.
        
        """
        
        for link_index in range(len(webscrape_links)):
            
            service = Service(dir_chrome_webdriver)
            options = webdriver.ChromeOptions()
            options.add_argument('headless') #Chrome runs headless, comment out this line if you'd like to see the action
            driver = webdriver.Chrome(service=service, options=options)
    
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
        
            folder_location = dir_save
    
            for link in all_files:
                filename = os.path.join(folder_location,"_".join(link.split('/')[4:]))
                urllib.request.urlretrieve(link, filename)
            time.sleep(15)
            
            driver.close()
        
        
class Process:
    """
    Process functions for PDF transcripts scraped from Nevada State Legislature website
    """
        
    def nv_pdf_to_text(dir_load, nv_json_name):
        """
        Convert all PDFs to a dictionary and then saved locally as a JSON file.
        
        Parameters
        ----------
        dir_load : String
            Local location of the directory holding PDFs.
        nv_json_name : String
            JSON file name, include full local path.
    
        Returns
        -------
        A single JSON file, can be loaded as dictionary to work with.
    
        """
        directory = dir_load
        n=0
        committee = {} 
        
        file_list = os.listdir(directory)
        file_list.sort()
        del file_list[0]
        
        for file in file_list:
            filename = directory + file
            all_text = '' 
            with pdfplumber.open(filename) as pdf:
                for pdf_page in pdf.pages:
                    single_page_text = pdf_page.extract_text()
                    all_text = all_text + '\n' + single_page_text
                    committee[n]=all_text
            n=n+1   
                                    
        with open(nv_json_name, 'w') as f: 
            json.dump(committee, f, ensure_ascii=False)    
        
    def nv_text_clean(nv_json_path, trim=None):    
        """
        Loads JSON into environment as dictionary
        Preprocesses the raw PDF export from previously generated json    
        Optional: Trims transcript to exclude list of those present and signature page/list of exhibits
        
        Parameters
        ----------
        nv_json_path : String
            Local path of nv_json generated by nv_pdf_to_text.
        trim: TRUE/Default(NONE)
            Provides option to trim transcript to spoken section and transcriber notes
            
        Returns
        -------
        Cleaned dictionary that excludes PDF formatting and (optional) front and back end 
    
        """
        
        file_path = open(nv_json_path,)
        data = json.load(file_path)
        
        if trim:
            for key in data:
                if isinstance(data[key], str):
                    ##Removes list of attendees on front end
                    start_location = re.search(r"(CHAIR.*[A-z]\:|Chair.*[A-z]\:)", data[key]).start() #Chair speaks first
                    data[key] = data[key][start_location:] #Starts transcript from when Chair first speaks
                    ##Removes signature page after submission (RESPECTFULLY SUBMITTED)
                    end_location = re.search(r"(Respectfully\sSUBMITTED\:|RESPECTFULLY\sSUBMITTED\:|RESPECTFULLY\sSUBMITTED)", data[key]).start() #Signature page starts with
                    data[key] = data[key][:end_location] #End transcript just before respectfully submitted            
                    ##PDF formatting
                    data[key] = re.sub(r"Page\s[0-9]{1,}", "", data[key]) #Removes page number
                    data[key] = re.sub(r"\n", "", data[key])
                    data[key] = data[key].strip()
                    data[key]=" ".join(data[key].split())
                elif isinstance(data[key], list):
                    for i in range(len(data[key])):
                        start_location = re.search(r"(CHAIR.*[A-z]\:|Chair.*[A-z]\:)", data[key][i]).start() #Chair speaks first
                        data[key][i] = data[key][i][start_location:] #Starts transcript from when Chair first speaks
                        ##Removes signature page after submission (RESPECTFULLY SUBMITTED)
                        end_location = re.search(r"(Respectfully\sSUBMITTED\:|RESPECTFULLY\sSUBMITTED\:|RESPECTFULLY\sSUBMITTED)", data[key][i]).start() #Signature page starts with
                        data[key][i] = data[key][i][:end_location] #End transcript just before respectfully submitted            
                        ##PDF formatting
                        data[key][i] = re.sub(r"Page\s[0-9]{1,}", "", data[key][i]) #Removes page number
                        data[key][i] = re.sub(r"\n", "", data[key][i])
                        data[key][i] = data[key][i].strip()
                        data[key][i]=" ".join(data[key][i].split())
                else:
                    print("Incompatible File")
    
            return(data)
                
        else:
            for key in data:
                if isinstance(data[key], str):          
                    ##PDF formatting
                    data[key] = re.sub(r"Page\s[0-9]{1,}", "", data[key]) #Removes page number
                    data[key] = re.sub(r"\n", "", data[key])
                    data[key] = data[key].strip()
                    data[key]=" ".join(data[key].split())
                elif isinstance(data[key], list):
                    for i in range(len(data[key])):      
                        ##PDF formatting
                        data[key][i] = re.sub(r"Page\s[0-9]{1,}", "", data[key][i]) #Removes page number
                        data[key][i] = re.sub(r"\n", "", data[key][i])
                        data[key][i] = data[key][i].strip()
                        data[key][i]=" ".join(data[key][i].split())
                else:
                    print("Incompatible File")
    
            return(data)
