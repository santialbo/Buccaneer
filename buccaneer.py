from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta
import re

def enum(**enums):
    return type('Enum', (), enums)

ORDER_BY = enum(NAME = 1, SIZE = 3, UPLOADER = 5, SEEDERS = 7, LEECHERS = 9, TYPE = 13)

def search(searchString, pageNumber = 0, orderBy = ORDER_BY.UPLOADER):
	url = ''.join(["http://thepiratebay.se/search/",
		   searchString.replace(" ", "%%20"),
		   "/" + str(pageNumber) + "/" + str(orderBy)])
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
	del trs[:2]
	results = []
	for tr in trs:
		results.append(_parse_search_result_table_row(tr))
	return results

def _parse_search_result_table_row(tr):
	res = {}
	tds = tr.findAll("td")
	linkName = tds[1].find("a", {"class": "detLink"})
	res['name'] = linkName.contents[0]
	res['link'] = linkName["href"]
	descString = tds[1].find("font").contents[0].replace("&nbsp;", " ")
	m = re.search("^Uploaded (Today|Y-day|\d\d-\d\d) (\d{4}|\d\d:\d\d), Size (\d+.\d* (?:[KMG]iB))", descString)
	res['size'] = m.group(3)
	now = datetime.today()
	if re.match("\d{4}", m.group(2)) == None:
		if m.group(1) == "Today":
			res['time'] = datetime.strptime(now.strftime("%m-%d-%Y") + " " + m.group(2), "%m-%d-%Y %H:%M")
		elif m.group(1) == "Y-day":
			res['time'] = datetime.strptime((now + timedelta(-1)).strftime("%m-%d-%Y") + " " + m.group(2), "%m-%d-%Y %H:%M")
		else:
			res['time'] = datetime.strptime(m.group(1) + "-" + str(now.year) + " " + m.group(2), "%m-%d-%Y %H:%M")
	else:
		res['time'] = datetime.strptime(m.group(1) + "-" + m.group(2), "%m-%d-%Y")
	res['seeders'] = int(tds[2].contents[0])
	res['leechers'] = int(tds[3].contents[0])
	res['magnet'] = tds[1].find("img", {"alt": "Magnet link"}).parent['href']
	return res