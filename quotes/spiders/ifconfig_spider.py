import scrapy
import logging

class IfconfigSpider(scrapy.Spider):
    name = "ifconfig"
    allowed_domains = ["ifconfig.me"]
    start_urls = ["https://ifconfig.me/"]

    def parse(self, response):
        with open('./output.txt', mode = 'a', encoding = 'utf-8') as f:

            f.write('ifconfig reported IP : %s\n' % response.css('#ip_address').get())
