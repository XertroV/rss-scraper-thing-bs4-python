#!/usr/bin/env python3
from bs4 import BeautifulSoup
from PyRSS2Gen import RSSItem, Guid
import ScrapeNFeed
from datetime import datetime
import urllib.parse


class OReillyFeed(ScrapeNFeed.ScrapedFeed):

    def HTML2RSS(self, headers, body):
        soup = BeautifulSoup(body, 'lxml')
        headerText = soup.firstText('Upcoming Titles')
        titleList = headerText.findNext('ul')
        items = []
        for item in titleList('li'):
            link = self.baseURL + item.a['href']
            if not self.hasSeen(link):
                bookTitle = item.a.string
                releaseDate = item.em.string
                items.append(RSSItem(title=bookTitle,
                                     description=releaseDate,
                                     link=link))
        self.addRSSItems(items)


# OReillyFeed.load("Newly announced O'Reilly books",
#                  'http://www.oreilly.com/catalog/new.html',
#                  "Keep track of O'Reilly books as they're announced",
#                  'oreilly.xml',
#                  'oreilly.pickle',
#                  managingEditor='leonardr@segfault.org (Leonard Richardson)')


def mk_rss(l, prepend_to_link=None):
    if l.select_one('h1') is not None:
        title = ''.join(l.select_one('h1').strings)
    else:
        title = ''.join(l.select_one('h2').strings)

    subhead = l.select_one('p.subhead')
    desc = "(no description)" if subhead is None else subhead.contents[0]

    author = l.parent.select_one(".field-author").contents[0].strip()

    date_str = l.parent.select_one('time').contents[0]
    date = datetime.strptime(date_str, '%b %d, %Y')
    ctime = date.ctime()
    pub_date = (f'{ctime[0:3]}, {date.day:02d} {ctime[4:7]}'
                + date.strftime(' %Y %H:%M:%S %z'))

    link = l['href']
    if prepend_to_link is not None:
        link = f"{prepend_to_link}{link}"
    print(f"mk_rss: {title} by {author} on {pub_date} - {link}")
    return RSSItem(
        link=link,
        description=desc,
        guid=Guid(link),
        pubDate=pub_date,
        title=title,
        author=author
    )


class FPMFeed(ScrapeNFeed.ScrapedFeed):

    def HTML2RSS(self, headers, body):
        soup = BeautifulSoup(body, 'html.parser')
        homepage = soup.select_one('.homepage')
        # print(f"homepage: {homepage}")
        articles = homepage.select('article')
        # print(f"articles: {articles}")
        # all_links = homepage('a')
        links = list([art.select_one('a') for art in articles])
        parsed_url = urllib.parse.urlparse(self.baseURL)
        # print(parsed_url)        
        rss_items = list([mk_rss(l, prepend_to_link=f"https://{parsed_url.netloc}") for l in links])
        # print(rss_items)
        self.addRSSItems(rss_items)

        return


FPMFeed.load("New FrontPageMag posts",
             'https://www.frontpagemag.com',
             "FrontPageMag RSS feed - unofficial",
             'fpm.xml',
             'fpm-state.pickle')

FPMFeed.load("The Point blog on FPM - new posts",
             'https://www.frontpagemag.com/point/',
             "The Point (FPM) RSS feed - unofficial",
             'fpm-the-point.xml',
             'fpm-the-point-state.pickle')
