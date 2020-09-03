#!/usr/bin/env python3
from bs4 import BeautifulSoup
from PyRSS2Gen import RSSItem, Guid
import ScrapeNFeed


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
        title = l.select_one('h1').contents[0]
        # desc = l.select_one('p.subhead').contents[0]
        date = l.parent.select_one('time').contents[0]
    else:
        title = l.select_one('h2').contents[0]
        date = l.parent.select_one('time').contents[0]
    desc = l.select_one('p.subhead').contents[0]
    link = l['href']
    if prepend_to_link is not None:
        link = f"{prepend_to_link}{link}"
    print(f"mk_rss: {title} - {link}")
    return RSSItem(
        link=l.href,
        description=desc,
        guid=Guid(link),
        pubDate=date,
        title=title
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
        rss_items = list([mk_rss(l, prepend_to_link=self.baseURL) for l in links])
        # print(rss_items)
        self.addRSSItems(rss_items)

        return


FPMFeed.load("New FrontPageMag posts",
             'https://www.frontpagemag.com/',
             "FrontPageMag RSS feed - unofficial",
             'fpm.xml',
             'fpm-state.pickle')
