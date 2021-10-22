# ########################################################################
# This script aims to compare phenotypes by looking at the common
# mapped genes from the GWAS results
# ########################################################################

## @knitr load_common_gene_jaccard_index_function

#
# Define a function counting the number of gene in common between two GWAS filtered results on phenotypes
#
common_gene_jaccard_index <- function( first_df, second_df){
  
  inter = length( intersect( unique( first_df$FlybaseID), unique( second_df$FlybaseID)))
  union = length( unique( c( first_df$FlybaseID, second_df$FlybaseID)))
  return( inter/union)
}

# ###################
# MAIN
# ###################

## @knitr compute_phenotype_correlation

#
# Compute the jaccard index between set of genes associated to each phenotype,
# grouping phenotypes by age and by suffix
#

cat("<H4>Heatmaps of Jaccard indexes of set of mapped genes for each phenotype</H4>")
all_correlation_tables = list()
count = 1
# -- parse the list of ages and suffixes
for( current_age in unique( GENE_MAPPING_FILE_DF$age)){
  for( current_data_stat_type in unique( data_stat_type_list)){
    for( current_suffix in unique( GENE_MAPPING_FILE_DF$suffix)){
      # -- get only the entries corresponding to the current age and suffix
      current_file_df = GENE_MAPPING_FILE_DF[ which( GENE_MAPPING_FILE_DF$age == current_age &
                                                     GENE_MAPPING_FILE_DF$data_stat_type == current_data_stat_type &
                                                     GENE_MAPPING_FILE_DF$suffix == current_suffix &
                                                     GENE_MAPPING_FILE_DF$phenotype %in% prefered_phenotypes), ]
      
      # -- parse the pairs of phenotypes to compute the jaccard index between their set of mapped genes
      # -- and store the result in a dataframe in order to show it has a heatmap
      correlation_df = data.frame()
      phenotype_names_set = vector()
      for( current_filename_1 in row.names( current_file_df)){
        phenotype_names_set = append( phenotype_names_set, current_file_df[ current_filename_1, "phenotype"])
        current_phenotype_df_1 = GENE_MAPPING_FINAL_DF_LIST[[ current_filename_1]]
        current_jaccard_index_list = list()
        for( current_filename_2 in row.names( current_file_df)){
          current_phenotype_2 = current_file_df[ current_filename_2, "phenotype"]
          current_phenotype_df_2 = GENE_MAPPING_FINAL_DF_LIST[[ current_filename_2]]
          jaccard_index = common_gene_jaccard_index( current_phenotype_df_1, current_phenotype_df_2)
          current_jaccard_index_list[[ current_phenotype_2]] = jaccard_index
        }
        correlation_df = rbind( correlation_df, current_jaccard_index_list)
      }
      row.names( correlation_df) = phenotype_names_set

      all_correlation_tables[[ count]] = heatmaply( correlation_df,
                                                    colors= colorRampPalette(brewer.pal(9, "Blues")),
                                                    cexCol = 0.8,cexRow = 0.8,
                                                    main = paste( "Gene list comparison at age", current_age, "for", current_data_stat_type, "with selected snps at", current_suffix, "(Selected phenotypes)"))
      count = count + 1
    }
  }
}

htmltools::tagList( all_correlation_tables)

#
# Compute for each gene, its participation to each phenotype
# with phenotypes grouped by age and suffix
# To do so, for each age/suffix group, build a dataframe "genes vs phenotype" that will contain
# a 1 when the gene is associated to the phenotype, 0 if not
#
# 
# cat("<H4>Heatmaps of gene membership to set of mapped genes for each phenotype</H4>")
# 
# all_membership_tables = list()
# count = 1
# # -- parse the list of ages and suffixes
# for( current_age in unique( GENE_MAPPING_FILE_DF$age)){
#   for( current_data_stat_type in data_stat_type_list){
#     for( current_suffix in unique( GENE_MAPPING_FILE_DF$suffix)){
#       # -- get only the entries corresponding to the current age and suffix
#       current_file_df = GENE_MAPPING_FILE_DF[ which( GENE_MAPPING_FILE_DF$age == current_age &
#                                                      GENE_MAPPING_FILE_DF$data_stat_type == current_data_stat_type &
#                                                      GENE_MAPPING_FILE_DF$suffix == current_suffix &
#                                                      GENE_MAPPING_FILE_DF$phenotype %in% prefered_phenotypes), ]
#       
#       # -- initialized the final dataframe genes vs phenotype with only "0"
#       membership_df = data.frame( matrix( rep( 0, length( FINAL_PHENOTYPE_SET) * length( FINAL_GENES_FLYBASE_SET)), ncol=length( FINAL_PHENOTYPE_SET)))
#       names( membership_df) = FINAL_PHENOTYPE_SET
#       row.names( membership_df) = FINAL_GENES_FLYBASE_SET
#       # -- assign the "1" in the dataframe when gene is associated to the phenotype
#       for( current_filename in row.names( current_file_df)){
#         current_phenotype = GENE_MAPPING_FILE_DF[ current_filename, "phenotype"]
#         for( gene_id in GENE_MAPPING_FINAL_DF_LIST[[ current_filename]]$FlybaseID){
#           membership_df[ gene_id, current_phenotype] = 1
#         }
#       }
# 
#       # Change the flybaseID to gene symbols
#       row.names( membership_df) = GENE_FLYBASE_TO_SYMBOL_CONVERT_DF[ row.names( membership_df), "symbol"]
#       # all_membership_tables[[ count]] = datatable( membership_df,
#       #                                              caption = paste( "Gene membership at age", current_age,"for", current_data_stat_type, "with selected snps at", current_suffix, "(All phenotypes)"))
#       # 
#       # count = count + 1
#       
#       all_membership_tables[[ count]] = datatable( membership_df[ , which( names( membership_df) %in% prefered_phenotypes)],
#                                                    caption = paste( "Gene membership at age", current_age, "for", current_data_stat_type, "with selected snps at", current_suffix, "(Selected phenotypes)"))
#       
#       count = count + 1
#     }
#   }
# }
# 
# htmltools::tagList( all_membership_tables)
