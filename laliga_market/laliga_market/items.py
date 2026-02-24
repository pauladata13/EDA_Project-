# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LaligaItem(scrapy.Item):
    equipo = scrapy.Field()
    valor_mercado = scrapy.Field()
    