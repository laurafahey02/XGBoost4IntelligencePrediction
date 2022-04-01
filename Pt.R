args <- commandArgs(trailingOnly = TRUE)

snps <- read.table("clumped_snps", header=T)
snps_pt <- snps[snps$P < args[1],]
write.table(snps_pt, args[2], col.names=F, row.names=F, quote=F)
