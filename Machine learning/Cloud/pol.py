#!/usr/bin/python3
import numpy as np 
import pandas as pd 
from math import sqrt

# similarity/distance measures
from scipy.spatial import distance
from sklearn.metrics.pairwise import linear_kernel
import joblib

# vect
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

# sklearn
from sklearn.svm import LinearSVC
from sklearn.exceptions import DataConversionWarning; import warnings
from sklearn.linear_model import Lasso, LinearRegression, Ridge, ElasticNet, LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.datasets import make_classification
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest, chi2, f_classif
from sklearn.model_selection import GridSearchCV


# load data
data = pd.read_csv('part2.csv')
data = data[data['title'].notna()]
data = data.reset_index()
print(len(data))
data['set'] = 'hi'

data['x_cat'] = data['url'].str.replace('https://ekstrabladet.dk/nyheder/','')
data['x_cat'] = data['x_cat'].str.replace('https://ekstrabladet.dk/','')
data['x_cat'] = data['x_cat'].apply(lambda x: x.split('/')[0])

len_title = []
for i in data['title']:
    len_title.append(len(i))
data['len_title'] = pd.DataFrame(data=len_title)

n = len(data['set'])
if n%2 !=0:
    n -= 1
n1 = int(n/2)

data['set'][:n1] = 'test'
data['set'][n1:n] = 'train'

df_train = data[data.set=="train"]
df_test = data[data.set=="test"]
lambdas = np.logspace(-4, 4, 10)

pipeline_ols = Pipeline([
    ('vect', CountVectorizer()),
    #('tfidf', TfidfTransformer()),
    ('pol', PolynomialFeatures(include_bias=True)),
    ('clf', LinearRegression()),
])

param_grid_ols = {
    "vect__ngram_range": [(1,1), (1,2), (1,3), (1,4)],
             #"tfidf__use_idf": [True, False]
            'pol__degree': [1,2,3]
             }

search_ols = GridSearchCV(pipeline_ols, param_grid_ols, scoring='neg_mean_squared_error', cv=3, verbose=10, n_jobs = -1)

search_ols.fit(df_train.x_cat.values, df_train.comments.values)
#search_ols.fit(df_train.x_cat.values.reshape(-1,1), df_train.comments.values)

print('Best parameter set: %s ' % search_ols.best_params_)
print('Best mse: %s ' % search_ols.best_score_)

train_preds_ols = search_ols.predict(df_train.x_cat.values.reshape(-1,1))
test_preds_ols = search_ols.predict(df_test.x_cat.values.reshape(-1,1))
print('mse = ' + str(mse(df_test.comments.values, test_preds_ols)))
print("training accuracy:", np.mean([(np.round(train_preds_ols,0)==df_train.comments.values)]))
print("testing accuracy:", np.mean([(np.round(test_preds_ols,0)==df_test.comments.values)]))

joblib.dump(search_ols, 'cloud_ols.pkl')