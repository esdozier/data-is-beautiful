#This is just a test program for eBay webscraping to harvest data for the PokeTCG Pricing Database
#The full data scraping program will be able to scrape a whole page of sold items and their sold date.
import httpx           
import json
import sys
from parsel import Selector

#Establishes our HTTP2 client with browser-like headers
session = httpx.Client(
    headers={
        "User-Agent": "Chrome/133.0.6943.142",
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3,q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip,deflate,br",
    },
    http2=True,
    follow_redirects=True
)

#Input for listing
url=input("Paste listing URL here:")
id=input("Name your file for the output .JSON:")

def parse_product(response: httpx.Response) -> dict:
    """Parse Ebay's product listing page for core product data"""
    sel = Selector(response.text)
    # define helper functions that chain the extraction process
    css_join = lambda css: "".join(sel.css(css).getall()).strip()  # join all selected elements
    css = lambda css: sel.css(css).get("").strip()  # take first selected element and strip of leading/trailing spaces

    item = {}
    item["url"] = css('link[rel="canonical"]::attr(href)')
    item["id"] = item["url"].split("/itm/")[1].split("?")[0]  # we can take ID from the URL
    item["price_original"] = css(".x-price-primary>span::text").replace("US $","")
    item["name"] = css_join("h1 span::text")

    return item


response = session.get(url)
product_data = parse_product(response)

f = open(id, 'x')
f.close()

with open(id, "w") as f:
    f.write(json.dumps(product_data, indent=2))
    f.close()
# write  the results in JSON format 

 