# Part 1: Reddit (HTML to MongoDB)
# see Jupyter Notebook for verbose version

import re
import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient

# Source Reddit
posts = []
url = "http://reddit.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
html = requests.get(url, headers=headers).text
parser = bs(html)

# Destination MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.reddit
db.posts.drop()
collection = db.posts

# Find comments <span> element; it is the only elements all posts have in common
comments = parser.find_all("span", text=re.compile(".*comments"))

# Get the parent post from the comment and scrape the data
for comment in comments:
    post = comment.parent.parent.parent.parent
    # skip sponsored  or pinned content
    if len(post.find_all("span", text="promoted")) > 0 \
        or len(post.find_all("span", text="pinned by moderators")):
        continue
    # get post data
    post_data = {}
    post_data["title"] = post.find_all("h3")[0].text
    post_data["link"] = post.find_all("h3")[0].parent.parent["href"]
    post_data["age"] =" ".join(post.find_all("a", text=re.compile(".*ago"))[0].text.split(" ")[0:2])
    post_data["comments"] = post.find_all("span", text=re.compile(".*comments"))[0].text.split(" ")[0]
    post_data["subreddit"] = "Main Page / " + post.find_all("h3")[0].parent.parent["href"].split('/')[2]
    posts.append(post_data)

# Let's also scrape some of the more interesting subreddits
subreddits = ["science", "technology", "programming", "AskReddit", "news"]

# Get the parent post from the comment and scrape the data
for reddit in subreddits:
    # go to subreddit
    url = "http://reddit.com/r/" + reddit
    html = requests.get(url, headers=headers).text
    parser = bs(html)
    # get comments <span>
    comments = parser.find_all("span", text=re.compile(".*comments"))
    # get parent post and scrape data
    for comment in comments:
        post = comment.parent.parent.parent.parent
        # skip sponsored or pinned content
        if len(post.find_all("span", text="promoted")) > 0 \
            or len(post.find_all("span", text="pinned by moderators")):
            continue
        # get post data
        post_data = {}
        post_data["title"] = post.find_all("h3")[0].text
        post_data["link"] = post.find_all("h3")[0].parent.parent["href"]
        post_data["age"] =" ".join(post.find_all("a", text=re.compile(".*ago"))[0].text.split(" ")[0:2])
        post_data["comments"] = post.find_all("span", text=re.compile(".*comments"))[0].text.split(" ")[0]
        post_data["subreddit"] = post.find_all("h3")[0].parent.parent["href"].split('/')[2]
        posts.append(post_data)

# Put all collected posts into MongoDB
for post in posts:
    collection.insert_one(post)

# Close database connection
client.close()