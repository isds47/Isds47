## Scraping the data
How the data was scraped:

- All urls to the articles are collected in the scraping.ipynb
- The urls are split into 4 chunks and scraped separately in the folder bots.
- we use connector to save the logs (thank you Snorre Ralund!)
- get_head.py starts a chromedriver and scrapes the given urls for headlines, body text, date, and amount of comments.
- the bots folder can split up the urls into chunks and scrape them seperately, more info about the process in that folder.
- the scraped data is then processed in scraping.ipynb