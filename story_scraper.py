import datetime
from datetime import datetime
import undetected_chromedriver as uc
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
import time
import re

whole_story = []
root_url = "https://fanfiction.net"


def scrape_story(url):
    if __name__ == "__main__":
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        wd = uc.Chrome(options=options)
        wd.get(url)
        time.sleep(5)
        try:
            html_page = wd.page_source
            soup = Soup(html_page, 'html.parser')
        finally:
            wd.quit()
            get_story(soup)


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
            scrape_story(root_url + next_chapter_url)
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
    }
    if 'Story' not in metadata:
        metadata['Story'] = story
    get_txt(metadata)


def get_txt(metadata):
    with open(f'{metadata["Title"]} By {metadata["Author"]}.txt', 'w') as f:
        f.write(f'{metadata}')


scrape_story('')

