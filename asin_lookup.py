#!/usr/bin/env python

"""
ASIN Lookup on Amazon.com
"""

import sys

if sys.version_info > (3, 0):
    # Python 3
    import requests
else:
    # Python 2
    import urllib2
import copy
from bs4 import BeautifulSoup

# Query ASIN on Amazon


def asin_lookup(product_name):
    # Convert spaces to pluses
    query_product_name = product_name.replace(' ', '+')

    # Query the movie title on Amazon.com
    asin_query_url = "http://www.amazon.com/s/?url=search-alias%3Daps&field-keywords=" + query_product_name + "&rh=i%3Aaps%2Ck%3A" + query_product_name

    if sys.version_info > (3, 0):
        # Python 3
        url_query = requests.get(asin_query_url)
        if url_query.status_code != 200:
            print("ULR  could not be opened")
            return None
        url_query_response = url_query.content
    else:
        # Python 2
        try:
            url_query_response = urllib2.urlopen(asin_query_url)
        except urllib2.HTTPError:
            print("URL could not be opened")
            return None

    
    soup = BeautifulSoup(url_query_response, "html.parser")

    # Look through first five results
    for i in range(0, 5):
        query_result = soup.find(id="result_" + str(i))
        if query_result:
            # Get ASIN
            try:
                asin_string = query_result.attrs['data-asin']
            except Exception as e:
                print("Can't find ASIN")
    
            # Get msrp
            msrp_query = query_result.find("span", class_="a-size-base-plus a-color-secondary a-text-strike")
            if msrp_query:
                msrp = msrp_query.getText()
            
            # Get current dollar amount
            dollar_query = query_result.find("span", class_="sx-price-whole")
            if dollar_query:
                dollar_amount = dollar_query.getText()

            # Get current cent amount
            cent_query = query_result.find("sup", class_="sx-price-fractional")
            if cent_query:
                cent_amount = cent_query.getText()

            if asin_string: print("ASIN: {}".format(asin_string))
            if msrp: print("MSRP: {}".format(msrp))
            if dollar_amount and cent_amount: print("Current price: ${}.{}".format(dollar_amount, cent_amount))

        else:
            break

    return


def main(argv=None):
    if argv is None:
        argv = sys.argv

    #0 Parse options and user input
    if len(argv) < 2:
        print("Please enter product name to lookup")
        return None

    product_name = argv[1]

    #1 Query for keywords
    asin_lookup(product_name)

if __name__ == "__main__":
    sys.exit(main())
