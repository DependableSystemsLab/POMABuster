# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import string


class ERC20SanitizationPipeline:
    printable = set(string.printable)

    def _clean_name(self, name_list):
        return ' '.join([x for x in name_list if x != '\n'])

    def _clean_string(self, string):
        return ''.join(filter(lambda x: x in self.printable, string))

    def _clean_float(self, string):
        return string.replace(',', '').replace('$', '').replace('\n', '')

    def _clean_address(self, string):
        return string.lstrip('/token/')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['index'] is None:
            raise DropItem(f"Missing index in {item}")

        adapter['name'] = self._clean_name(adapter['name'])
        adapter['market_cap_circulating'] = self._clean_float(self._clean_string(
            adapter['market_cap_circulating']))
        adapter['market_cap_onchain'] = self._clean_float(self._clean_string(
            adapter['market_cap_onchain']))
        adapter['market_cap_fully_diluted'] = self._clean_float(
            adapter['market_cap_fully_diluted'])
        adapter['price_in_usd'] = self._clean_float(adapter['price_in_usd'])
        adapter['holders'] = self._clean_float(adapter['holders'])
        adapter['volume'] = self._clean_float(adapter['volume'])
        adapter['address'] = self._clean_address(adapter['address'])
        adapter['total_supply'] = self._clean_float(adapter['total_supply'])
        adapter['decimals'] = adapter['decimals']

        return item


class HolderSanitizationPipeline:

    def _clean_float(self, string):
        return string.replace(',', '').replace('$', '')

    def _clean_address(self, string):
        return string.split('?a=')[1]

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter['rank'] is None:
            raise DropItem(f"Missing rank in {item}")

        adapter['holder_address'] = self._clean_address(adapter['holder_address'])
        adapter['amount'] = self._clean_float(adapter['amount'])
        adapter['percentage'] = adapter['percentage'].strip('%')

        return item