# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt8962124/']

    def parse(self, response):
        """
        """

        next_page = response.urljoin('fullcredits/')

        yield scrapy.Request(next_page, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        """
        """

        links = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for link in links:
            yield scrapy.Request(link, callback = self.parse_actor_page)