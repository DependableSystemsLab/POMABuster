import scrapy
from scrape_erc20.items import ERC20Item


class EtherscanERC20Spider(scrapy.Spider):
    name = 'ERC20'
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrape_erc20.pipelines.ERC20SanitizationPipeline': 1,
        }
    }
    allowed_domains = ['etherscan.io']
    start_urls = ['https://etherscan.io/tokens?p=1']

    def parse(self, response):
        table = response.xpath(
            '//*[@id="ContentPlaceHolder1_tblErc20Tokens"]')
        rows = table.xpath('//tr')
        for item in rows:
            item = ERC20Item(
                index = item.xpath('(td)[1]//text()').extract_first(),
                name = item.xpath('(td)[2]/a/div//text()').extract(),
                address = item.xpath('(td)[2]//@href').extract_first(),
                # 'description': item.xpath('(td)[3]//text()').extract_first(),
                price_in_usd = item.xpath('(td)[3]//text()').extract_first(),
                volume = item.xpath('(td)[5]//text()').extract_first(),
                market_cap_circulating = item.xpath('(td)[6]//text()').extract_first(),
                market_cap_onchain = item.xpath('(td)[7]//text()').extract_first(),
                holders = item.xpath('(td)[8]//text()').extract_first(),
                )
            # yield item
            if item['address']:
                yield response.follow(
                    item['address'], self.parse_overview, meta={'item': item})

        next_page = response.xpath(
            '(//ul[@class="pagination pagination-sm mb-0"]//li)[4]//@href').extract_first()
        if next_page:
            yield response.follow(next_page, self.parse)
    
    def parse_overview(self, response):
        overview = response.xpath('//section[@id="ContentPlaceHolder1_divSummary"]/div[@class="row g-3 mb-4"]')
        item = response.meta.get('item')
        item['market_cap_fully_diluted'] = overview.xpath(
            '//div[@id="ContentPlaceHolder1_tr_marketcap"]/div/text()').extract_first()
        item['total_supply'] = overview.xpath('//div[@class="d-flex align-items-center"]/span/text()').extract_first()
        item['decimals'] = overview.xpath('//div[@class="col-lg-4"]/div/div[@class="card-body d-flex flex-column gap-5"]/div/h4/b/text()').extract_first()
        item['official_website'] = overview.xpath('//div[@id="ContentPlaceHolder1_divLinks"]//span[@class="hash-tag text-truncate"]/text()').extract_first()
        yield item
