# XGBoost4IntelligencePrediction

This repository contains the main scipts used to predict an intellegice phenotype based on genotype data for 57,558 samples (post quality control). This study is descibed in the preprint, [Comparing the XGBoost machine learning algorithm to polygenic scoring for the prediction of intelligence based on genotype data](https://www.biorxiv.org/content/10.1101/2022.06.12.495467v1).

The workflow used is visualised below. First, sample independent feature selection was performed which involved filtering SNPs by their annotation. The data was then split into five folds, leaving one fold to report the final model performance. The remaining four folds were used for model optimisation and training. In 3-fold cross-validation, two folds were used for training and one as validation data to evaluate the model's performance. A GWAS was run on each fold, followed by LD clumping. The first parameter optimised was the P value threshold (Pt) for feature selection, followed by the XGBoost hyperparameters (HPs). Model optimisation involved choosing the model with the hyperparameter values that resulted in the highest AUC on the validation dataset. Sample dependent feature selection was then performed (involved running a GWAS, performing LD clumping and retaining SNPs that pass the best performing Pt) and the model was run using the best performing HPs on all four training folds. Predictions were made on the test fold. Finally, confounder adjustment was performed on the predictions and performance metrics were calculated.

![image](https://github.com/laurafahey02/XGBoost4IntelligencePrediction/blob/main/XGB_workflow.jpg)


## Brief description of scripts

The contents of **/cv1** were replicated for two more directories, cv2 and cv3, representing each cross-validaiton fold for model optimisaiton. **GWAS_clumping_recode.sh** was used to preprocess data for model optimisation. It creates training and validation data subsets for three-fold cross-validation. It runs a GWAS for the purpose of filtering SNPs by LD clumping and P value threshold. It also converts plink files to text files for input into Python. **xgb_pt0.1.py** was used for P value threshold optimisation. hp_optim.py was used for XGBoost hyperparamter optimisation. **outer.py** was used to run XGBoost on the full training dataset using the optimised hyperparamters. It uses this model to predict phenotype values of the test samples and calculate performance metrics. **xgb_reds_adjust.R** adjusts the XGBoost predictions for confounders and claulates performance metrics.

