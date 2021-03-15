import scrapy

from scrapy.loader import ItemLoader

from ..items import KhhuItem
from itemloaders.processors import TakeFirst


class KhhuSpider(scrapy.Spider):
	name = 'khhu'
	start_urls = ['https://www.kh.hu/csoport/sajto']

	def parse(self, response):
		post_links = response.xpath('//*[(@id = "_pressnewsportlet_WAR_pressnewsportlet_ocerSearchContainerSearchContainer")]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//ul[@class="lfr-pagination-buttons pager"]/li[3]/a/@href').getall()
		print(next_page)
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="wrap"]/h1/text()').get()
		description = response.xpath('//div[@class="news-content wrap"]//text()[normalize-space()]|//div[@class="news-lead"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//time/text()').get()

		item = ItemLoader(item=KhhuItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
