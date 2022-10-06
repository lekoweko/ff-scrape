from selenium import webdriver
import undetected_chromedriver as uc
from bs4 import BeautifulSoup as Soup
import re
from random import randint
import time
import html2text

'''

Returns txt files for an author's reviews. To use, insert the author's URL(str) into scrape_author_reviews. 
Example: scrape_author_reviews('https://www.fanfiction.net/u/<author-id>/')

Chapter: Chapter the review was left on
Date:  Date of the review
Username: Username
User ID: User ID or None if a guest left a review. 
Review: The review text

'''

reviews = []
review_urls = []
root_url = 'https://www.fanfiction.net'


def scrape_author_urls(author_url):
    if __name__ == "__main__":
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        wd = uc.Chrome(options=options)
        wd.get(author_url)
        wait = randint(5, 7)
        time.sleep(wait)
        try:
            html_page = wd.page_source
            author_soup = Soup(html_page, 'html.parser')
        finally:
            wd.quit()
            get_author_urls(author_soup)


def get_author_urls(author_soup):
    author_story_page = author_soup.find(id='st')
    review_links = author_story_page.find_all(class_='reviews')
    for review_link in review_links:
        link = root_url + review_link.get('href')
        review_urls.append(link)
    scrape_all_review(review_urls)


def scrape_all_review(review_urls):
    for url in review_urls:
        scrape_page(url)


def scrape_page(url):
    if __name__ == "__main__":
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        wd = uc.Chrome(options=options)
        wd.get(url)
        wait = randint(5, 7)
        time.sleep(wait)
        try:
            html_page = wd.page_source
            soup = Soup(html_page, 'html.parser')
        finally:
            wd.quit()
            get_reviews(soup)


# get reviews
def get_reviews(soup):
    reviews_table = soup.find(class_='table-striped').tbody
    reviews_tds = reviews_table.find_all('td')
    for review_td in reviews_tds:
        match = re.search(r'href="/u/(.*)/.*">(.*)</a>', str(review_td))
        if match is not None:
            user_id = int(match.groups()[0])
            user_name = str(match.groups()[1])
        else:
            user_id = None
            user_name = str(review_td.find('small').previous_sibling)
        chapter_and_date = review_td.find('small').get_text()
        review = {
            'chapter': chapter_and_date.split('.')[0],
            'date': chapter_and_date.split('.')[1],
            'user_name': user_name,
            'user_id': user_id,
            'text': html2text.html2text(review_td.div.text)
        }
        reviews.append(review)
    center = soup.find('center')
    thead = soup.find(class_='thead')
    title = thead.find_all('a')[-1].get_text()
    if center:
        if 'b' in str(center.contents[-1]):
            # return(title, reviews)
            create_txt_file(title, reviews)
        else:
            next_page = center.b.next_sibling.next_sibling.get('href')
            scrape_page(root_url + next_page)
    else:
        # return(title, reviews)
        create_txt_file(title, reviews)


def create_txt_file(title, reviews):
    with open(f'Reviews for {title}.txt', 'w', newline='') as f:
        for review in reviews:
            review_text = str(review["text"]).replace('b', '', 1)
            f.write(f'Chapter: {review["chapter"]}\n')
            f.write(f'Date: {review["date"]}\n')
            f.write(f'Username: {review["user_name"]}\n')
            f.write(f'User ID: {review["user_id"]}\n')
            f.write(f'Review: {review_text}\n\n')
    reviews.clear()

def scrape_author_reviews(author_url):
    scrape_author_urls(author_url)


scrape_author_reviews('')


