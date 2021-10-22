# ###############################################################################################
# This script aims to compare phenotypes at fixed ages. The script compute the mean of
# the phenotype on each DGRP strain and produce a cluster of of the matrix strains vs phenotypes.
# A heatmap of the phenotype cluster correlation is then shown and a study of the strains cluster
# is made.
# ###############################################################################################

## @knitr compare_phenotype

cluster_number_pheno = 10
cluster_number_strain = 10
BrBG <- colorRampPalette(brewer.pal(11, "BrBG"))
RdBu <- colorRampPalette(brewer.pal(11, "RdBu"))

cat("<H5>Select phenotypes and strains that can be used for clustering</H5>")

# -- select phenotype with enough non NA values
selected_phenotype_set = vector()
for( current_phenotype in PHENOTYPE_SET){
  ok_pheno = na.exclude( MEAN_DF[[ current_age]][ , current_phenotype])
  if( length( ok_pheno) > 0.9*nrow( MEAN_DF[[ current_age]])){
    selected_phenotype_set = append( selected_phenotype_set, current_phenotype)
  }else{
    cat("<BR>Phenotype", current_phenotype, "has been removed due to too missing information")
  }
}

# -- select the strains that are complete
ok_strain_set = complete.cases( MEAN_DF[[ current_age]][, c( "strain_name", "age", selected_phenotype_set)])
cat("<BR> Removed strains due to missing information :", nrow( MEAN_DF[[ current_age]]) - length(ok_strain_set))

# -- draw the clustered heatmap
row.names( MEAN_DF[[ current_age]]) = MEAN_DF[[ current_age]][ , "strain_name"]
heatmaply( MEAN_DF[[ current_age]][ ok_strain_set, selected_phenotype_set], 
                            distfun = "spearman",
                            scale = "column", 
                            cexCol = 0.5, cexRow = 0.2,
                            k_col=NA, k_row=NA,
                            width = 1000, height=1000,
                            main = paste( "Correlation between phenotypes and individuals (Spearman on mean)")
                        )


#
# -- select the phenotypes groups
#
# cat("<H5>Analyzing clusters on phenotypes</H5>")
# cut = cutree(pheno_heatmap$tree_col, k = cluster_number_pheno)
# 
# cluster_ordered_pheno = vector()
# cluster_size_set = c(0)
# total_size = 0
# for( cluster_index in 1:cluster_number_pheno){
#   pheno_set = which( cut == cluster_index)
#   cluster_ordered_pheno = append( cluster_ordered_pheno, pheno_set)
#   total_size = total_size + length( pheno_set)
#   cluster_size_set = append( cluster_size_set, total_size)
#   if( length( pheno_set) > 0){
#     cat("<BR><BR>Cluster", cluster_index,":<BR> ", paste( names( cut[ pheno_set]), collapse="<BR>  "))
# #       if( length( pheno_set) > 1){
# #         correlation_plot = ggcorplot( data = MEAN_DF[[ current_age]][ , names( cut[ pheno_set])], var_text_size =2, cor_text_limits = c(4,6))
# #         correlation_plot = correlation_plot +
# #           ggtitle( paste("Age", current_age, "W"))
# #         print( correlation_plot)
# #       }
#   }
# }

# -- plot the correlation heatmap between phenotypes in cluster order
#cluster_ordered_pheno = pheno_heatmap$x$layout$xaxis$categoryarray
cor_mat = matrix( rep(0, length( selected_phenotype_set)^2), ncol = length( selected_phenotype_set))
colnames( cor_mat) = selected_phenotype_set
rownames( cor_mat) = selected_phenotype_set
for( first_pheno_index in 1:length(selected_phenotype_set)){
  for( second_pheno_index in first_pheno_index:length( selected_phenotype_set)){
    cor = cor( MEAN_DF[[ current_age]][ ok_strain_set, selected_phenotype_set[ first_pheno_index]], 
               MEAN_DF[[ current_age]][ ok_strain_set, selected_phenotype_set[ second_pheno_index]], 
               method="spearman")
    cor_mat[ first_pheno_index, second_pheno_index] = cor
    cor_mat[ second_pheno_index, first_pheno_index] = cor
  }
}

heatmaply( cor_mat, 
                           distfun = "spearman",
                           cutree_cols = cluster_number_pheno,
                           cexCol = 0.5, cexRow = 0.5,
                           k_col=NA, k_row=NA,
                           colors = RdBu,
                           width = 1000, height=1000,
                           main = paste( "Correlation between phenotypes (Spearman on mean)")
)


# -- select the strain groups
# cat("<BR>--------------------------------")
# cat("<BR>Analyzing clusters on strains")
# cat("<BR>--------------------------------")
# cut = cutree(pheno_heatmap$tree_row, k = cluster_number_strain)
# 
# for( cluster_index in 1:cluster_number_strain){
#   individual_set = which( cut == cluster_index)
#   if( length( individual_set) > 0){
#     cat("<BR><BR>Cluster", cluster_index,":<BR> Strains:", paste( names( cut[ individual_set]), collapse=", "))
#     cat("<BR> Dates = ", paste( unique( ALL_DATA_DF[ which( ALL_DATA_DF[ , INDIVIDUAL_STRAIN] %in% names( cut[ individual_set])
#                                                           & ALL_DATA_DF[ , PHENOTYPE_AGE] == current_age)
#                                   , INDIVIDUAL_DATE]), collapse =", "))
#   }
# }


