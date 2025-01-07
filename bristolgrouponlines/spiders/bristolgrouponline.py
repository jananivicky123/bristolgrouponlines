from scrapy import Request
from scrapy import Spider

class BristolgrouponlineSpider(Spider):
    name = "bristolgrouponline"
    allowed_domains = ["bristolgrouponline.com"]
    start_urls = ["https://www.bristolgrouponline.com/buy-a-business/"]

    def parse(self, response):
        listings = response.xpath('//*[@class="stretched-link"]/@href').extract()
        for listing in listings:
            abs_listing = f"https://www.bristolgrouponline.com{listing}"
            yield Request(abs_listing,callback = self.parse_listing)

            next_page = response.xpath('//*[@aria-label="Next"]/@href').get()
            abs_next_page = f"https://www.bristolgrouponline.com{next_page}"
            yield Request(abs_next_page,callback = self.parse)

    def parse_listing(self, response):
        listing_url = response.url
        listing_Name = response.xpath('//h1/text()').get()
        city_state = response.xpath('//h3[@class="city-state"]/text()').get()
        description = response.xpath('//h2[contains(.,"Overview")]/following-sibling::p/text()').get()
        asking_Price = response.xpath('//*[@class="row-details"]/text()').get()
        revenue = response.xpath('//*[@class="row-details"]/following-sibling::div/text()').get()
        cash_flow = response.xpath('//*[@class="block-1 result-details"]/div[@class="row-details"][last()]/text()').get()
        broker_name = response.xpath('//li[@class="name"]/text()').get()
        broker_company = response.xpath('//*[@class="office-location"]//li//text()').extract()
        broker_email = response.xpath('//*[@class="email"]/a/@href').get()
        broker_phone = response.xpath('//*[@class="phone"]/text()').get()
        listing_id = response.xpath('//h3[@class="listing-id"]/text()').get()
        reason_for_sale = response.xpath('//h2[contains(.,"Reason for Selling:")]/following-sibling::div/text()').get()
        year_established = response.xpath('//h2[contains(.,"Established:")]/following-sibling::div/text()').get()
        full_time_employees = response.xpath('//h2[contains(.,"Employees:")]/following-sibling::div/text()').get()
        adjusted_EBITDA = ''

        data = {
            "listing_url":listing_url,
            "listing_Name":listing_Name,
            "city_state":city_state,
            "description":description,
            "asking_Price":asking_Price,
            "revenue":revenue,
            "cash_flow":cash_flow,
            "broker_name":broker_name,
            "broker_company":broker_company,
            "broker_email":broker_email,
            "broker_phone":broker_phone,
            "listing_id":listing_id,
            "reason_for_sale":reason_for_sale,
            "year_established":year_established,
            "full_time_employees":full_time_employees,
            "adjusted_EBITDA":adjusted_EBITDA}

        yield data
        
