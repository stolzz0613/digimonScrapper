import scrapy

#Titulos = //div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/text()
#Fechas = //div[contains(@class, "recuadro")]//div[contains(@class, "fecha")]/text()
#Link = //div[contains(@class, "recuadro")]//div[contains(@class, "titulo")]/a/href()
#Imagen = //div[contains(@class, "recuadro")]//div[contains(@class, "figure")]/img/@href

class Digimon(scrapy.Spider):
    name = 'links'
    start_urls = [
        'https://digimon.fandom.com/wiki/Category:Digimon_species'
    ]
    custom_settings = {
        'FEED_URI': 'digimon.json',
        'FEED_FORMAT': 'json',
        'CONCURRENT_REQUEST': 24,
        'MEMUSAGE_LIMIT_MB': 2048,
        'MEMUSAGE_NOTIFY_MAIL': ['andres0613@utp.edu.co'],
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'andresB',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def getImage(self, response, **kwargs):
        url = kwargs['url']
        image= response.xpath('//a[contains(@class, "image-thumbnail")]/img/@src').get()
        title= response.xpath('//h1[contains(@class, "page-header__title")]/text()').get()
        level= response.xpath('//div[contains(@class, "pi-border-color")]/div/text()').get()

        yield {
            'url': url,
            'image': image,
            'title': title,
            'level': level
        }

    def parse(self, response):
        links= response.xpath('//a[contains(@class, "category-page__member-link")]/@href').getall()
        nextPageLink= response.xpath('//a[contains(@class, "category-page__pagination-next")]/@href').get()

        for e in links:
            yield response.follow(e, callback=self.getImage, cb_kwargs= { 'url': e })
        if nextPageLink:
            yield scrapy.Request(nextPageLink, callback=self.parse)