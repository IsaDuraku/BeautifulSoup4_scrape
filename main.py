from bs4 import BeautifulSoup
import requests
import time
# import csv

#To scrape local file!!
# with open('home.html','r') as html_file:
#     content = html_file.read()
#
#     soup = BeautifulSoup(content,'lxml')
#     # #print(soup.prettify())
#     # courses_html_tags = soup.find_all('h5')
#     # for course in courses_html_tags:
#     #     print(course.text)#mashallah
#
#     course_cards = soup.find_all('div', class_='course-card') #dont forget to add _
#     for course in course_cards:
#         course_name = course.h5.text
#         course_price = course.a.text.split()[-1]
#
#         print(f"The price of {course_name} is {course_price}")

#To scrape website!
print('Put some skill that you are not familiar with: ')
Job_title = input('>')
print(f'Filtering out {Job_title}')

def find_jobs():
    html_text = requests.get('https://kosovajob.com/').text
    soup = BeautifulSoup(html_text, 'lxml')
    texts = soup.find_all('div', class_='jobListCnts jobListPrm')
    with open('posts/job.txt', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Puna me titull", "Qytetin", "Koha e mbetur e shpalljes edhe", "More_info"])
        for index, text in enumerate(texts):
            city = text.find('div', class_='jobListCity').text.replace(' ', '')

            if 'Prishtinë' in city:
                title = text.find('div', class_='jobListTitle').text.replace(' ', '')
                date = text.find('div', class_='jobListExpires').text  # .span.text nese ish kon span bllok
                more_info = text.a['href'] #normal ne tutorial u kon text.div.a po kosovaJob qeshtu pe qet linkun

                if Job_title in title:
                    # with open(f'posts/{index}.txt', 'w') as f:
                    #     f.write(f"Puna me titull: {title} ne qytetin {city} koha e mbetur e shpalljes edhe: {date}\n")
                    #     f.write(f"More info: {more_info}")
                    writer.writerow([title, city, date, more_info])
                    print(f"Job saved: {title} - {city} - {date} - {more_info}")
                    print(f"File saves: {index}")




if __name__ =='__main__':
    while True:
        find_jobs()
        time_wait= 600#every so seconds run the function again
        print(f"Waiting {time_wait} seconds")
        time.sleep(time_wait)


#With fakeUser_agents scrapeing
# URL = 'https://stackoverflow.com/questions/62303739/beautiful-soup-returning'
# from fake_useragent import UserAgent
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
# ua=UserAgent()
# hdr = {'User-Agent': ua.random,
#       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
#       'Accept-Encoding': 'none',
#       'Accept-Language': 'en-US,en;q=0.8',
#       'Connection': 'keep-alive'}
# source = requests.get(URL,headers=hdr)
#
# soup = BeautifulSoup(source.text, features="lxml")
# text = soup.findAll('div', class_= 's-prose js-post-body')
# code = text.find('code',class_='hljs language-python').text
#
# # company_description = soup.find_all('div', class_ = 'description__ce057c5c')
# print(text)
# # print(company_description)\

