import csv
import time
import json
import requests
from lxml import etree
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')





def scrape_tag_list(lens):
    url = 'https://old.reddit.com/subreddits/'
    headers = {'User-Agent':'Mozilla/5.0 Chrome/47.0.2526.106 Safari/537.36'}
    st = requests.get(url, headers=headers).text
    open("test.html", 'w').write(st)
    page = etree.HTML(st)

    
    driver = webdriver.Chrome(chrome_options=chrome_options)
# url = 'https://old.reddit.com/subreddits/'
    url = 'https://www.baidu.com'
    st = driver.get(url)
    print(st)

# scrape information off of subreddit posts
def scrape_each_tag(subreddit, tab, pl):

    url = 'https://old.reddit.com/r/{0}/{1}'.format(subreddit, tab)
    headers = {'User-Agent':'Mozilla/5.0 Chrome/47.0.2526.106 Safari/537.36'}

    page = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
    attrs = {'class':'thing'}
    
    count = 1
    posts = []

    while count <= pl:
        post_count = 1
        for post in page.findAll('div', attrs=attrs):
            title = post.find('p', class_="title").text
            author = post.find('a', class_='author').text if post.find('a', class_='author') is not None else 'unknown'
            comments = post.find('a', class_='comments').text.split()[0]
            upvotes = post.find('div', attrs={'class': 'score likes'}).text
            downvotes = post.find('div', attrs={'class': 'score dislikes'}).text

            if comments == 'comment' : comments = 0

            post_data = {
                'page' : count,
                'post' : post_count,
                'title' : title,
                'author' : author,
                'comments' : comments,
                'upvotes' : upvotes,
                'downvotes' : downvotes
            }

            posts.append(post_data)

            post_count+=1

        count+=1

        # pagination
        next_button = page.find('span', class_='next-button')
        next_page_link = next_button.find('a').attrs['href']
        time.sleep(2)
        next_page = requests.get(next_page_link, headers=headers)
        page = BeautifulSoup(next_page.text, 'html.parser')

    # write everything to file
    with open('%s.json' % subreddit, 'a') as outfile:
        json.dump(posts, outfile, sort_keys=True, indent=4)

# if __name__ == '__main__':
#     # scrape(subreddit='vmware', tab='new', pl=100)
#     scrape_tag_list(10)

