import pandas as pd
import get_head as gh
import os

dirname = os.getcwd()
path = os.path.join(dirname, 'chunk3.csv')

urls3 = pd.read_csv(path)

chunk3_head = gh.get_head(urls3['0'],len(urls3['0']))

chunk3_head = pd.DataFrame(data=chunk3_head)
chunk3_head.to_csv("chunk3_head.csv", index=False)