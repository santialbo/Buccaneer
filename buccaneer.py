"""
Buccaneer is a python script that scrapes the results in The Pirate Bay
"""
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta
import re

def enum(**enums):
    """
    Lets define enums
    """
    return type('Enum', (), enums)

ORDER_BY = enum(NAME = 1,
                SIZE = 3,
                UPLOADER = 5,
                SEEDERS = 7,
                LEECHERS = 9,
                TYPE = 13,
                UPLOADED = 99)

def search(search_string, page = 0, order_by = ORDER_BY.UPLOADER):
    """
    Searches for the given string in The Pirate Bay.
    Returns a list of dictionaries with the information of each torrent.
    """
    url = ''.join(["http://thepiratebay.se/search/",
           search_string.replace(" ", "%%20"),
           "/" + str(page) + "/" + str(order_by)])
    resp = urlopen(url)
    html = resp.read()
    soup = BeautifulSoup(html)
    table = soup.find("table", {"id": "searchResult"})
    if table == None:
        return []
    else:
        return _parse_search_result_table(table)

def _parse_search_result_table(table):
    trs = table.findAll("tr")
    del trs[:1]
    results = []
    for tr in trs:
        results.append(_parse_search_result_table_row(tr))
    return results

def _parse_search_result_table_row(tr):
    res = {}
    tds = tr.findAll("td")
    link_name = tds[1].find("a", {"class": "detLink"})
    res['name'] = link_name.contents[0].encode('utf-8').strip()
    res['link'] = link_name["href"]
    desc_string = tds[1].find("font").contents[0].replace("&nbsp;", " ")
    m = re.search(r"^Uploaded (Today|Y-day|\d\d-\d\d) (\d{4}|\d\d:\d\d), " +
            r"Size (\d+(?:.\d*)? (?:[KMG]iB))", desc_string)
    res['size'] = m.group(3)
    now = datetime.today()
    if re.match(r"\d{4}", m.group(2)) == None:
        hour =" " + m.group(2)
        if m.group(1) == "Today":
            res['time'] = datetime.strptime(
                    now.strftime("%m-%d-%Y") + hour,
                    "%m-%d-%Y %H:%M")
        elif m.group(1) == "Y-day":
            res['time'] = datetime.strptime(
                    (now + timedelta(-1)).strftime("%m-%d-%Y") + hour,
                     "%m-%d-%Y %H:%M")
        else:
            res['time'] = datetime.strptime(
                    m.group(1) + "-" + str(now.year) + hour,
                    "%m-%d-%Y %H:%M")
    else:
        res['time'] = datetime.strptime(m.group(1) + "-" + m.group(2),
                "%m-%d-%Y")
    res['seeders'] = int(tds[2].contents[0])
    res['leechers'] = int(tds[3].contents[0])
    res['magnet'] = tds[1].find("img", {"alt": "Magnet link"}).parent['href']
    return res

