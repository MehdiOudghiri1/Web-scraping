# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
    quote = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()


class AuthorItem(scrapy.Item):
    place_birth = scrapy.Field()
    date_birth = scrapy.Field()
    date_death = scrapy.Field()
    genre = scrapy.Field()
    influences = scrapy.Field()
    books = scrapy.Field()
    description = scrapy.Field()


