import scrapy; import json
#scrapy crawl ntschool -o schools.csv
#https://www.youtube.com/watch?v=Pu3gmdWsLYc

class NtschoolSpider(scrapy.Spider):
    name = "ntschool"
    start_urls = ["https://directory.ntschools.net/#/schools"]
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9,hi;q=0.8,lb;q=0.7",
        "Referer": "https://directory.ntschools.net/",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "X-Requested-With": "Fetch",
    }

    def parse(self, response):
        yield scrapy.Request(
            url="https://directory.ntschools.net/api/System/GetAllSchools",
            callback=self.parse_api,
            headers=self.headers
        )

    def parse_api(self, response):
        base_url = 'https://directory.ntschools.net/api/System/GetSchool?itSchoolCode='

        data = response.json()
        for school in data:
            school_code = school['itSchoolCode']
            school_url = base_url + school_code
            request = scrapy.Request(
                url=school_url,
                callback=self.parse_school,
                headers=self.headers,
                dont_filter=True # Many schools have the same code, same page, but listed more than once
            )
            yield request
    
    def parse_school(self, response):
        data = response.json()

        yield {
            "name": data["name"],
            "telephoneNumber": data["telephoneNumber"],
            "mail": data["mail"],
            "physicalAddress": data["physicalAddress"]["displayAddress"],
            "postalAddress": data["postalAddress"]["displayAddress"],
        }


