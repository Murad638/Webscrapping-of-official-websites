# Web Scraping Python Code

## Overview

Main.py ---> python script performs web scraping to extract EMTAK (Estonian Classification of Economic Activities) codes from the [Estonian Business Register](https://ariregister.rik.ee/eng/company/) webpage. The script takes registration numbers from a feather file, sends requests to the website, extracts relevant information, and saves it to a CSV file.

## Worth-Mentioned Remarks
- The script may encounter errors, such as `er-ror` in logs summary, and takes approximately 21 minutes for 1000 requests.
- A total of 5 timeout errors were observed during testing.
- The script needs testing for the entire dataset (4300 registration numbers).

Main2_NACE.py ---> python script performs web scraping to extract European NACE codes from the [European Commission Mergers Cases](https://ec.europa.eu/competition/mergers/cases/index/nace_all.html) webpage. It retrieves the NACE codes and descriptions, saves them to a CSV file, and logs the process.

## Dependencies
- [Requests](https://docs.python-requests.org/en/master/) library
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library
- [Pandas](https://pandas.pydata.org/) library

Install the dependencies using:
```bash
pip install requests beautifulsoup4 pandas
