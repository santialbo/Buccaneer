import buccaneer

results = buccaneer.search('Weeds s08e04 720p', 0, buccaneer.ORDER_BY.SEEDERS)
for r in results:
	print '{0} {1:5d}   {2}'.format(r['name'].ljust(45), r['seeders'], r['magnet'])
