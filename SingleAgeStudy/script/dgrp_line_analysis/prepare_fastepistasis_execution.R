# ####################################################################################
# This script aims to execute the phenotype GWAS thanks to the Fast-LMM analysis
# ####################################################################################

## @knitr prepare_epistasis_execution

cat("<BR>")

DATA_TO_ANALYZE = match.arg( DATA_TO_ANALYZE, c( "MEAN", "CV"))

# Make report for each age
fast_epistasis_df = data.frame()

cat("<H3>Preparing FastEpistasis analysis execution for", DATA_TO_ANALYZE, "</H3>")

dt_list = list()
dt_count = 1
for( current_age in AGE_SET){
  
  # Make report for each phenotype
  fast_epistasis_run_information_df = data.frame()
  for( current_phenotype in PHENOTYPE_SET){

  	# Prepare Phenotype filename and check it exist
  	input_dir = file.path( OUTPUT_DIR, EPISTASIS_OUTPUT_SUBFOLDER)
  	phenotype_file_name = get_phenotype_stat_file( NULL, current_phenotype, current_age, DATA_TO_ANALYZE)
  	if( !file.exists( file.path( input_dir, phenotype_file_name))){
  		cat("<BR>Phenotype data file does not exist for ", current_phenotype, ": bypass Epistasis execution")
  		next
  	}
		
    # Build the command to execute the python FastEpistasis script
		current_dataframe = data.frame( age = c( current_age),
                										phenotype_name = c( current_phenotype),
                										input_folder=c( input_dir),
                										phenotype_file=c( phenotype_file_name),
                										families_file=c( get_pheno_age_families_file( OUTPUT_DIR, current_phenotype, current_age, DATA_TO_ANALYZE))
		                                )

    fast_epistasis_df = rbind( fast_epistasis_df, current_dataframe)
    fast_epistasis_run_information_df = rbind( fast_epistasis_run_information_df, 
                                               data.frame( age = current_age, phenotype = current_phenotype))
  }
  dt_list[[ dt_count]] = datatable( fast_epistasis_run_information_df, 
                                 caption = paste( "Phenotype planned for Fastepistasis analysis at age", current_age))
  dt_count = dt_count + 1
}
htmltools::tagList( dt_list)

# Write the commands to file
output_filename = file.path( OUTPUT_DIR, EPISTASIS_OUTPUT_SUBFOLDER, paste0( "execute_epistasis_", DATA_TO_ANALYZE, ".txt"))
write.table( fast_epistasis_df, file=output_filename, col.names = TRUE, row.names = FALSE, quote = FALSE, sep=";")