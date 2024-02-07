# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 2023

@author: Murad Khalilov
"""

### worth-mentioned remarks:
# error -> er-ror (because logs summary shows huge numbers)
# takes 21 minutes for 1000 requests
# only 5 timeout error
# need to test for whole data (4300)

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
log_file_name = f"path to log files/EMTAK_BT_{datetime.date.today()}-{user}.log"

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



main_data = pd.read_feather("data.feather")

main_data['REG_NR'] = main_data['REG_NR'].astype(str)

print("Unique numbers of Reg_nr: ", len(main_data[(main_data['country'] == 'Estonia')]['REG_NR'].unique()))

registration_numbers = main_data[(main_data['country'] == 'Estonia')]['REG_NR'].unique().tolist()

url_base = "https://ariregister.rik.ee/eng/company/"


dfs = []
n = 0
empty = 0
empty_list = []
request_error = 0
request_error_list = []


for reg_number in registration_numbers:

    
    try:

        # Define headers as a dictionary
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }


        session = requests.Session()
        retry_strategy = Retry(total=3, backoff_factor=2, status_forcelist=[500, 502, 503, 504])
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)

        url = url_base + reg_number

        response = session.get(url, timeout=4, headers=headers)
        
        if response.status_code == 429:
            print(f"Received a 429 er-ror for {url}. Waiting and retrying...")
            time.sleep(1)  # Wait for the defined delay
            #response = requests.get(url)  # Retry the request
            response = session.get(url, timeout=4, headers=headers)


        response.raise_for_status()
    

        #if n % 20 == 0 & n < 500:
        #    time.sleep(5)

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', id='areas-of-activity-table')


        #print(table)
        if table:
            # Find the table headers (th elements) within the table's thead
            header_row = table.find('thead').find('tr')
            headers = [header.get_text(strip=True) for header in header_row.find_all('th')]

            # Find all rows (tr elements) within the table's tbody
            rows = table.find('tbody').find_all('tr')


            data_list = []

            # Iterate through the rows and extract data with headings
            for row in rows:
                # Extract the text from each cell (td element) within the row
                cells = row.find_all('td')
                if len(cells) == len(headers):
                    data = [cell.get_text(strip=True) for cell in cells]

                    # Create a dictionary to associate data with headings
                    data_dict = dict(zip(headers, data))
                    
                    data_list.append(data_dict)

                    # Break out of the loop after processing the first row --- only needed first row either Principial activity or something else...
                    break



                    #if "Principal activity" in data:
                    #    # Append the dictionary to the data_list
                       




            # Create a DataFrame from the data list
            if data_list:
                df = pd.DataFrame(data_list)
                df['REG_NR'] = reg_number
                dfs.append(df)

        else:
            print(f"Table with id - {reg_number} - 'areas-of-activity-table' not found.")
            empty = empty + 1
            empty_list.append(reg_number)

        print('Batch: ', n)
        n = n+1

    except requests.exceptions.RequestException as e:
        print("Request er-ror:", e)
        request_error = request_error + 1
        request_error_list.append(reg_number)





# Combine all DataFrames into one
if dfs:
    combined_df = pd.concat(dfs, ignore_index=True)
    print("Combined DataFrame:")
    print(combined_df)
else:
    print("No data found for any registration number.")



print("Writing csv file..")

combined_df.to_csv(f"C:/Users/{user}/project/Murad's analysis/EMTAK_codes_EE.csv", sep=';',  encoding='utf-8',  index = False)



print(f"number of Empty REG_NRs not found in website: {empty} and {empty_list}")
print(f"number of Request er-ror in website: {request_error} and {request_error_list}")



print(f"Elapsed time: {(time.time() - start_time)/60} minutes.")

# To stop redirecting to the log file and restore the default behavior:
sys.stdout.close()
sys.stderr.close()
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__
