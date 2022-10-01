from bs4 import BeautifulSoup as Soup
import html2text
from selenium import webdriver
import undetected_chromedriver as uc
from random import randint
import re
import time

urls = []
whole_story = []
root_url = "https://fanfiction.net"


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
            if len(urls):
                get_story(soup)
            else:
                get_story_urls(soup)



def get_story_urls(soup):
    inner_content = soup.find('div', id='content_wrapper_inner')
    page_urls = inner_content.find_all('div', class_='z-list zhover zpointer')
    for url in page_urls:
        page_url = root_url + url.find('a', class_='stitle').get('href')
        urls.append(page_url)
    for url in urls:
        scrape_page(url)

def get_story(soup):
    story = soup.find(id='storytext')
    adverts = story.find('div')
    if adverts:
        for advert in story.find_all('div'):
            advert.replace_with('')
    chaptered = soup.find('select', id='chap_select')
    story = story.decode_contents()
    if chaptered:
        span = soup.find('span', {'style': 'float:right; '})
        next_c = span.find_all('button')[-1]
        chapter_title = soup.find('option', {'selected': True}).text
        chapter = f'<p>{chapter_title}<p>{story}'
        if next_c.get_text() == 'Next >':
            whole_story.append(chapter)
            next_chapter_url = next_c.get('onclick')[14:].strip("''")
            scrape_page(root_url + next_chapter_url)
        else:
            whole_story.append(chapter)
            joined_story = ''.join(whole_story)
            get_metadata(soup, joined_story)
    else:
        get_metadata(soup, story)


def get_metadata(soup, story):
    story_info = soup.find("span", class_="xgray xcontrast_txt").text
    story_data = story_info.split('-')
    top_data = soup.find_all("a", class_="xcontrast_txt")
    metadata = {
        "Fandom": top_data[1].text,
        "Title": soup.find("b", class_="xcontrast_txt").text,
        "Author": top_data[2].text,
        "Author ID": int(re.search(r"var userid = (.*);", str(soup)).groups()[0]),
        "Publisher": root_url,
        "Story URL": "https:" + soup.find("title").find_previous_sibling().get('href'),
        "Author URL": root_url + top_data[2].get('href'),
        "Story Data": story_data,
        "Summary": soup.find("div", class_="xcontrast_txt").text,
        "Story": html2text.html2text(story)
    }
    get_txt(metadata)


def get_txt(metadata):
    with open(f'{metadata["Title"]} By {metadata["Author"]}.txt', 'w') as f:
        for data in metadata:
            f.write("'{}':'{}'\n".format(data, metadata[data]))


scrape_page('')

