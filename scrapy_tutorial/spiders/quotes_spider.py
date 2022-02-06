import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        url = 'http://quotes.toscrape.com/'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = url + 'tag/' + tag
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        author_url = response.css('.author + a::attr(href)').get()
        yield response.follow(author_url, self.parse_author)

        yield from response.follow_all(css='ul.pager a', callback=self.parse)

    def parse_author(self, response):
        yield {
            'author_name': response.css('.author-title::text').get().strip(),
            'auhtor_birthdate': response.css('.author-born-date::text').get(),
            'author_bornlocation': response.css('.author-born-location::text').get(),
            'author_bio': response.css('.author-description::text').get().strip(),
        }