#!/usr/bin/env python

"""
ASIN Lookup on Amazon.com
"""

import sys
import re
from bs4 import BeautifulSoup


if sys.version_info > (3, 0):
    # Python 3
    import requests
else:
    # Python 2
    import urllib2

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

    # Finds first result
    query_result = soup.find(id="result_0")
    if query_result:
        msrp = None
        dollar_amount = None
        cent_amount = None

        info = {"asin": None, "msrp": None, "price": None}

        # Get ASIN
        try:
            asin_string = query_result.attrs['data-asin']
        except Exception as e:
            print("Can't find ASIN")
            return None
        if asin_string:
            info["asin"] = asin_string

        # Get msrp
        msrp_query = query_result.find("span", class_="a-size-base-plus a-color-secondary a-text-strike")
        if msrp_query:
            info["msrp"] = parse_msrp(msrp_query.getText())
        
        # Get current dollar amount
        dollar_query = query_result.find("span", class_="sx-price-whole")
        if dollar_query:
            try:
                dollar_amount = int(dollar_query.getText())
            except Exception as e:
                print("Can't convert current dollar amount to int")

        # Get current cent amount
        cent_query = query_result.find("sup", class_="sx-price-fractional")
        if cent_query:
            try:
                cent_amount = int(cent_query.getText())    
            except Exception as e:
                print("Can't convert current cent amount to int")

        # Adds dollar and cents to info
        if dollar_amount:
            if cent_amount:
                info["price"] = (dollar_amount, cent_amount)
            else:
                info["price"] = (dollar_amount + 1, 0)
        
    return info


def parse_msrp(msrp):
    split_msrp = re.findall(r"\d+", msrp)
    if len(split_msrp) != 2:
        print("Can't parse msrp")
        return None
    try:
        parsed_msrp = tuple(int(part) for part in split_msrp)
    except Exception as e:
        print("Error converting list of strings to tuple of ints in parse msrp")
        return None
    return parsed_msrp


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
