### scraping in chunks.

- each bot scrapes a different chunk of the urls
- run_bots.py can run a different chunk on each core of a pc, but we found this to slow down the pc it runs on a lot.
- get_head.py is the function that scrapes data _multi_core is for the run_bots.py
- we use connector to save the logs (thank you Snorre Ralund!)