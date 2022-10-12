from bs4 import BeautifulSoup
import requests
from csv import writer

url= "https://www.pararius.com/apartments/amsterdam?ac=1"
page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')
lists = soup.find_all('section', class_="listing-search-item")

all_info=[]


for list in lists:
    title = list.find('a', class_="listing-search-item__link--title").text.replace('\n', '')
    location = list.find('li', class_="illustrated-features__item--surface-area").text.replace('\n', '')
    price = list.find('div', class_="listing-search-item__price").text.replace('\n', '')
    area = list.find('li', class_="illustrated-features__item--number-of-rooms").text.replace('\n', '')
    info = [title,location, price,area]
    all_info.append(info)
   

print(all_info)
