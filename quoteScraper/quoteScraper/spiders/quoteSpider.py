import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



from quoteScraper.items import AuthorItem, QuoteItem

class LoginSpider(scrapy.Spider):
    name = 'loginquotes'
    start_urls = ['https://quotes.toscrape.com/login']

    def __init__(self, *args, **kwargs):
        super(LoginSpider, self).__init__(*args, **kwargs)
        # Setup Chrome options for selnium
        # chrome_options = Options()
        # chrome_options.add_argument("--headless") # no UI
        # self.driver = webdriver.Chrome(options=chrome_options)

    def parse(self, response):
        token = response.css('input[name="csrf_token"]::attr(value)').get()
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'csrf_token': token,
                'username': 'Marran',
                'password': '12M3zz'
            },
            callback=self.after_login

        )

    def after_login(self, response):
        if "Logout" not in response.text:
            self.logger.error("Login failed")
            return 
        
        self.logger.info("Login successful. Scraping quotes...")
        # Actual scraping
        quotes_divs = response.css("div.quote")
        print(f'len quotes_div = {len(quotes_divs)}')
        for quote_div in quotes_divs:
            quote_item = QuoteItem()
            quote_item['quote'] = quote_div.css("span.text::text").get()
            print("*********!!!!!!!!!!!!*******************")
            print(quote_div.css("span.text::text").get())
            quote_item['tags'] = quote_div.css("div.tags a.tag::text").getall()
            

            goodreads_url = quote_div.xpath('.//span[2]/a[2]/@href').get()
            print(goodreads_url)
            yield response.follow(
                    goodreads_url,
                    callback=self.parse_goodreads_ns,
                    meta={'quote_item':quote_item},
                    dont_filter=True
                  )
            
        next_page_url = response.css('li.next a::attr(href)').get()
        yield response.follow(
                next_page_url,
                callback=self.after_login,
                dont_filter=True
              )

            
        
        
    # def parse_goodreads(self, response):
    #     quote_item = response.meta['quote_item']
    #     author_item = AuthorItem()

    #     # Basic data extraction
    #     author_item['date_birth'] = response.xpath('//div[@itemprop="birthDate"]/text()').get()
    #     author_item['date_death'] = response.xpath('//div[@itemprop="deathDate"]/text()').get()
    #     author_item['place_birth'] = response.xpath('//div[div[text()="born"]]/text()').get()
    #     author_item['description'] = response.css('span[id^="freeTextContainer"]::text').get()
    #     author_item['books'] = response.css('span[itemprop="name"][role="heading"]::text').getall()

    #     # Check for "...more" to load additional genres/tags
    #     more_button_exists = response.xpath('//a[contains(text(), "...more")]')
    #     if more_button_exists:
    #         chrome_options = Options()
    #         chrome_options.add_argument("--headless")
    #         driver = webdriver.Chrome(options=chrome_options)

    #         try:
    #             driver.get(response.url)
    #             driver.implicitly_wait(3)

    #             more_button = driver.find_element(By.XPATH, '//a[contains(text(), "...more")]')
    #             more_button.click()
    #             driver.implicitly_wait(1)

    #             updated_html = driver.page_source
    #             updated_response = scrapy.Selector(text=updated_html)

    #             genres = updated_response.xpath('//div[text()="Genre"]/following-sibling::div[1]/a/text()').getall()
    #         finally:
    #             driver.quit()
    #     else:
    #         genres = response.xpath('//div[text()="Genre"]/following-sibling::div[1]/a/text()').getall()

    #     author_item['genre'] = genres
    #     quote_item['author'] = author_item

    #     yield quote_item

    def parse_goodreads_ns(self, response):
        quote_item = response.meta['quote_item']
        author_item = AuthorItem()
        # Basic data extraction
        author_item['date_birth'] = response.xpath('//div[@itemprop="birthDate"]/text()').get()
        author_item['date_death'] = response.xpath('//div[@itemprop="deathDate"]/text()').get()
        author_item['place_birth'] = response.xpath('//div[div[text()="Born"]]/text()').get()
        author_item['description'] = response.css('span[id^="freeTextContainer"]::text').get()
        author_item['books'] = response.css('span[itemprop="name"][role="heading"]::text').getall()
        # Check for "...more" to load additional genres/tags
        more_button_exists = response.xpath('//a[contains(text(), "...more")]')
        if more_button_exists:
            genres = response.xpath('//div[text()="Genre"]/following-sibling::div[1]/a/text()').getall()
        else:
            genres = response.xpath('//div[text()="Genre"]/following-sibling::div[1]/a/text()').getall()
        author_item['genre'] = genres
        quote_item['author'] = author_item
        yield quote_item
        
    # def more_click(self, response):
        

