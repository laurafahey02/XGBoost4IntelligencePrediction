#!/usr/bin/env python

import sys
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
import xgboost as xgb
from joblib import dump, load

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

# Open output file

f=open(output_file_name, "w")

# # 3. Run the model

params = {'colsample_bytree': 0.5,'colsample_bylevel':0.5, 'colsample_bynode':0.5,
 'learning_rate': 0.01,
 'max_depth': 12,
 'min_child_weight': 150,
 'n_estimators': 23493,
 'subsample': 0.5,
 'gamma': 0.2}

xg_class = XGBClassifier(seed=123, missing=9, tree_method="exact", n_jobs=-1, **params)

xg_class.fit(snps,samples,verbose=True)

y_pred = xg_class.predict(test_snps)

# # 4. Assess accuracy and get AUC score

# Compute predicted probabilities: y_pred_prob
y_pred_prob = xg_class.predict_proba(test_snps)[:,1]
# Compute and print AUC score
f.write("AUC\n: {}".format(roc_auc_score(test_samples, y_pred_prob)))
f.write("Accuracy: {}\n".format(accuracy_score(test_samples, y_pred)))

# Save model

dump(xg_class, 'xg_class.joblib')

# Get feature importance scores

bst = xg_class.get_booster()

with open('feature_importance.txt', 'w') as fI:
    for importance_type in ('weight', 'gain', 'cover', 'total_gain', 'total_cover'):
        print("%s: " % importance_type, bst.get_score(importance_type=importance_type), file=fI)

# Plot tree
node_params = {'shape': 'box',
              'style':'filled, rounded',
              'fillcolor': '#7CB9E8'}

leaf_params = {'shape': 'box',
              'style': 'filled',
              'fillcolor': '#ffd242'}

# Plot tree number 18000
graph_data = xgb.to_graphviz(xg_class, num_trees=18000, size="10,10",
               condition_node_params=node_params,
               leaf_node_params=leaf_params)

graph_data.view(filename='xgb_tree')

# Investigate tree complexity by counting splits

trees_strings = bst.get_dump(dump_format='text')
total_splits = 0
for tree_string in trees_strings:
        n_nodes = len(tree_string.split('\n')) - 1
        n_leaves = tree_string.count('leaf')
        total_splits += n_nodes - n_leaves
f.write("Total Splits: %s" % total_splits)

# Close output file
f.close()
