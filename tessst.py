import requests
from bs4 import BeautifulSoup

#This works and its saves the livestream links into database linkdb
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


def get_a_links(url):
    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Initialize a list to store <a> links
        a_links = []

        # Find the <article> element
        article = soup.find('body')

        if article:
            # Find all <div> elements inside the <article>
            div_elements = article.find_all('tr')

            for div in div_elements:
                # Find all <a> elements inside the <div>
                a_elements = div.find_all('a', href=True)

                for a in a_elements:
                    href = a['href']
                    a_links.append(href)

        return a_links


if __name__ == '__main__':
    website_url = 'https://freestreams-live1.se/football-streamz5/'  # Replace with the website you want to scrape
    a_links = get_a_links(website_url)

    if a_links:
        for a_link in a_links:
            # print("Found <a> link:", a_link)

            # Search for iframe links inside the <a> link
            iframe_links_inside_a = get_iframe_links(a_link)

            if iframe_links_inside_a:
                for iframe_link in iframe_links_inside_a:
                    print("Found iframe link inside <a>:", iframe_link)
            else:
                print("No iframe links found inside <a>.")
    else:
        print("No <a> links found.")