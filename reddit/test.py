import csv
import time
import json
import requests
from bs4 import BeautifulSoup

# scrape information off of subreddit posts
def scrape(subreddit, tab, pl):

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

if __name__ == '__main__':
    scrape(subreddit='Gotham', tab='new', pl=10)