import json
import math
import httpx
import asyncio

from typing import Dict, List, Literal
from urllib.parse import urlencode
from parsel import Selector

#Utilizing session information from parser guide documentation @Scrapfly.io
session = httpx.AsyncClient(
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
    },
    http2=True,
    follow_redirects=True
)


def parse_search(response: httpx.Response) -> List[Dict]:
    """parse ebay's search page for listing preview details"""
    previews = []
    # each listing has it's own HTML box where all of the data is contained
    sel = Selector(response.text)
    listing_boxes = sel.css(".srp-results li.s-item")
    for box in listing_boxes:
        # quick helpers to extract first element and all elements
        css = lambda css: box.css(css).get("").strip()
        css_all = lambda css: box.css(css).getall()
        previews.append(

            {
                #removed url output in favor of item unique id
                "id": css("a.s-item__link::attr(href)").split("/itm/")[1].split("?")[0],
                "title": css(".s-item__title>span::text"),
                "price": css(".s-item__price span::text").replace("$",""),
                "sold_date": css(".s-item__caption--signal span::text")
            }
            
        )
    return previews

async def scrape_search(
    query,
    max_pages=1,
    category=0,
    osacat=0,
    sold=1,
    complete=1,
    item_condition=3,
    items_per_page=240,
    sort: Literal["newly_listed", "ended_recently"] = "ended_recently",
) -> List[Dict]:
    """Scrape Ebay's search results page for product preview data for given"""

    def make_request(page):
        #Original block used to build ebay URL. Replaced with direct user input of a page they would like to scrape from. 
        #return "https://www.ebay.com/sch/i.html?" + urlencode({_nkw": query, "_sacat": category, _ipg": items_per_page, "LH_sold":sold, "LH_complete":complete, "_ItemCondition":item_condition, "_osacat":osacat})
        url_input = input("Copy and Past an eBay search page results: ")
        return url_input
    
    first_page = await session.get(make_request(page=1))
    results = parse_search(first_page)
    if max_pages == 1:
        return results
    # find total amount of results for concurrent pagination
    total_results = first_page.selector.css(".srp-controls__count-heading>span::text").get()
    total_results = int(total_results.replace(",", ""))
    total_pages = math.ceil(total_results / items_per_page)
    if total_pages > max_pages:
        total_pages = max_pages
    other_pages = [session.get(make_request(page=i)) for i in range(2, total_pages + 1)]
    for response in asyncio.as_completed(other_pages):
        response = await response
        try:
            results.extend(parse_search(response))
        except Exception as e:
            print(f"failed to scrape search page {response.url}")
    return results

id=input("Name your file:")

data = asyncio.run(scrape_search(""))

f = open(id, 'x') #ensures creation of file requested 
f.close()

with open(id, "w") as f:
    f.write(json.dumps(data, indent=2)) #writes generated json text to file created from previous statement
    f.close()