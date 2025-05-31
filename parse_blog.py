# Quick attempt at exploring blog output and how to parse it

import feedparser
# from bs4 import BeautifulSoup

BLOGFILE = "blog-05-30-2025.xml"

# Parse the blogger output file
d = feedparser.parse(BLOGFILE)

# Top level information
print(d.feed.title)
print(len(d.entries))

# Loop over entries for specific posts
for i, entry in enumerate(d.entries):
    # Get the tags used and skip any without Books in it
    tag_list = entry.tags
    tag_list = [
        x.get("term") for x in tag_list if not x.get("term", "").endswith("#post")
    ]
    if "Books" not in tag_list:
        continue

    print(i, entry.title, tag_list)

    # Extra information
    # print(entry.id)
    # print(entry.link)
    # print(entry.published)

    # print(entry.keys())

    # Get text without any HTML
    # soup = BeautifulSoup(entry.summary, "html.parser")
    # print(soup.text)
