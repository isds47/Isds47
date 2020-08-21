import pandas as pd
import get_head as gh
import os
dirname = os.getcwd()
path = os.path.join(dirname, 'chunk1.csv')

urls1 = pd.read_csv(path)


chunk1_head = gh.get_head(urls1['0'],len(urls1['0']))

chunk1_head = pd.DataFrame(data=chunk1_head)
chunk1_head.to_csv("chunk1_head.csv", index=False)