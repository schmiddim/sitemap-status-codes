import bs4 as bs
import multiprocessing as mp
import requests
from argparse import ArgumentParser


def parse_sitemap_xml(url, verbose):
    resp = requests.get(url)
    if 200 != resp.status_code:
        print(resp.status_code, str(url))
        return False
    soup = bs.BeautifulSoup(resp.content, 'xml')
    sitemaps = soup.findAll('sitemap')
    if len(sitemaps) == 0:
        if verbose:
            print('seems to be not a Sitemap Index')
        parse_sitemap(url, verbose)
    else:
        if verbose:
            print('this is a Sitemap Index - ', str(len(sitemaps)), ' Sitemaps found')
        for sitemap in sitemaps:
            loc = sitemap.find('loc').string
            parse_sitemap(loc, verbose)


def parse_sitemap(url, verbose):
    resp = requests.get(url)

    # we didn't get a valid response, bail
    if 200 != resp.status_code:
        print(resp.status_code, str(url))
        return False

    # BeautifulStoneSoup to parse the document
    soup = bs.BeautifulSoup(resp.content, 'xml')

    # find all the <url> tags in the document
    urls = soup.findAll('url')

    if verbose:
        print(str(len(urls)), ' urls found')

    # no urls? bail
    if not urls:
        return False
    # we do this in parallel now
    # @see http://sebastianraschka.com/Articles/2014_multiprocessing.html
    processes = [mp.Process(target=get_status_code, args=(url.find('loc').string, verbose)) for url in urls]
    for p in processes:
        p.start()
    for p in processes:
        p.join()


def get_status_code(url, verbose):
    resp = requests.get(url)
    if verbose or 200 != resp.status_code:
        print(resp.status_code, str(url))


if __name__ == '__main__':
    options = ArgumentParser()
    options.add_argument('-u', '--url', action='store', dest='url', help='The file contain one url per line')
    options.add_argument('-v', '--verbose', help='some interesting output', action="store_true")
    args = options.parse_args()
    parse_sitemap_xml(args.url, args.verbose)
