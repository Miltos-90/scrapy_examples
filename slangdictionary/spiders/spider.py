# Slang extractor
#response.xpath('.//div[contains(@class,"term")]//h2//a[contains(@href, "/meaning-definition")]/text()').extract()

# Definitions extractor
#x = './/div[@class="definitions"]/ul/li/text()[normalize-space()]|.//div[@class="definitions"]/ul/li/a/text()[normalize-space()]'
#response.xpath(x).extract()


# Extractor of the inner hyperlink pointing to another slang abbreviation
# If empty, the webpage does not point to another page. If not empty, it must be followed (it contaisn the definitions)
#response.xpath('.//div[@class="definitions"]//ul//li[.//blockquote]/a/@href').extract()

x = './/div[@class="definitions"]/ul/li/text()[normalize-space()]|.//div[@class="definitions"]/ul/li/a/text()[normalize-space()]'
response.xpath(x).extract()


# this is the definition extractor. Could be shortened if scrapy supported xpath 2.0
x = './/div[@class="definitions"]/ul/li/a/text()[normalize-space()]|.//div[@class="definitions"]/ul/li[not(a)]/text()[normalize-space()]'
response.xpath(x).extract()
