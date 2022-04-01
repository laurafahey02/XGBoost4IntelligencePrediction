#!/bin/sh -l
#SBATCH -J preprocessing
# SBATCH --partition=highmem

# Extract training samples
plink2 --bfile /data/lfahey/ukb_qc/pheno/GWAS_clumping_workflow/annot_highlow --keep /data/lfahey/ukb_qc/pheno/GWAS_clumping_workflow/3CV_train_split_1.txt --make-bed --out train_highlow

# GWAS
plink2 --bfile train_highlow --glm firth-fallback hide-covar --covar /data/lfahey/ukb_qc/qcd_files2/FI.cov --covar-variance-standardize COVAR3 COVAR4 COVAR5 COVAR5 COVAR6 COVAR7 COVAR8 COVAR9 COVAR10 COVAR12 COVAR13 --maf 0.01 --out highlow_train

# Clump

plink --bfile train_highlow --clump highlow_train.PHENO1.glm.logistic.hybrid --clump-kb 250 --clump-p1 1 --clump-p2 1 --clump-r2 0.1 --clump-snp-field ID

# edit clump results:

awk '{print $3, $5}' plink.clumped > clumped_snps

# Extract SNPs with P value threshold less than 0.1

Rscript ../Pt.R 0.1 0.1snps.out

# Extract clumped snps and recode

plink2 --bfile train_highlow --extract 0.1snps.out --export A --out train_highlow.0.1

cut -f 6- train_highlow.0.1.raw | tr "\t" " " > train_highlow.0.1.raw.txt

awk '{gsub(/1/, 0, $1)}1' train_highlow.0.1.raw.txt | awk '{gsub(/2/, 1, $1)}1' > 0.1.txt

sed -i 's/NA/9/g' 0.1.txt

rm cv1.63k.raw.txt

### test subset

# Extract training samples from QC'd files
for i in {1..22}; do  plink2 --pfile /data/lfahey/ukb_qc/qcd_files2/${i}_qcd --extract 0.3.snps.out --rm-dup force-first list --keep ../3CV_val_split_1.txt --pheno /data/lfahey/ukb_qc/pheno/highlow.samples --make-bed --out ${i}_test; done

## Create allfiles.txt
for i in {1..22}; do echo ${i}"_test.bed" $i"_test.bim" $i"_test.fam"; done > allfiles.txt

plink --merge-list allfiles.txt --make-bed --out all_test

plink2 --bfile all_test --export A --out all.test

cut -f 6- all.test.raw | tr "\t" " " > all.test.raw.txt

awk '{gsub(/1/, 0, $1)}1' all.test.raw.txt | awk '{gsub(/2/, 1, $1)}1' > 0.3.test.txt

sed -i 's/NA/9/g' 0.3.test.txt
