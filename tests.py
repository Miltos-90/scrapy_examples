# Definitions extractor
#x = './/div[@class="definitions"]/ul/li/text()[normalize-space()]|.//div[@class="definitions"]/ul/li/a/text()[normalize-space()]'
#response.xpath(x).extract()


# Extractor of the inner hyperlink pointing to another slang abbreviation
# If empty, the webpage does not point to another page. If not empty, it must be followed (it contaisn the definitions)
#response.xpath('.//div[@class="definitions"]//ul//li[.//blockquote]/a/@href').extract()


# this is the definition extractor. Could be shortened if scrapy supported xpath 2.0
x = """
.//div[@class="definitions"]/ul/li/text()[normalize-space()]
|
.//div[@class="definitions"]/ul/li/a/text()[normalize-space()]
"""
response.xpath(x).extract()

"""
The definitions can be one or more of the following two:
(I)  The concatenated text of li with the text of a that contains an href "/meaning-definition-of/..." inside it
(II) The text of li (only) if it does not contain a

"""

# Extract (I)
x = """
concat(
.//div[@class="definitions"]/ul/li[a[contains(@href, "/meaning-definition-of/")]]/text()[normalize-space()],
.//div[@class="definitions"]/ul/li/a/text()[normalize-space()]
)
"""
response.xpath(x).extract()

# Extract (II)
x = """
.//div[@class="definitions"]/ul/li[not(a)]/text()[normalize-space()]
"""
response.xpath(x).extract()

