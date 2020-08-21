import pandas as pd
import get_head as gh
import os

dirname = os.getcwd()
path = os.path.join(dirname, 'chunk2.csv')

urls2 = pd.read_csv(path)


chunk2_head = gh.get_head(urls2['0'],len(urls2['0']))

chunk2_head = pd.DataFrame(data=chunk2_head)
chunk2_head.to_csv("chunk2_head.csv", index=False)