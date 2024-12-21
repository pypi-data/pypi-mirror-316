import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_urls(base_url):

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a', href=True)


    urls = set()
    for link in links:
        url = link['href']
        full_url = urljoin(base_url, url)
        if base_url in full_url:  
            urls.add(full_url)
    
    return list(urls)

def clone_page(url):

    response = requests.get(url)
    filename = url.replace("https://", "").replace("http://", "").replace("/", "_") + ".html"
    file_path = os.path.join(os.getcwd(), filename)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response.text)
