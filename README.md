# Buccaneer

Buccaneer scrapes the results for search queries on [The Pirate Bay](http://www.thepiratebay.se).

## Installing

Install the dependencies with:

```
pip install -r requirements.txt
```

## Use

Use the `search` function in order to perform a query. The parameters are the query string, an optional page number, and an optional "order by".

```python
>>> import buccaneer
>>> results = buccaneer.search('Revolution OS', 0, buccaneer.ORDER_BY.SEEDERS)
>>> for r in results[:3]:
...     print '{0} {1:4d} {2}...'.format(r['name'].ljust(60), r['seeders'], r['magnet'][:30])
...
Revolution OS                                                 266 magnet:?xt=urn:btih:f502f11df1...
[DVD-RIP ITA] Revolution OS (Documentario) [CR-Bt]              5 magnet:?xt=urn:btih:c8dc8d77bb...
Revolution OS [2001] V.O. Sub. Espa&amp;ntilde;ol [Spanish]     5 magnet:?xt=urn:btih:3835de2c06...
```
