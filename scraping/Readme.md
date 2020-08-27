# Scraping the data
How the data was scraped:

- All urls to the articles are collected in the scraping.ipynb
- The urls are split into 4 chunks and scraped separately in the folder bots.
- get_head.py starts a chromedriver and scrapes the given urls for headlines, body text, date, and amount of comments.
- the run_bots.py scrapes data in the bots folder and runs the scraper on any amount of cores.
- each bot0-3 scrapes data in the respective folder scrapes data on 1 core.
- the scraped data is then processed in scraping.ipynb
