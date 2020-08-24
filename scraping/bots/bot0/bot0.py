import pandas as pd
import get_head as gh
import os
dirname = os.getcwd()
path = os.path.join(dirname, 'chunk0.csv')

urls0 = pd.read_csv(path)

chunk0_head = gh.get_head(urls0['0'],len(urls0['0']))
print(chunk0_head)

chunk0_head = pd.DataFrame(data=chunk0_head)
chunk0_head.to_csv("chunk0_head.csv", index=False)