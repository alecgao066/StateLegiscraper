"""
Helper Functions for Plotly Dash Dashboard
"""
import json
import re

from collections import defaultdict
import datetime
from datetime import date


class NVHelper:
    
   def nv_extract_month(nv_json_path):
       """
       
       Parameters
       ----------
       Local path of nv_json generated by nv_pdftotext.
           Local path of cleaned nv_json file. 
       Returns
       -------
       A new json file with month as the keys. We can call new_json_file[month] if we want the transcripts of meetings for this month.
       Eg: call new_json_file[4], we would get the transcripts for April.
   
       """
       data = open(nv_json_path)
       json_file = json.load(data)
   
       new_json_file = defaultdict(list)
   
       for key in json_file.keys():
           temp = json_file[key]
           match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)[ ]([1-9]|[12][0-9]|3[01])[,][ ]\d{4}', temp)
           date = datetime.datetime.strptime(match.group(), '%B %d, %Y').date()
           month = date.month
           new_json_file[month].append(temp)
           
       return(new_json_file)
  
   def nv_extract_date(nv_json_path):
       """
       
       Parameters
       ----------
       Local path of nv_json generated by nv_pdftotext.
           Local path of cleaned nv_json file. 
       Returns
       -------
       A new json file with month as the keys. We can call new_json_file[month] if we want the transcripts of meetings for this month.
       Eg: call new_json_file[4], we would get the transcripts for April.
   
       """
       data = open(nv_json_path)
       json_file = json.load(data)
   
       new_json_file = defaultdict(list)
   
       for key in json_file.keys():
           temp = json_file[key]
           match = re.search(r'(January|February|March|April|May|June|July|August|September|October|November|December)[ ]([1-9]|[12][0-9]|3[01])[,][ ]\d{4}', temp)
           date = datetime.datetime.strptime(match.group(), '%B %d, %Y').date()
           new_json_file[date] = temp
           
       return(new_json_file)   