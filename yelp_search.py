from lxml import html
import csv
import requests
# from exceptions import ValueError
from time import sleep
import re
import argparse


def parse(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, headers=headers, verify=False).text
    parser = html.fromstring(response)
    print("Parsing the page")
    listing = parser.xpath("//li[@class='regular-search-result']")
    total_results = parser.xpath("//span[@class='pagination-results-window']//text()")
    scraped_datas = []
    for results in listing:
        raw_position = results.xpath(".//span[@class='indexed-biz-name']/text()")
        raw_name = results.xpath(".//span[@class='indexed-biz-name']/a//text()")
        raw_ratings = results.xpath(".//div[contains(@class,'rating-large')]//@title")
        raw_review_count = results.xpath(".//span[contains(@class,'review-count')]//text()")
        raw_price_range = results.xpath(".//span[contains(@class,'price-range')]//text()")
        category_list = results.xpath(".//span[contains(@class,'category-str-list')]//a//text()")
        raw_address = results.xpath(".//address//text()")
        is_reservation_available = results.xpath(".//span[contains(@class,'reservation')]")
        is_accept_pickup = results.xpath(".//span[contains(@class,'order')]")
        url = "https://www.yelp.com" + results.xpath(".//span[@class='indexed-biz-name']/a/@href")[0]

        name = ''.join(raw_name).strip()
        position = ''.join(raw_position).replace('.', '')
        cleaned_reviews = ''.join(raw_review_count).strip()
        reviews = re.sub("\D+", "", cleaned_reviews)
        categories = ','.join(category_list)
        cleaned_ratings = ''.join(raw_ratings).strip()
        if raw_ratings:
            ratings = re.findall("\d+[.,]?\d+", cleaned_ratings)[0]
        else:
            ratings = 0
        price_range = len(''.join(raw_price_range)) if raw_price_range else 0
        address = ' '.join(' '.join(raw_address).split())
        reservation_available = True if is_reservation_available else False
        accept_pickup = True if is_accept_pickup else False
        data = {
            'business_name': name,
            'rank': position,
            'review_count': reviews,
            'categories': categories,
            'rating': ratings,
            'address': address,
            'reservation_available': reservation_available,
            'accept_pickup': accept_pickup,
            'price_range': price_range,
            'url': url
        }
        scraped_datas.append(data)
    return scraped_datas


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-p', '--place', action='store',
                           help='Location/ Address/ zip code')
    argparser.add_argument('-f', '--input_file', action='store',
                           help='Input File (Forward Slash (/) Separated and New Line Separated)')
    argparser.add_argument('-ef', '--example_file', action='store_true',
                           help='Example Input File')
    search_query_help = """Some available search queries are:\n
                            Restaurants,\n
                            Breakfast & Brunch,\n
                            Coffee & Tea,\n
                            Delivery,
                            Reservations"""
    argparser.add_argument('-s', '--search_query', action='store', help=search_query_help)
    args = argparser.parse_args()

    if args.example_file:
        print("--START OF FILE--\nrestaurants/Boston,MA\ncoffee_shops/Boston,MA\n--END OF FILE--")
        exit()

    if args.input_file:
        input_list = []
        with open(args.input_file) as f:
            input_lines = f.readlines()
        for line in input_lines:
            line = line.split('/')
            input_list.append((line[0], line[1].replace('_', ' ')))
    else:
        input_list = [(args.place, args.search_query)]

    for place, search_query in input_list:

        yelp_url = "https://www.yelp.com/search?find_desc=%s&find_loc=%s" % (search_query, place)
        print("Retrieving :", yelp_url)
        scraped_data = parse(yelp_url)
        print("Writing data to output file")
        with open("scraped_yelp_results_for_%s.csv" % (place), "w") as fp:
            fieldnames = ['business_name', 'rank', 'review_count', 'categories', 'rating', 'address',
                          'reservation_available', 'accept_pickup', 'price_range', 'url']
            writer = csv.DictWriter(fp, fieldnames=fieldnames)
            writer.writeheader()
            for data in scraped_data:
                writer.writerow(data)
