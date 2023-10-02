import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
def get_iframe_links(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        # Initialize a list to store iframe links
        iframe_links = []

        # Find all <iframe> elements
        iframe_elements = soup.find_all('iframe')
        for iframe in iframe_elements:
            iframe_src = iframe.get('src')
            if iframe_src:
                iframe_links.append(iframe_src)

        return iframe_links

def scrape_and_store_links(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        # Find the body element
        body = soup.find('div', class_='row vlog-posts row-eq-height')

        # Initialize a list to store links
        links = []

        # Find all <tr> elements within the body
        tr_elements = body.find_all('article')

        for a in tr_elements:
            # Find all links within the <tr> element
            tr_links = a.find_all('a', href=True)
            for link in tr_links:
                href = link['href']
                links.append(href)
                print("Found <a> link:", href)  # Print <a> links here

        iframe_links = []
        for link in links:
            iframe_links.extend(get_iframe_links(link))

        if iframe_links:  # Print iframe links
            for iframe_link in iframe_links:
                print("Found iframe link:", iframe_link)
        else:
            print("Found nothing")
if __name__ == '__main__':
    website_url = 'https://footyfull.com/'  # Replace with the website you want to start scraping
    scrape_and_store_links(website_url)

