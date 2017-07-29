import scrapy
from yelp_reviews.items import YelpReviewsItem


class ReviewSpider(scrapy.Spider):
    name = "pull_yelp_reviews"
    allowed_domains = ["yelp.com"]
    domain = "https://www.yelp.com/biz/"

    def __init__(self, id=None):
        self.id = id
        self.start_urls = [ self.domain + self.id]


    def parse(self, response):
        next_url = response.xpath('//a[@class="u-decoration-none next pagination-links_anchor"]/@href').extract()[0]

        review_texts = response.xpath('//li/div[@class="review review--with-sidebar"]//div[@class="review-content"]/p').extract()
        review_dates = response.xpath('//li/div[@class="review review--with-sidebar"]//span[@class="rating-qualifier"]/text()').extract()
        user_names = response.xpath('//li/div[@class="review review--with-sidebar"]//a[@class="user-display-name js-analytics-click"]/text()').extract()
        review_scores = response.xpath('//li/div[@class="review review--with-sidebar"]//div[starts-with(@class, "i-stars i-stars--regular")]/@title').extract()

        for i in range(len(review_texts)):
            print i
            yield YelpReviewsItem(id = self.id,
                                  user_name = user_names[i],
                                  review_date = review_dates[i],
                                  review_text = review_texts[i],
                                  review_score = review_scores[i])

        yield scrapy.Request(next_url, callback=self.parse)

