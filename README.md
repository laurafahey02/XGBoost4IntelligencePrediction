# XGBoost4IntelligencePrediction

This repository contains the main scipts used for the second project of my PhD thesis entitled "Comparing the XGBoost machine learning algorithm to polygenic scoring for the prediction of intelligence based on genotype data". Methods will be described in upcoming paper.

Note that hyperparamter optimisation was performed using 3-fold cross validation (CV) and a semi-manual stepwise method. This method was chosen because of it being efficient in terms of time and memory; in part because it meant each CV fold could be run on a different node of the high-performance compute cluster, allowing access to the memory on three nodes and enabling the running of each CV fold in parallel across the three nodes. Therefore, the scripts in the cv1 directory were in reality copied and run for each CV in two more directories.

