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
data = pd.read_csv('no_words.csv')
data = data[data['title'].notna()]
data = data.reset_index()

data['set'] = 'hi'

data['set'][:1000] = 'test'
data['set'][1000:2000] = 'train'

df_train = data[data.set=="train"]
df_test = data[data.set=="test"]
lambdas = np.logspace(-4, 4, 10)

pipeline_las = Pipeline([
    ('vect', CountVectorizer()),
    #('tfidf', TfidfTransformer()),
    ('pol', PolynomialFeatures(include_bias=True)),
    ('las', Lasso(random_state=1, max_iter=10000))
    #('clf', LinearRegression())
    #('stanscal', RobustScaler(with_centering=False))
])
pipeline_las.get_params().keys()

param_grid_las = {'pol__degree': [1,2,3],
                'las__alpha': lambdas}

search_las = GridSearchCV(pipeline_las, param_grid_las, scoring='neg_mean_squared_error', cv=3, verbose=10, n_jobs = 12)

search_las.fit(df_train.proc_title.values, df_train.comments.values)

print('Best parameter set: %s ' % search_las.best_params_)
print('Best mse: %s ' % search_las.best_score_)

train_preds_las = search_las.predict(df_train.title.values)
test_preds_las = search_las.predict(df_test.title.values)
print("training accuracy:", np.mean([(np.round(train_preds_las,0)==df_train.comments.values)]))
print("testing accuracy:", np.mean([(np.round(test_preds_las,0)==df_test.comments.values)]))

joblib.dump(search_las, 'cloud_las.pkl')