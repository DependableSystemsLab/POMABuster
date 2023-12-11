import scrapy
import json
from scrape_erc20.items import HolderItem


class EtherscanERC20HolderSpider(scrapy.Spider):
    name = 'Holder'
    allowed_domains = ['etherscan.io']
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrape_erc20.pipelines.HolderSanitizationPipeline': 1,
        }
    }

    def start_requests(self):
        url = 'https://etherscan.io/token/tokenholderchart/{}'
        token_file = 'erc20.jsonlines'
        with open(token_file) as f:
            tokens = [json.loads(line)['address'] for line in f]
            # data = json.load(f)
            # tokens = [item['address'] for item in data]
        return [scrapy.FormRequest(
            url.format(address), callback=self.parse, meta={'address': address}) for address in tokens]

    def parse(self, response):
        table = response.xpath("//*[@id='ContentPlaceHolder1_resultrows']")
        rows = table.xpath('//tr')
        for item in rows:
            item = HolderItem(
                token_address = response.meta['address'],
                rank = item.xpath('(td)[1]//text()').extract_first(),
                holder_name = item.xpath('(td)[2]//text()').extract_first(),
                holder_address = item.xpath('(td)[2]//@href').extract_first(),
                # '/token/{token_address}?a={holder_address}'
                amount = item.xpath('(td)[3]//text()').extract_first(),
                # 2,309,748,407.959
                percentage = item.xpath('(td)[4]//text()').extract_first(),
                # 7.1515%
                )
            yield item