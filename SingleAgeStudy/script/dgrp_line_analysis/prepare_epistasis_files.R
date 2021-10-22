# ####################################################################################
# This script aims to produce files that contains phenotype information that will
# be use in later epistasis analysis
# ####################################################################################

## @knitr prepare_epistasis_files

DATA_TO_ANALYZE = match.arg( DATA_TO_ANALYZE, c( "MEAN", "CV"))

cat("<BR><H3>Preparing data for epistasis analysis for", DATA_TO_ANALYZE, "</H3>")

GWAS_TRANSFORMATION_MODE = match.arg( GWAS_TRANSFORMATION_MODE, c( "LOG2", "REMOVE_OUTLIER_LINES", "NONE"))
cat("<BR>Data transformation mode is", GWAS_TRANSFORMATION_MODE)

# Create the output folder
epistasis_output_dir = file.path( OUTPUT_DIR, EPISTASIS_OUTPUT_SUBFOLDER)
dir.create( epistasis_output_dir, showWarnings = FALSE, recursive = TRUE, mode = "0777")
cat("<BR>Output folder =", epistasis_output_dir)

cat("<BR><BR>")

# Parse the ages and the phenotypes to produce one file per age and phenotype
# containing the phenotype information per strain
dt_list = list()
count = 0
for( current_age in AGE_SET){
  
  information_epistasis_preparation_df = data.frame()
  for( current_phenotype in selected_phenotype_set){
    
    # Get the means of the current phenotype for current age
    if( DATA_TO_ANALYZE == "MEAN"){    
      phenotype_df = data.frame( fid = MEAN_DF[[ current_age]]$strain_name,
                               iid = MEAN_DF[[ current_age]]$strain_name,
                               phenotype = MEAN_DF[[ current_age]][ , current_phenotype]
                              )
    }
    if( DATA_TO_ANALYZE == "CV"){
      phenotype_df = data.frame( fid = CV_DF[[ current_age]]$strain_name,
                                 iid = CV_DF[[ current_age]]$strain_name,
                                 phenotype = CV_DF[[ current_age]][ , current_phenotype]
      )
    }
    phenotype_df$fid = gsub("dgrp" , "line_", phenotype_df$fid)
    phenotype_df$iid = gsub("dgrp" , "line_", phenotype_df$iid)
    
    # Remove the NA values
    phenotype_na_indexes =  which( is.na( phenotype_df$phenotype))
    if( length( phenotype_na_indexes) > 0){
      na_values_text = paste( phenotype_df[ phenotype_na_indexes, "fid"], collapse=";")
      phenotype_df = phenotype_df[ -phenotype_na_indexes, ]
    }else{
      na_values_text = ""
    }
    
    # Try to manage the outliers values by searching a suitable transformation
    phenotype_values_quartiles = quantile( phenotype_df$phenotype, probs = c(0.25,0.75), na.rm = TRUE)
    iqr = phenotype_values_quartiles[2] - phenotype_values_quartiles[1]  
    min_lim = phenotype_values_quartiles[1] - 1.5*iqr
    max_lim = phenotype_values_quartiles[2] + 1.5*iqr
    outliers_values_index = which( phenotype_df$phenotype < min_lim | phenotype_df$phenotype > max_lim)
    acception_interval = paste0("[", min_lim, ";", max_lim, "]")
    if( length( outliers_values_index) > 0){
      outliers_text = paste( phenotype_df[ outliers_values_index, "fid"], " (", signif( phenotype_df[ outliers_values_index, "phenotype"], 3), ")", sep="", collapse=";\n")
  	  if( GWAS_TRANSFORMATION_MODE == "LOG2"){
  		  phenotype_df$phenotype = log2( phenotype_df$phenotype)
  	  }else if( GWAS_TRANSFORMATION_MODE == "REMOVE_OUTLIER_LINES"){
  		  phenotype_df = phenotype_df[ -outliers_values_index,]
  	  }
    }else{
      outliers_text = ""
    }
    
    # Export the data frame
    write.table( phenotype_df, file = get_phenotype_stat_file( epistasis_output_dir, current_phenotype, current_age, DATA_TO_ANALYZE), quote = FALSE, col.names = FALSE, row.names = FALSE, sep=" ")

    # Export the families used
    write.table( phenotype_df[,1:2], file = get_pheno_age_families_file( epistasis_output_dir, current_phenotype, current_age, DATA_TO_ANALYZE), quote = FALSE, col.names = FALSE, row.names = FALSE, sep=" ")
    
    # Build the information dataframe
    information_epistasis_preparation_df = rbind( information_epistasis_preparation_df, 
                                             data.frame( age = current_age,
                                                         phenotype = current_phenotype,
                                                         nb.exported.data.for.gwas = nrow( phenotype_df),
                                                         na.values.lines = na_values_text,
                                                         values.acceptation.interval = acception_interval,
                                                         outliers.lines = outliers_text
                                             ))
  }
  
  # Print the information data frame
  count = count + 1
  dt_list[[ count]] = datatable( information_epistasis_preparation_df, 
                                 caption = paste("Information on epistasis data preparation for", DATA_TO_ANALYZE, "at age", current_age),
                                 width = 3000)
}
htmltools::tagList( dt_list)