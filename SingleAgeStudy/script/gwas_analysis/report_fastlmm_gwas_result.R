# ####################################################################################
# This script aims to report the result of the GWAS analysis made by the Fast-LMM
# tool.
# ####################################################################################

# ------------------------------------------------------------------------------------
# Define a function to plot a PNG image imported from external file
# ------------------------------------------------------------------------------------
plotPNG <- function( image_path){
	
	# Load the PNG image
	img = readPNG( image_path)
	
	# Create a plot with no axes, no box and no label
	plot( 1:2, type='n',  xaxt='n',  yaxt='n', xlab="", ylab="", bty="n")
	
	# Raster the image to the plot
	rasterImage(img, 1, 1, 2, 2)
}


# ------------------------------------------------------------------------------------
# MAIN
# # ------------------------------------------------------------------------------------

# Test if the list of files to parse are synchronized
if( length( phenotype_strain_values_file_list) != length( signif_result_file_list)
    || length( phenotype_strain_values_file_list) != length( manathanplot_file_list)
    || length( phenotype_strain_values_file_list) != length( QQplot_file_list)){

	stop( "ERROR: file lists does not have the same length.")
}

# Make report for each age
for( current_age in sort( unique( age_list))){
  
  dgrp_file_name = paste( "dgrp2_", current_age, "W", sep="")
  
  cat("\n##########################")
  cat("\n AGE", current_age, "W")
  cat("\n##########################")
  
  # Make report for each phenotype
  for( current_phenotype in sort( unique( phenotype_name_list))){
    
  	cat("\n----------------------------------------------")
  	cat("\n PHENOTYPE-----", current_phenotype)
  	cat("\n----------------------------------------------")
	
	for( current_data_stat_type in sort( unique( data_stat_type_list))){
		
		cat("\n----------------------------------------------")
		cat("\n DATA STAT TYPE-----", current_data_stat_type)
		cat("\n----------------------------------------------")
		
		# Search files with the right phenotype, age and data stat type
		found = FALSE
		pheno_age_key = paste0( current_phenotype, "_", current_age, "W_", current_data_stat_type)
		for( file_index in 1:length( phenotype_strain_values_file_list)){
			
			phenotype_strain_values_file = file.path( WORKING_DIR, phenotype_strain_values_file_list[ file_index])
			signif_result_file = file.path( WORKING_DIR, signif_result_file_list[ file_index])
			manathanplot_file = file.path( WORKING_DIR, manathanplot_file_list[ file_index])
			QQplot_file = file.path( WORKING_DIR, QQplot_file_list[ file_index])
			
			if( grepl( pheno_age_key, phenotype_strain_values_file) &&
					grepl( pheno_age_key, signif_result_file) &&
					grepl( pheno_age_key, manathanplot_file) &&
					grepl( pheno_age_key, QQplot_file) ){
				found = TRUE
				break;
			}
		}
		
		# Test if the files to be analyzed have been found
		if( !found){
			stop( "ERROR: unable to find all the required files for phenotype=" + current_phenotype + " and age =" + current_age)
		}else{
			cat("\n Analyzed files are:")
			cat("\nFile of phenotype/strain values=", phenotype_strain_values_file)
			cat("\nFile of GWAS significant results=", signif_result_file)
			cat("\nFile of Manathan plot=", manathanplot_file)
			cat("\nFile of QQplot=", QQplot_file)
		}
		
		# Locate the base name for the output file
		match = gregexpr( pattern ='_signif', signif_result_file)
		if( match[[1]][1] > 0){
			base_output_name = file.path( OUTPUT_DIR, basename( substr( signif_result_file, start = 1, stop = match[[1]][1] + 6)))
		}else{
			stop( "ERROR: unable to find string '_signif' in GWAS significant result file name:" + signif_result_file)
		}
	    
	    # Show the QQplot if exists
	    plotPNG( QQplot_file)
	    
	    # Show the Manathan plot if exists
	    plotPNG( manathanplot_file)
	    
	    # Plot the phenotype values used for the GWAS
		phenotype_strain_values = read.table( phenotype_strain_values_file, header = FALSE, stringsAsFactors = FALSE, sep=" ")
		phenotype_strain_values_plot = ggplot( data=NULL) + 
		    geom_boxplot( data = phenotype_strain_values, aes(x=1, y=V3)) +
		    ggtitle( "Mean values of the phenotype per strain") +
		    ylab("Phenotype strain mean value")
		print( phenotype_strain_values_plot)
	
	    
	    # Show statistics on SNPs
		# read the file
		# headers are : sid_index  SNP	Chr	GenDist	ChrPos	PValue	SnpWeight	SnpWeightSE	SnpFractVarExpl	Mixing	Nullh2
		snp_df = read.table( signif_result_file, header = TRUE, sep = "\t")
		
		pval_histogram = ggplot( data = NULL) + 
		                  geom_histogram( data = snp_df, aes( PValue)) + 
		                      ggtitle( paste( "Pvalue histogram for", current_phenotype, "\nat age", current_age, "W"))
		
		print( pval_histogram)
		
		# Export the SNP that have a p-value lesser than 1e-5
		cat("\nExporting SNP with pval<1e-5")
		signif_e5 = paste( base_output_name, "1e-5.txt", sep="")
		write.table( snp_df[ which( snp_df[ , "PValue"] <= 0.00001 ), ], file = signif_e5, col.names = TRUE, row.names = FALSE, quote = FALSE, sep = "\t")
		
		list_signif_e5 = paste( base_output_name, "1e-5_list.txt", sep="")
		write.table( snp_df[ which( snp_df[ , "PValue"] <= 0.00001 ), "SNP"], file = list_signif_e5, col.names = TRUE, row.names = FALSE, quote = FALSE, sep = "\t")
		
		# Export the SNP that have the 100 best p-value
		cat("\nExporting SNP with 100 best pval")
		value_100th = sort( snp_df[ , "PValue"], decreasing = FALSE)[100]
		
		signif_100th = paste( base_output_name, "100th.txt", sep="")
		write.table( snp_df[ which( snp_df[ , "PValue"] <= value_100th ), ], file = signif_100th, col.names = TRUE, row.names = FALSE, quote = FALSE, sep = "\t")
		
		list_signif_100th = paste( base_output_name, "100th_list.txt", sep="")
		write.table( snp_df[ which( snp_df[ , "PValue"] <= value_100th ), "SNP"], file = list_signif_100th, col.names = TRUE, row.names = FALSE, quote = FALSE, sep = "\t")
		
		# Copy the used SNP result file to the output
		file.copy( signif_result_file, file.path( OUTPUT_DIR, basename( signif_result_file)))
	}
  }
}