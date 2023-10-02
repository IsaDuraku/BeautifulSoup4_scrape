import requests
from bs4 import BeautifulSoup
import psycopg2


def create_iframe_links_table():
    # Create a PostgreSQL table to store iframe links
    conn = psycopg2.connect(
        database="linkdb",
        user="postgres",  # Replace with your PostgreSQL username
        password="2458",  # Replace with your PostgreSQL password
        host="localhost",  # Replace with your PostgreSQL host
        port="5432"  # Replace with your PostgreSQL port
    )
    cursor = conn.cursor()

    cursor.execute('''SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'livestream_links')''')
    table_exists = cursor.fetchone()[0]

    if table_exists:
        # If the table exists, delete all data in it
        cursor.execute('''DELETE FROM livestream_links''')
        conn.commit()
        print("Table 'livestream_links' exists and all data has been deleted.")
    else:
        # If the table doesn't exist, create it
        cursor.execute('''CREATE TABLE livestream_links (id serial PRIMARY KEY, url text)''')
        conn.commit()
        print("Table 'livestream_links' has been created.")

    # Close the database connection
    conn.close()
create_iframe_links_table()
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

                conn = psycopg2.connect(
                    database="linkdb",
                    user="postgres",  # Replace with your PostgreSQL username
                    password="2458",  # Replace with your PostgreSQL password
                    host="localhost",  # Replace with your PostgreSQL host
                    port="5432"  # Replace with your PostgreSQL port
                )
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO livestream_links (time, event, url) VALUES (%s, %s, %s)''', (iframe_src,))
                conn.commit()
                conn.close()
        return iframe_links

def scrape_and_store_links(url):

    # Fetch the webpage content
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'lxml')

        # Find the body element
        body = soup.find('body')

        # Initialize a list to store links
        links = []

        # Find all <tr> elements within the body
        tr_elements = body.find_all('tr')

        for tr in tr_elements:
            # Find all links within the <tr> element
            tr_links = tr.find_all('a', href=True)
            for link in tr_links:
                href = link['href']
                links.append(href)


        # Open the links and search for iframes
        iframe_links = []
        for link in links:
            iframe_links.extend(get_iframe_links(link))

        # Print iframe links
        if iframe_links:
            for iframe_link in iframe_links:
                print("Found iframe link:", iframe_link)
        else:
            print("found nothing")

if __name__ == '__main__':
    website_url = 'https://freestreams-live1.se/football-streamz5/'  # Replace with the website you want to start scraping
    scrape_and_store_links(website_url)