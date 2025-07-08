
import json
import csv
import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Cannot fetch data")
        return

    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="product_pod")

    books = []  # List to store book info

    for article in articles:
        title = article.h3.a['title']
        price_text = article.find("p", class_="price_color").text
        currency = price_text[0]
        price = float(price_text[1:])

        books.append({
            "title": title,
            "currency": currency,
            "price": price
        })
    return books

all_books=scrape_books(url)

with open("books.json", "w", encoding="utf-8") as f:
        json.dump(all_books, f,indent=2, ensure_ascii=False)

   
# print(json.dumps(all_books, indent=2))

with open("books.csv","w",encoding="utf-8",newline='') as f:
     writer=csv.DictWriter(f,fieldnames=["title","currency","price"])
     writer.writeheader()
     writer.writerows(all_books)
