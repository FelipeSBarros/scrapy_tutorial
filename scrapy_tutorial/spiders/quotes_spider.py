import scrapy
from scrapy.loader import ItemLoader

from scrapy_tutorial.items import QuotesItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = "http://quotes.toscrape.com/"
        tag = getattr(self, "tag", None)
        if tag is not None:
            url = url + "tag/" + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        quotes = response.css("div.quote")

        for quote in quotes:
            loader = ItemLoader(item=QuotesItem(), selector=quote)
            loader.add_css("quote_content", ".text::text")
            loader.add_css("tags", ".tag::text")
            quote_item = loader.load_item()
            author_url = quote.css(".author + a::attr(href)").get()
            yield response.follow(
                author_url, self.parse_author, meta={"quote_item": quote_item}
            )

        yield from response.follow_all(css="ul.pager a", callback=self.parse)

    def parse_author(self, response):
        quote_item = response.meta["quote_item"]
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css("author_name", ".author-title::text")
        loader.add_css("author_birthday", ".author-born-date::text")
        loader.add_css("author_bornlocation", ".author-born-location::text")
        loader.add_css("author_bio", ".author-description::text")
        yield loader.load_item()
