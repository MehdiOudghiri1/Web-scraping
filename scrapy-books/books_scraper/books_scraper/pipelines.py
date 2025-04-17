# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BooksScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        title = adapter.get('title')
        if title:
            adapter['title'] = title.strip()

        availability = adapter.get('availability')
        if availability:
            try:
                adapter['availability'] = float(availability.strip().split("(")[1].split(' ')[0])
            except:
                adapter['availability'] = None
        
        star_rating = adapter.get('star_rating')
        if star_rating:
            adapter['star_rating'] = star_rating.split(' ')[1]

        prices = ('price', 'price_incl_tax', 'price_excl_tax', 'tax')
        for price in prices:
            p = adapter.get(price)
            if price:
                try:
                    adapter[price] = float(p[1:])
                except:
                    adapter[price] = None
        upc = adapter.get('upc')
        if upc:
            adapter['upc'] = upc.strip() 

        description = adapter.get('description')
        if description:
            adapter['description'] = description.strip()       
        
        
        return item
