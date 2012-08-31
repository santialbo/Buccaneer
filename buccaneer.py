from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
from datetime import datetime
import re

def enum(**enums):
    return type('Enum', (), enums)

order_by = enum(NAME = 1, SIZE = 3, UPLOADER = 5, SEEDERS = 7, LEECHERS = 9, TYPE = 13)

def search(searchString, pageNumber = 0, orderBy = order_by.UPLOADER):
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
	del trs[0]
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
	m = re.search("^Uploaded (\d\d-\d\d) (\d{4}|\d\d:\d\d), Size (\d+.\d* (?:[KMG]iB))", descString)
	res['size'] = m.group(3)
	if re.match("\d{4}", m.group(2)) == None:
		res['time'] = datetime.strptime(m.group(1) + "-" + str(datetime.now().year) + " " + m.group(2), "%m-%d-%Y %H:%M")
	else:
		res['time'] = datetime.strptime(m.group(1) + "-" + m.group(2), "%m-%d-%Y")
	res['seeders'] = int(tds[2].contents[0])
	res['leechers'] = int(tds[3].contents[0])
	res['magnet'] = tds[1].find("img", {"alt": "Magnet link"}).parent['href']
	return res