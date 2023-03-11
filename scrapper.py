import requests
from bs4 import BeautifulSoup

class Site():

    def __init__(self, site_link):
        super().__init__()
        self.site_link = site_link

    def getSiteLink(self):
        return self.site_link

    def setSiteLink(self, cityName):
        self.site_link = self.site_link.replace("istanbul", cityName)
        return self.site_link

    def scrapeData(self):
        response = requests.get(self.site_link)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            for cell in cells:
                print(cell.text)
