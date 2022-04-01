#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
from random import sample
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import accuracy_score

# arguments
disc_data = sys.argv[1]
test_data = sys.argv[2]

output_file_name = sys.argv[3]

# # 1. Read in data

data = pd.read_table(disc_data, delimiter=' ')
test = pd.read_table(test_data, delimiter=' ')

# "iloc" in pandas is used to select rows and columns by number, in the order that they appear in the data frame.
snps = data.iloc[:,1:].values.astype(np.int16)
samples = data.iloc[:,0].values.astype(np.int16)

test_snps = test.iloc[:,1:].values.astype(np.int16)
test_samples = test.iloc[:,0].values.astype(np.int16)

# Define parameter grid to search through
list_dict = [{'learning_rate': 0.05, 'max_depth': 50, 'min_child_weight': 10,'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5},
 {'learning_rate': 0.05, 'max_depth': 10, 'min_child_weight': 50,'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5},
 {'learning_rate': 0.05, 'max_depth': 10, 'min_child_weight': 300, 'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5},
 {'learning_rate': 0.05, 'max_depth': 30, 'min_child_weight': 10, 'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5},
 {'learning_rate': 0.05, 'max_depth': 30, 'min_child_weight': 50,'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5},
 {'learning_rate': 0.05, 'max_depth': 30, 'min_child_weight': 300, 'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5},
 {'learning_rate': 0.05, 'max_depth': 10, 'min_child_weight': 10, 'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5},
 {'learning_rate': 0.05, 'max_depth': 50, 'min_child_weight': 50, 'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5},
 {'learning_rate': 0.05, 'max_depth': 50, 'min_child_weight': 300,'n_estimators': 6000, 'subsample': 0.5, 'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5}]

f=open(output_file_name, "w")

def XGB(params, trial):
    xg_class = XGBClassifier(seed=123, missing=9, tree_method="hist", n_jobs=-1, **params)
    xg_class.fit(snps,samples, verbose=True, early_stopping_rounds=800, eval_metric='aucpr',eval_set=[(test_snps,test_samples)])
    y_pred = xg_class.predict(test_snps)
    y_pred_prob = xg_class.predict_proba(test_snps)[:,1]
    f.write("\nTrial: {}".format(trial))
    f.write("\nAUC: {}".format(roc_auc_score(test_samples, y_pred_prob)))
    f.write("Accuracy: {}\n".format(accuracy_score(test_samples, y_pred)))

for x in range(9):
    XGB(list_dict[x], x)

f.close()
