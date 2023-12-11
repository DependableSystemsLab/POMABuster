# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ERC20Item(scrapy.Item):
    index = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    price_in_usd = scrapy.Field()
    volume = scrapy.Field()
    market_cap_circulating = scrapy.Field()
    market_cap_onchain = scrapy.Field()
    holders = scrapy.Field()
    market_cap_fully_diluted = scrapy.Field()
    total_supply = scrapy.Field()
    # transfers = scrapy.Field() # dynamic load, not ez to get 
    decimals = scrapy.Field()
    official_website = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

class HolderItem(scrapy.Item):
    token_address = scrapy.Field()
    rank = scrapy.Field()
    holder_name = scrapy.Field()
    holder_address = scrapy.Field()
    amount = scrapy.Field()
    percentage = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)