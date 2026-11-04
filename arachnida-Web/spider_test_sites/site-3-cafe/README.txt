# Little Pixel Cafe test site

This is a small local website for testing your Spider.

Pages:
- index.html (start here)
- menu.html, story.html, gallery.html

Run a local server from this directory:
    python3 -m http.server 8000

Then visit:
    http://localhost:8000/

Try:
    ./spider.py http://localhost:8000/
    ./spider.py -r -l 1 http://localhost:8000/
    ./spider.py -r -l 2 http://localhost:8000/

Expected crawl depth (starting page counts as depth 0):
- depth 0: index.html only
- depth 1: index.html plus its direct links
- depth 2: pages linked from those direct links as well

The pages intentionally contain back-links, so your visited_urls set should prevent repeat visits.
