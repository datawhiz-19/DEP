import requests
from bs4 import BeautifulSoup
import csv

# Base URL of the website
link = 'https://books.toscrape.com/catalogue/page-{}.html'
book_link = 'https://books.toscrape.com/catalogue/'

# List to store book details
books = []

# Function to convert rating text to a number
def Rating_conversion(rating_in_text):
    rating_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }
    return rating_dict.get(rating_in_text, 0)

# Function to extract data from a single page
def data_extraction(soup, page):
    pages = []
    for book in soup.find_all('article', class_='product_pod'):
        title = book.h3.a['title']
        thumbnail_url = 'https://books.toscrape.com/' + book.find('img', class_='thumbnail')['src']
        price = book.find('p', class_='price_color').text.replace("Â","")
        rating_in_text = book.p['class'][1]
        availability = book.find('p', class_='instock availability').text.strip()
        link = book_link + book.h3.a['href']
        rating = Rating_conversion(rating_in_text)
        
        
        book_data = {
            'Title': title,
            'Price': price,
            'Availability': availability,
            'Rating': rating,
            'Link': link,
            'Thumbnail URL': thumbnail_url
        }
        pages.append(book_data)
    return pages

# Fetch data from pages sequentially
for page in range(1, 11):  # Scraping the first 10 pages
    url = link.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    pages = data_extraction(soup, page)
    books.extend(pages)
    print(f"Data Extracted from page # {page}")

# Save the data to a CSV file
with open('books_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=books[0].keys())
    writer.writeheader()
    writer.writerows(books)
print("Data saved to books_data.csv")

#------------
