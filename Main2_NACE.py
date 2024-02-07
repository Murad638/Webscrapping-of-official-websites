# ==================================================================================================================
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 2023

@author: Murad Khalilov
"""

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import datetime
import logging
import sys
import re


# Get the current username
user = os.getenv("USERNAME")

# Create a log file name with the current date and username
log_file_name = f"path to log files/NACE_{datetime.date.today()}-{user}.log"

# Configure the logging
logging.basicConfig(
    filename=log_file_name,
    level=logging.INFO,  # Set the log level to INFO or desired level
    format="%(asctime)s - %(levelname)s - %(message)s",
     filemode='w'
)

# Redirect standard output and error to the log file
sys.stdout = open(log_file_name, "w")
sys.stderr = open(log_file_name, "w")

start_time = time.time()

# Convert the Unix timestamp to a datetime object and format the datetime object as a string
date_time = datetime.datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')

# Print the formatted date and time as a string
print("Start time: ", date_time)



print("Second soup: European NACE codes")

# URL of the webpage to scrape
url = "https://ec.europa.eu/competition/mergers/cases/index/nace_all.html"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the HTML content
    html_content = response.text
    
    # Define a regular expression pattern to match the desired data
    pattern = r'(\S+ - .+?)\s*(?=<br>|$)'
    
    # Find all matches of the pattern in the HTML content
    matches = re.findall(pattern, html_content)
    
    # Split each match into code and description
    data = [match.split(" - ", 1) for match in matches]
    
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data, columns=["Code", "Description"])
    
    # Print the DataFrame
    print(df)


    df.to_csv(f"C:/Users/{user}/project/Murad's analysis/EU_NACE.csv", index=False, sep=';')
    
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)



print(f"Elapsed time: {(time.time() - start_time)/60} minutes.")

# To stop redirecting to the log file and restore the default behavior:
sys.stdout.close()
sys.stderr.close()
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
