Sitemap Status Codes
====================

This script tests all urls in a sitemap and echos everything that does not return 200 OK


Based on this Gist:
https://gist.github.com/chrisguitarguy/1305010

Requirements
============
I think you need Python 2.7 and BeautifulSoup 

Usage
=====
Please keep in mind that this is some kind of python sandbox for me. 
example:

```
python3 sitemap-status-codes3.py -u https://www.vapesetups.com/sitemap -v
```


this is way faster because I use Multiprocessing

@see http://sebastianraschka.com/Articles/2014_multiprocessing.html

```
python3 sitemap-status-codes-parallel3.py -u https://www.vapesetups.com/sitemap -v
```


