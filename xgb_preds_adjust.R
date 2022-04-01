library(dplyr)
library(splines)

covar <- read.table("test.cov.pheno", header=T)
preds <- read.table("prediction_probs.txt")

# add preds to covar file

covar$PRED <- preds$V1

# Convert non qunatitative things to factors

covar$FID <- as.factor(covar$FID)
covar$IID <- as.factor(covar$IID)
covar$SEX <- as.factor(covar$SEX)
covar$CENTRE <- as.factor(covar$CENTRE)
covar$ARRAY <- as.factor(covar$ARRAY)
covar$PHENOTYPE <- as.factor(covar$PHENOTYPE)

# Get rid of lines with NA

#covar <- covar[complete.cases(covar), ]

# add preds and obs to covar

covar_rescale <- mutate_if(covar, is.numeric, list(~as.numeric(scale(.))))

covar_pheno <- subset(covar_rescale,select=c(16,17,3,4,5,6,7,8,9,10,11,12,13,14,15))

# Run logistic model with only ML predictions as predictors
logistic <- glm(PHENOTYPE ~ PRS, family = binomial(link = 'logit'), data=covar_pheno, na.action = na.exclude)
#summary(logistic)

# Run logistic model with ML predictions and confounders as predictors
logistic_covar_pred <- glm(PHENOTYPE ~ PRED + bs(SEX, knots=5) + bs(CENTRE, knots=5) + bs(PC1, knots=5) + bs(PC2, knots=5) + bs(PC3, knots=5) + bs(PC4, knots=5) + bs(PC5, knots=5) + bs(PC6, knots=5) + bs(PC7, knots=5) + bs(PC8, knots=5) + bs(TDI, knots=5), family = binomial(link = 'logit'), data=covar_pheno, na.action = na.exclude)
#summary(logistic_covar_prs)

# Run logistic model with only confounders as predictors
logistic_covar <- glm(PHENOTYPE ~ bs(SEX, knots=5) + bs(ARRAY, knots=5), bs(CENTRE, knots=5) + bs(PC1, df=5) + bs(PC2, df=5) + bs(PC3, df=5) + bs(PC4, df=5) + bs(PC5, df=5) + bs(PC6, df=5) + bs(PC7, df=5) + bs(PC8, df=5) + bs(TDI, df=5) + bs(AGE, df=5), family = binomial(link = 'logit'), data=covar_pheno, na.action = na.exclude)

nagelkerke(logistic_covar_prs)
nagelkerke(logistic_covar)
nagelkerke(logistic_prs)
