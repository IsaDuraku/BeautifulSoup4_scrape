from bs4 import BeautifulSoup
import requests
import time
import csv

print('Put some skill that you are not familiar with: ')
Job_title = input('>')
print(f'Filtering out {Job_title}')

# Open the file before the loop
with open('posts/job.txt', 'w') as file:
    writer = (file)
    writer.writerow(["Puna me titull", "Qytetin", "Koha e mbetur e shpalljes edhe", "More_info"])

    def find_jobs():
        html_text = requests.get('https://kosovajob.com/').text
        soup = BeautifulSoup(html_text, 'lxml')
        texts = soup.find_all('div', class_='jobListCnts jobListPrm')
        for index, text in enumerate(texts):
            city = text.find('div', class_='jobListCity').text.replace(' ', '')

            if 'Prishtinë' in city:
                title = text.find('div', class_='jobListTitle').text.replace(' ', '')
                date = text.find('div', class_='jobListExpires').text
                more_info = text.a['href']

                if Job_title in title:
                    writer.writerow([title, city, date, more_info])
                    print(f"Job saved: {title} - {city} - {date} - {more_info}")

    if __name__ == '__main__':
        while True:
            find_jobs()
            time_wait = 10
            print(f"Waiting {time_wait} seconds")
            time.sleep(time_wait)