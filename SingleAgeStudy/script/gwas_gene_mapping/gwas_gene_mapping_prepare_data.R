# ########################################################################
# This script aims to classify the data among age, phenotype and suffix
# and to provide usefull data structure to manage them
# ########################################################################

# ##############
# Load data
# ##############
## @knitr load_data

cat("<H4>Loading data</H4>")

# Get the list of gene mapped files without their path
basename_gene_mapping_file_list = do.call( basename, list( gene_mapping_file_list))

# Identify the gene mapping file for each age, phenotype, data stats type (MEAN, CV) and suffix 
# Put the retrieved information in two dataframe (one for found files (GENE_MAPPING_FILE_DF), one for not found file (missing_gene_mapping_file_df))
GENE_MAPPING_FILE_DF = data.frame()
missing_gene_mapping_file_df = data.frame()
# parse ages, phenotypes and suffixes
for( current_index in 1:length( age_list)){
  current_age = age_list[ current_index]
  current_pheno = phenotype_name_list[ current_index]
  current_data_stat_type = as.character( data_stat_type_list[ current_index])
  for( current_suffix in suffix_list){
    # build the theoretical file name from the various parameter
    current_file_name = paste0( "phenotype_", current_pheno, "_", current_age, "W_", current_data_stat_type, "_ordered_GWASresults_signif", current_suffix, "_genemap.txt")
    # look if that filename exists in the results, if so, add its entry in the
    # dataframe of found data, if not, add it to the dataframe of missing data
    current_index = which( basename_gene_mapping_file_list == current_file_name)
    if( length( current_index) == 1){
      GENE_MAPPING_FILE_DF = rbind( GENE_MAPPING_FILE_DF, data.frame( age = current_age,
                                                                      phenotype = current_pheno,
                                                                      suffix = current_suffix,
                                                                      data_stat_type = current_data_stat_type,
                                                                      filename = basename_gene_mapping_file_list[ current_index],
                                                                      filepath = gene_mapping_file_list[ current_index],
                                                                      stringsAsFactors = FALSE
                                                                      )
                                  )
    }else{
      missing_gene_mapping_file_df = rbind( missing_gene_mapping_file_df, data.frame( age = current_age,
                                                                      phenotype = current_pheno,
                                                                      suffix = current_suffix,
                                                                      data_stat_type = current_data_stat_type,
                                                                      stringsAsFactors = FALSE
                                                                      )
                                  )
    }
  } 
}


cat("<BR>Number of found data files:", nrow( GENE_MAPPING_FILE_DF))
cat("<BR>Number of not found data files:", nrow( missing_gene_mapping_file_df))

# Show the table of avilable results from GWAS
datatable( GENE_MAPPING_FILE_DF, caption = "List of available results from GWAS")

# Add the row names corresponding to the filename
row.names( GENE_MAPPING_FILE_DF) = GENE_MAPPING_FILE_DF$filename

# Parse the list of available result files to get their informations in dataframe that will be stored in a named list
# and take advantage of this parsing to build a map able to convert gene FlybaseID to gene symbol
GENE_MAPPING_DF_LIST = list()
GENE_FLYBASE_TO_SYMBOL_CONVERT_DF = data.frame()
for( line_index in 1:nrow( GENE_MAPPING_FILE_DF)){
  current_filename = GENE_MAPPING_FILE_DF$filename[ line_index]
  current_filepath = file.path( WORKING_DIR, GENE_MAPPING_FILE_DF$filepath[ line_index])
  GENE_MAPPING_DF_LIST[[ current_filename]] = read.table( current_filepath, header=TRUE, sep="\t", quote=NULL, stringsAsFactors = FALSE)
  GENE_FLYBASE_TO_SYMBOL_CONVERT_DF = rbind( GENE_FLYBASE_TO_SYMBOL_CONVERT_DF, data.frame( flybase = GENE_MAPPING_DF_LIST[[ current_filename]]$FlybaseID,
                                                                                           symbol = GENE_MAPPING_DF_LIST[[ current_filename]]$GeneSymbol))
}
# Remove duplciated line in convertion map
GENE_FLYBASE_TO_SYMBOL_CONVERT_DF = GENE_FLYBASE_TO_SYMBOL_CONVERT_DF[ !duplicated( GENE_FLYBASE_TO_SYMBOL_CONVERT_DF, by=c("flybase", "symbol")),]
row.names( GENE_FLYBASE_TO_SYMBOL_CONVERT_DF) = GENE_FLYBASE_TO_SYMBOL_CONVERT_DF$flybase

# ########################
# Filter data
# ########################

## @knitr filter_data

cat("<H4>Filtering data</H4>")

#
# Removing genes associated with mutations present in less than a certain number of lines
# .......................................................................................

cat("<BR><b>Removing genes associated with mutations present in less than", EXCLUDED_LINE_NUMBER, "strains in GWAS</b>")

# -- Create a new list for the filtered result
gene_mapping_maf_df_list =list()
# -- Add information of nombre of genes after filtering in main dataframe
GENE_MAPPING_FILE_DF$raw.nb.genes = rep( 0, nrow( GENE_MAPPING_FILE_DF))
GENE_MAPPING_FILE_DF$maf.nb.genes = rep( 0, nrow( GENE_MAPPING_FILE_DF))

# -- Parse the filenames to filter the corresponding dataframes
for( filename in names( GENE_MAPPING_DF_LIST)){
  current_df = GENE_MAPPING_DF_LIST[[ filename]]
  gene_mapping_maf_df_list[[ filename]] = current_df[ which( current_df$NbOfLinesForMutationInGWAS >= EXCLUDED_LINE_NUMBER), ]
  GENE_MAPPING_FILE_DF[ filename, "raw.nb.genes"] = length( unique( current_df$FlybaseID))
  GENE_MAPPING_FILE_DF[ filename, "maf.nb.genes"] = length( unique( gene_mapping_maf_df_list[[ filename]]$FlybaseID))
}

#
# Removing genes associated with mutations with uninteresting effects
# ....................................................................

cat("<BR><b>Removing genes associated with", paste( EXCLUDED_EFFECT_SET, collapse="/"), "mutations </b>")

# -- Create a new list for the filtered result
gene_mapping_effect_df_list = list()
# -- Add information of nombre of genes after filtering in main dataframe
GENE_MAPPING_FILE_DF$effect.nb.genes = rep( 0, nrow( GENE_MAPPING_FILE_DF))

# -- Parse the filenames to filter the corresponding dataframes
for( filename in names( gene_mapping_maf_df_list)){
  current_df = gene_mapping_maf_df_list[[ filename]]
  gene_mapping_effect_df_list[[ filename]] = current_df[ which( !(current_df$Type %in% EXCLUDED_EFFECT_SET)), ]
  GENE_MAPPING_FILE_DF[ filename, "effect.nb.genes"] = length( unique( gene_mapping_effect_df_list[[ filename]]$FlybaseID))
}

#
# Removing genes associated with mutations to far from gene
# ....................................................................

cat("<BR><b>Removing genes associated to mutations at more than", MAX_DISTANCE, "bp</b>")

# -- Create a new list for the filtered result
gene_mapping_distance_df_list = list()
# -- Add information of nombre of genes after filtering in main dataframe
GENE_MAPPING_FILE_DF$distance.nb.genes = rep( 0, nrow( GENE_MAPPING_FILE_DF))

# -- Parse the filenames to filter the corresponding dataframes
for( filename in names( gene_mapping_effect_df_list)){
  current_df = gene_mapping_effect_df_list[[ filename]]
  gene_mapping_distance_df_list[[ filename]] = current_df[ which( current_df$Position <= MAX_DISTANCE), ]
  GENE_MAPPING_FILE_DF[ filename, "distance.nb.genes"] = length( unique( gene_mapping_distance_df_list[[ filename]]$FlybaseID))
}


#
# Once all the filtering are done, look at the final result and extract final information
# .......................................................................................

# -- Show the main dataframe information on evolution of number of genes during filtering
datatable( GENE_MAPPING_FILE_DF[ , c( "age", "phenotype", "suffix", "raw.nb.genes", "maf.nb.genes", "effect.nb.genes", "distance.nb.genes")],
           rownames = FALSE)

# -- Define which is the final choice of filtering
GENE_MAPPING_FINAL_DF_LIST = gene_mapping_distance_df_list

# -- Get the final list of all detected genes and available phenotypes
# -- and output to file the fltered list of results
FINAL_GENES_FLYBASE_SET = vector()
FINAL_PHENOTYPE_SET = vector()
for( filename in names( GENE_MAPPING_FINAL_DF_LIST)){
  FINAL_PHENOTYPE_SET = append( FINAL_PHENOTYPE_SET, GENE_MAPPING_FILE_DF[ filename, "phenotype"])
  current_df = GENE_MAPPING_FINAL_DF_LIST[[ filename]]
  write.table( current_df, file = file.path( OUTPUT_DIR, paste0( tools::file_path_sans_ext( filename), "_filtered.txt")),
               row.names = FALSE, col.names = TRUE, quote = FALSE, sep="\t")
  FINAL_GENES_FLYBASE_SET = append( FINAL_GENES_FLYBASE_SET, GENE_MAPPING_FINAL_DF_LIST[[ filename]]$FlybaseID)
}
FINAL_GENES_FLYBASE_SET = unique( FINAL_GENES_FLYBASE_SET)
FINAL_PHENOTYPE_SET = unique( FINAL_PHENOTYPE_SET)
