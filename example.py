import buccaneer

results = buccaneer.search('Revolution OS', 0, buccaneer.ORDER_BY.SEEDERS)
for r in results[:3]:
    print '{0} {1:4d} {2}...'.format(r['name'].ljust(60), r['seeders'], r['magnet'][:30])
