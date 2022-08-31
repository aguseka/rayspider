import scrapy
import validators
import w3lib.html as r


class MyspiderSpider(scrapy.Spider):
    name = 'myspider'
    allowed_domains = ['raywhite.co.id']

    start_urls = [
        'https://www.raywhite.co.id/jual?listing_type=1&order=newest&limit=39&location=Denpasar&location2=Denpasar&page=1'
    ]

    def parse(self, response):
        links = response.css('li.page-item a::attr(href)')
        for link in links:
            # using url validator module to detect the url
            if validators.url(link.get()) is True:
                yield response.follow(link.get(), callback=self.page_parse,)
            else:
                pass

    def page_parse(self, response):
        links = response.css('div.col-sm-4 a::attr(href)')
        for link in links:
            yield response.follow(link.get(), callback=self.detail_parse,)

    def detail_parse(self, response):
        detail = response.css('div.row')
        yield {
            "main_title": detail.css('h2.card-title::text').get().replace('\t', '').replace('\n', ''),
            "title": detail.css('h1.section-heading::text').get().strip().replace('\t', '').replace('\n', ''),
            # trying to strip html tags and explode the list
            "description": (r.remove_tags(str(detail.css('p.card-text:nth-child(3)').getall()))).replace('\n\t[]', ''),
            "listing_id": detail.css('tr:nth-child(1) td:nth-child(2)::text').get(),
            "building_size": detail.css('tr:nth-child(2) td:nth-child(2)::text').get(),
            "land_size": detail.css('tr:nth-child(3) td:nth-child(2)::text').get(),
            "price": detail.css('tr:nth-child(4) td:nth-child(2)::text').get(),
            "url": response.url
        }
