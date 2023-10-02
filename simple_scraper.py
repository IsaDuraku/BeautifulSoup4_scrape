import requests
from bs4 import BeautifulSoup
import re
import psycopg2
from datetime import date

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
        cursor.execute('''CREATE TABLE livestream_links (id serial PRIMARY KEY, time text, event text,url text,date DATE)''')
        conn.commit()
        print("Table 'livestream_links' has been created.")

    # Close the database connection
    conn.close()
create_iframe_links_table()
def process_webpage(url):
    # Send an HTTP GET request to the URL to retrieve the webpage content
    response = requests.get(url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')

        # Find the <body> tag
        body_tag = soup.text.split("\n")[:120] #Split every line individually

        # Initialize a list to store the extracted lines
        extracted_lines = []
        conn = psycopg2.connect(
            database="linkdb",
            user="postgres",  # Replace with your PostgreSQL username
            password="2458",  # Replace with your PostgreSQL password
            host="localhost",  # Replace with your PostgreSQL host
            port="5432"  # Replace with your PostgreSQL port
        )
        current_date = date.today()
        #me dictionary
        if body_tag:
            # Split the text into lines
            lines = body_tag

            # Process each line

            for line in lines:
                # Check if the line starts with a time format and contains both | and -
                if any(time_str in line for time_str in
                       ["00:", "01:", "02:", "03:", "04:", "05:", "06:", "07:", "08:", "09:",
                        "10:", "11:", "12:", "13:", "14:", "15:", "16:", "17:", "18:", "19:",
                        "20:", "21:", "22:", "23:"]) and '|' in line and 'x' in line and "Handball" not in line and "Rugby" not in line:
                    # Split the line at both | and - symbols
                    parts = re.split(r'\t(.*?)\s*\|\s*', line)
                    parts = [p.strip() for p in parts if p.strip()]  # Remove leading/trailing spaces
                    # extracted_lines.append(parts)
                    # Check if there are at least three elements in parts
                    if len(parts) >= 3:
                        line_dict = {
                            "Time": parts[0].strip(),
                            "Event": parts[1].strip(),
                            "URL": parts[2].strip()
                        }

                        line_dict["DATE"] = current_date.strftime('%d-%m-%Y')
                        extracted_lines.append(line_dict)
                    else:
                        print("Skipping line:", line)

                    # Append the dictionary to the list

        cursor = conn.cursor()
        for line_dict in extracted_lines:
            cursor.execute(
                '''INSERT INTO livestream_links (time, event, url,date) VALUES (%s, %s, %s,%s)''',
                (line_dict["Time"], line_dict["Event"], line_dict["URL"],line_dict["DATE"])
            )
        conn.commit()

        # Close the database connection
        conn.close()

        # Print the extracted lines
        for line_dict in extracted_lines:
            print("Line:", line_dict)
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)


if __name__ == '__main__':
    # Input the URL of the webpage you want to process
    webpage_url = 'https://sportsonline.gl/'

    # Call the function to process the webpage
    process_webpage(webpage_url)
