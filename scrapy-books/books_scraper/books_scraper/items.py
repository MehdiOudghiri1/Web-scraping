# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):

    title = scrapy.Field()
    star_rating = scrapy.Field()
    availability = scrapy.Field()
    price = scrapy.Field()

    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    star_rating = scrapy.Field()
    tax = scrapy.Field()
    number_reviews = scrapy.Field()
    product_type = scrapy.Field()
    upc = scrapy.Field()
    description = scrapy.Field()


