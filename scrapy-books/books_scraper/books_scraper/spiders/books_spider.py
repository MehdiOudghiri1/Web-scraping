import scrapy
from books_scraper.items import BookItem

class BookSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):

        for book in response.css('article.product_pod'):
            book_item = BookItem()
            book_item['title'] =  book.css('h3 a::attr(title)').get()
            book_item['star_rating'] = book.css('p ::attr(class)').get()
            book_item['availability'] = ''.join(book.css('p.instock.availability::text').getall()).strip()
            book_item['price'] =  book.css('div.product_price p.price_color::text').get()
        
            book_page = book.css('h3 a::attr(href)').get()

            if book_page:
                book_page_url = response.urljoin(book_page)

                yield response.follow(
                    book_page_url,
                    callback=self.parse_book,
                    meta={'book_item' : book_item}
                )

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield response.follow(next_page_url, callback=self.parse)


    def parse_book(self, response):
        book_item = response.meta['book_item']

        table = response.css('table.table.table-striped tr')
        book_item['description'] = response.css('#product_description ~ p::text').get()
        book_item['upc'] = table[0].css('td::text').get()
        book_item['product_type'] = table[1].css('td::text').get()
        book_item['price_excl_tax'] = table[2].css('td::text').get()
        book_item['price_incl_tax'] = table[3].css('td::text').get()
        book_item['tax'] = table[4].css('td::text').get()
        book_item['availability'] = table[5].css('td::text').get()
        book_item['number_reviews'] = table[6].css('td::text').get()

        yield book_item
        


        