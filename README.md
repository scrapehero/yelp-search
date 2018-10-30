# Yelp Search Scraper
Script to extracts business listings from yelp.com

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Fields to Extract

This yelp search scraper can extract the fields below:

1. Business Name
2. Rank
3. Review Count
4. Categories
5. Rating
6. Address
7. Reservation Available
8. Accept Pickup
9. Price Range
10. Yelp URL

### Prerequisites

For this web scraping tutorial using Python 3, we will need some packages for downloading and parsing the HTML. 
Below are the package requirements:

 - lxml
 - requests
 - unicodecsv

### Installation
Run the following from the base directory.
```
pip install -r requirements.txt
```
--OR--

PIP to install the following packages in Python (https://pip.pypa.io/en/stable/installing/) 

Python Requests, to make requests and download the HTML content of the pages (http://docs.python-requests.org/en/master/user/install/)

Python LXML, for parsing the HTML Tree Structure using Xpaths (Learn how to install that here – http://lxml.de/installation.html)

## Running the scraper
We would execute the code with the script name followed by the flagged arguments **place** and **keyword**. Here is an example
to find the business details for restaurants in Boston. MA.

```
python3 yelp_search.py -p Boston,MA -s restaurants 
```
```
python3 yelp_search.py -f input_file.txt 
```
**NEED HELP?**

Run the following to see the help for the python file.
```
python3 yellow-pages.py -h
```
