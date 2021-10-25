# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt8962124/']

    def parse(self, response):
        """
        """

        full_credits = response.url + 'fullcredits/'

        yield scrapy.Request(full_credits, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        """
        """

        paths = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        for path in paths:
            actor_page = response.urljoin(path)

            yield scrapy.Request(actor_page, callback = self.parse_actor_page)

    
    def parse_actor_page(self, response):
        """
        """

        overview = response.css("div#name-overview-widget")

        actor = overview.css("span.itemprop::text").get()

        for film in response.css("div.filmo-row"):

            category = film.css("::attr(id)").get()

            if ("actor" in category) or ("actress" in category):

                movie_or_TV_name = film.css("a::text").get()

                yield {"actor" : actor,
                       "movie_or_TV_name" : movie_or_TV_name}