## Machine Learning

- The -all-words ipynb runs on the whole dataset while the other runs on the dateset containing only high frequency words.
- The Modelvalidation.ipynb runs models without gridsearchCV we ended up not using it in favour of gridsearchCV.
- it is possible to run the models on a google cloud server by adjusting the .py files in the cloud folder and uploading to the server.

### Gridsearch
- 3 models
    1. OLS
    2. LASSO
    3. Elastic net
- saves the results from the 3 models and creates validation curves, learning curves and calculates the accuracy.
