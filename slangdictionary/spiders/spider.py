# Slang extractor
response.xpath('.//div[@class="term featured"]//h2//a[contains(@href, "/meaning-definition")]/text()').extract()

# Definitions extractor
response.xpath('.//div[@class="definitions"]//ul//li[.//blockquote]/text()[normalize-space()]').extract()
