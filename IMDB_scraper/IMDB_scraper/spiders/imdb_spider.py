# to run
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'

    start_urls = ['https://www.imdb.com/title/tt8962124/']

    def parse(self, response):
        """
        This method should assume that we start on a movie page
        and then navigate to the Cast & crew page.
        It does not return any data.
        """

        # URL of the Cast & crew page
        full_credits = response.url + 'fullcredits/'

        # yield a request specifying the parse_full_credits() method should be called
        # when we get to the Cast & crew page
        yield scrapy.Request(full_credits, callback = self.parse_full_credits)


    def parse_full_credits(self, response):
        """
        This method should assume that we start on the Cast & crew page
        and then navigate to the page of each actor listed on the page. 
        Crew members are not included. 
        It does not return any data.
        """

        # create a list of relative paths, one for each actor
        paths = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        # loop through the list of paths
        for path in paths:

            # URL of the page of each actor
            actor_page = response.urljoin(path)

            # yield a request specifying the parse_actor_page() method should be called
            # when the actor's page is reached
            yield scrapy.Request(actor_page, callback = self.parse_actor_page)

    
    def parse_actor_page(self, response):
        """
        This method should assume that we start on the page of an actor.
        It should yield a dictionary with two key-value pairs, 
        one of which contains the name of the actor, 
        the other of which contains the name of a movie or TV show, 
        for each of the movies or TV shows on which the actor has worked.
        """

        # container of the name of the actor
        overview = response.css("div#name-overview-widget")

        # extract the name of the actor
        actor_name = overview.css("span.itemprop::text").get()

        # loop through the actor's Filmography section
        for film in response.css("div.filmo-row"):
            
            # extract the id of each movie or TV show
            category = film.css("::attr(id)").get()

            # choose the movies and TV shows in the Actor or Actress section
            if ("actor" in category) or ("actress" in category):
                
                # extract the name of each movie or TV show
                movie_or_TV_name = film.css("a::text").get()

                # yield data
                yield {"actor" : actor_name,
                       "movie_or_TV_name" : movie_or_TV_name}