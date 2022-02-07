from datetime import datetime

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def remove_quotes(text):
    # strip the unicode quote
    text = text.strip(u'\u201c'u'\u201d')
    return text


def convert_date(text):
    # convert string March 14, 1894 to python date
    return datetime.strptime(text, '%B %d, %Y')


def parse_location(text):
    # parse ocation "in Ulm, Germany" removing "in"
    return text[3:]


class QuotesItem(scrapy.Item):
    # define the fields for your item here like:
    quote_content = scrapy.Field(
        input_processor=MapCompose(remove_quotes),
        # TakeFirst return the first value not the whole list
        output_processor=TakeFirst()
    )
    tags = scrapy.Field()
    author_name = scrapy.Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    author_birthday = scrapy.Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    author_bornlocation = scrapy.Field(
        input_processor=MapCompose(parse_location),
        outpur_processor=TakeFirst()
    )
    author_bio = scrapy.Field(
        input_processor=MapCompose(str.split),
        output_processor=TakeFirst()  # need to be fixed
    )
