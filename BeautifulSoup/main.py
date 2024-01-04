import urllib3
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient


url = "https://stackoverflow.com/questions?tab=newest&page=1"
#create an instance MongoDB
client = MongoClient('localhost', 27017)
#create a databases if it not exist
db = client['stackoverflow']
#create a collection if it not exist
collection = db['questions']



def scrap_and_store(url: str):
    try:
        r = requests.get(url)

        soup = BeautifulSoup(r.content,'html5lib')
        h3 = soup.find_all('h3', attrs={'class': 's-post-summary--content-title'})

        items = []

        for row in h3:
            item = {}
            item["title"] = row.find('a', {'class': 's-link'}).text
            item['URL'] = row.find('a', {'class': 's-link'})['href']
            
            items.append(item)
        #insert a data 
        collection.insert_many(items)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

def scrape_multiple_pages(pages: list) -> None:
    for page in pages:
        url = f"https://stackoverflow.com/questions?tab=newest&page={page}"
        scrap_and_store(url)

scrap_and_store(url)
