#!/usr/bin/python2.7
import requests
from argparse import ArgumentParser
from BeautifulSoup import BeautifulStoneSoup as Soup


def parse_sitemap_xml(url, verbose):
    resp = requests.get(url)
    if 200 != resp.status_code:
        print resp.status_code, str(url)
        return False
    soup = Soup(resp.content)
    sitemaps = soup.findAll('sitemap')
    if len(sitemaps) == 0:
        if verbose:
            print 'seems to be not a Sitemap Index'
        parse_sitemap(url, verbose)
    else:
        if verbose:
            print 'this is a Sitemap Index - ', str(len(sitemaps)), ' Sitemaps found'
        for sitemap in sitemaps:
            loc = sitemap.find('loc').string
            parse_sitemap(loc, verbose)


def parse_sitemap(url, verbose):
    resp = requests.get(url)

    # we didn't get a valid response, bail
    if 200 != resp.status_code:
        print resp.status_code, str(url)
        return False

    # BeautifulStoneSoup to parse the document
    soup = Soup(resp.content)
    # find all the <url> tags in the document
    urls = soup.findAll('url')

    if verbose:
        print  str(len(urls)), ' urls found'

    # no urls? bail
    if not urls:
        return False

    # extract what we need from the url
    for u in urls:
        loc = u.find('loc').string
        resp = requests.get(loc)
        if 200 != resp.status_code:
            print resp.status_code, str(loc)
        if verbose:
            print resp.status_code, str(loc)


if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('-u', '--url', action='store', dest='url', help='The file contain one url per line')
    options.add_argument('-v', '--verbose', help='some interesting output', action="store_true")
    args = options.parse_args()
    parse_sitemap_xml(args.url, args.verbose)
