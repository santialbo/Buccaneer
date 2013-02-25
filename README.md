# Buccaneer

Buccaneer is an unofficial API for The Pirate Bay (http://www.thepiratebay.se). You can use it for searching torrents in TPB easily.


## Example of usage

```python
	>>> import buccaneer
	>>> results = buccaneer.search('Weeds s08e04 720p', 0, buccaneer.order_by.SEEDERS)
	>>> for r in results:
	... 	print '{0} {1:5d}   {2}'.format(r['name'].ljust(45), r['seeders'], r['magnet'])
	...
	Weeds.S08E04.720p.HDTV.x264-EVOLVE [PublicHD]    882   magnet:?xt=urn:btih:662...
	Weeds.S08E04.720p.HDTV.x264-EVOLVE [PublicHD]     39   magnet:?xt=urn:btih:7b51...
	Weeds.S08E04.720p.HDTV.x264-EVOLVE                 7   magnet:?xt=urn:btih:6898...
```