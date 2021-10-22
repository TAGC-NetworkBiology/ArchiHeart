# #######################################################################
# This script aims to look at the global behavior of phenotype values
# for each strain and to apply various correction to look at their effect
# The script also compute the MEAN and CV of each pair phenotype/strain
# and report list of pairs of which this computation was not possible.
# At the end, the data to use are chosen according to the selected type
# of correction to apply.
# #######################################################################

## @knitr describe_phenotypes

# Check if the correction mode is correct
PHENOTYPE_CORRECTION_MODE = match.arg( PHENOTYPE_CORRECTION_MODE, c('NO_CORRECTION', 'REMOVE_OUTLIERS', 'CONTROL_CORRECTION'))

# ..................................................................
# For each phenotype, display the values of the measure by strains
# First, display the raw measures then compute the values removing the
# 1.5IQR outliers. Build a new dataframe with those restricted values.
# Note that all the type of correction will be applied to show the data 
# but only the required one will be used to compute the means and CV
# ..................................................................

# -- initialize the dataframe that will contains values to use for mean and CV computation
DATA_TO_USE_LONG_DATA_DF[[ current_age]] = data.frame()

# -- parse the list of phenotypes
for( current_phenotype in PHENOTYPE_SET){
  
  cat("<BR><H5>", current_phenotype, "</H5>")
  
  # Get all the values for the current age and phenotype
  current_df = ALL_DATA_DF[ which( ALL_DATA_DF$strain_number %in% not_control_strain_set &
                                     ALL_DATA_DF$phenotype_name == current_phenotype &
                                     ALL_DATA_DF$age == current_age &
                                     !is.na( ALL_DATA_DF$value)
                                   ), ]
  
	# If no correction is required, raw data are used to compute the mean and CV
  # (see MEAN_DF and CV_DF computation at the end of the script)					 
	if( PHENOTYPE_CORRECTION_MODE == "NO_CORRECTION"){
		DATA_TO_USE_LONG_DATA_DF[[ current_age]] = rbind( DATA_TO_USE_LONG_DATA_DF[[ current_age]], current_df)
	}
  
  # -- build the plot of the raw values as boxplot per strain
  ypos_1 = max( current_df$value)
  all_values_plot = ggplot( data = current_df, aes( strain_number, value, color=strain_number)) + 
                  geom_boxplot() +
                  theme( legend.position= "none") + theme(axis.text.x = element_text(size = 3, angle = 90, hjust = 1))+
                  stat_summary(fun.data = n_count_1, geom = "text", size = 1, angle=90, hjust = 0) +
                  ggtitle( paste( "All data for phenotype", current_phenotype)) + 
                  xlab("strain")
  
  # Remove the outliers values
  strain_list = unique( current_df$strain_number)
  for( current_strain in strain_list){
    strain_indexes = which( current_df$strain_number == current_strain)
    outliers_indexs_in_strain_indexes = get_15IQR_outliers_indexes( current_df[ strain_indexes, "value"])
    if( length( outliers_indexs_in_strain_indexes) > 0){
      current_df = current_df[ -strain_indexes[ outliers_indexs_in_strain_indexes], ]
    }
  }

	# If removing the outliers is required, data with no outliers are used (but wihtout applying control correction)
	# are used to compute the mean (see MEAN_DF and CV_DF computation at the end of the script)
	if( PHENOTYPE_CORRECTION_MODE == "REMOVE_OUTLIERS"){
		DATA_TO_USE_LONG_DATA_DF[[ current_age]] = rbind( DATA_TO_USE_LONG_DATA_DF[[ current_age]], current_df)
	}
  
  # -- build the plot of the values without outliers as boxplot per strain
  ypos_2 = max( current_df$value)
  nooutliers_values_plot = ggplot( data = current_df, aes( strain_number, value, color=strain_number)) + 
                          geom_boxplot() +
                          stat_summary(fun.y=mean, colour="red", geom="point", size=1,show.legend = FALSE) +
                          stat_summary(fun.data = n_count_2, geom = "text", size = 1, angle=90, hjust = 0) +
                          theme( legend.position= "none") + theme(axis.text.x = element_text(size = 3, angle = 90, hjust = 1)) +
                          ggtitle( paste( "Outliers removed data for phenotype", current_phenotype)) + 
                          xlab("strain")
  
  # Correct the value with the date correction computed in the previous analysis step (control analysis)
  correction_for_current_phenotype_age = RAW_DATA_PHENOTYPE_DATE_CORRECTION_DF[ which( RAW_DATA_PHENOTYPE_DATE_CORRECTION_DF$age == current_age &
                                                                                      RAW_DATA_PHENOTYPE_DATE_CORRECTION_DF$phenotype_name == current_phenotype),]
  # -- Parse the list of correction and apply them to data
  for( correction_index in 1:nrow( correction_for_current_phenotype_age)){
    correction_age = correction_for_current_phenotype_age[ correction_index, "age"]
    correction_phenotype = correction_for_current_phenotype_age[ correction_index, "phenotype_name"]
    correction_date = correction_for_current_phenotype_age[ correction_index, "date"]
    correction_value = correction_for_current_phenotype_age[ correction_index, "value.correction"]
    
    index_to_correct = which( current_df$age == correction_age &
                              current_df$phenotype_name == correction_phenotype &
                              current_df$date == correction_date)
    
    current_df[ index_to_correct, "value"] = current_df[ index_to_correct, "value"] - correction_value
  }
  
  # -- build the plot of the values without outliers and with date correction as boxplot per strain
  nooutliers_corrected_values_plot = ggplot( data = current_df, aes( strain_number, value, color=strain_number)) + 
                          geom_boxplot() +
                          stat_summary(fun.y=mean, colour="red", geom="point", size=1,show.legend = FALSE) +
                          stat_summary(fun.data = n_count_2, geom = "text", size = 1, angle=90, hjust = 0) +
                          theme( legend.position= "none") + theme(axis.text.x = element_text(size = 3, angle = 90, hjust = 1)) +
                          ggtitle( paste( "Date corrected data for phenotype", current_phenotype)) + 
                          xlab("strain")


  # -- display the three above plots
  # print( plot_grid( all_values_plot, nooutliers_values_plot, nooutliers_corrected_values_plot, labels = c("A", "B", "C"), nrow = 3, align = "v"))
  print( all_values_plot)
  print( nooutliers_values_plot)
  print( nooutliers_corrected_values_plot)

	# If date correction is required, data without outliers and with control correction are used to compute the mean 
	#(see MEAN_DF computation at the end of the script)
	if( PHENOTYPE_CORRECTION_MODE == "DATE_CORRECTION"){
    DATA_TO_USE_LONG_DATA_DF[[ current_age]] = rbind( DATA_TO_USE_LONG_DATA_DF[[ current_age]], current_df)
	}
}

# Finalize the dataframe containing values to use for mean and CV computation
names( DATA_TO_USE_LONG_DATA_DF[[ current_age]]) = names( ALL_DATA_DF)

# Build the wide version of the previous dataframe
DATA_TO_USE_WIDE_DATA_DF[[ current_age]] = reshape( DATA_TO_USE_LONG_DATA_DF[[ current_age]], v.names = "value", idvar = "individual_name", timevar = "phenotype_name", direction = "wide")
names( DATA_TO_USE_WIDE_DATA_DF[[ current_age]]) = unlist( sapply( names( DATA_TO_USE_WIDE_DATA_DF[[ current_age]]), function( name){
  if( grepl( "value.", name)){
    return( substr( name, start = 7, stop = nchar( name)))
  }else{
    return ( name)
  }
}), use.names = FALSE)

# Write the selected data of the phenotypes to file
base_output_file_path = file.path( OUTPUT_DIR, tools::file_path_sans_ext( basename( phenotype_data_input_file)))
write.table( DATA_TO_USE_WIDE_DATA_DF[[ current_age]], 
           file = file.path( paste0(base_output_file_path, "_",PHENOTYPE_CORRECTION_MODE, "_", current_age, "W.txt")), quote=FALSE, row.names=FALSE, col.names=TRUE, sep=",")

# ..................................................................
#
# Build the dataframe containing the mean of the phenotype by strain
#
# ..................................................................

MEAN_DF[[ current_age]] = data.frame( do.call("rbind",
                                              
            by( DATA_TO_USE_WIDE_DATA_DF[[ current_age]], DATA_TO_USE_WIDE_DATA_DF[[ current_age]][, INDIVIDUAL_STRAIN], function( by_df){
              
              # -- get the current strain name
              strain_number = unique( by_df[ , INDIVIDUAL_STRAIN])
              if( length( strain_number) != 1){
                stop( paste( "ERROR :: analysis_describe_strain_phenotype : there is many strains mixed : ", paste( strain_number, collapse =",")))
              }
              current_strain = strain_number[1]
              
              # -- get the ages
              age_set = sort( unique( by_df[ , INDIVIDUAL_AGE]))
              if( length( age_set) != 1){
                stop( paste( "ERROR :: analysis_describe_strain_phenotype : there is many ages mixed : ", paste( age_set, collapse =",")))
              }
              mean_current_age = age_set[1]
              
              # -- get the mean of values
              phenotype_mean = vector()
              for( current_phenotype in PHENOTYPE_SET){
                no_na_values = na.omit( by_df[ ,current_phenotype])
                if( length( no_na_values) >= 7){
                  values_mean = mean( no_na_values)
                }else{
                  values_mean = NA
                }
                phenotype_mean = append( phenotype_mean, values_mean)
              }
              
              return( c( current_strain, mean_current_age, phenotype_mean))
            })
), stringsAsFactors = FALSE)

# Finalized the dataframe with computed means
names( MEAN_DF[[ current_age]]) = c( "strain_name", "age", PHENOTYPE_SET)
for( phenotype in PHENOTYPE_SET){
	MEAN_DF[[ current_age]][ ,phenotype] = as.numeric( as.character( MEAN_DF[[ current_age]][ , phenotype]))
}

# Extract the information on strin/phenotype with not computed means (due to not enough values)
retiered_strain_phenotypes = data.frame()
for( phenotype in PHENOTYPE_SET){
  for( strain in row.names( MEAN_DF[[ current_age]])){
    if( is.na( MEAN_DF[[ current_age]][ strain, phenotype])){
      retiered_strain_phenotypes = rbind( retiered_strain_phenotypes, data.frame( age=current_age, strain=strain, phenotype=phenotype))
    }
  }
}
datatable( MEAN_DF[[ current_age]], caption="Datatable of computed means per phenotype and per line")
datatable( retiered_strain_phenotypes, caption="Strain/phenotype combinaison with to few values to compute MEAN statistics")

# ..................................................................
#
# Build the dataframe containing the CV of the phenotype by strain
#
# ..................................................................
CV_DF[[ current_age]] = data.frame( do.call("rbind",
			
			by( DATA_TO_USE_WIDE_DATA_DF[[ current_age]], DATA_TO_USE_WIDE_DATA_DF[[ current_age]][, INDIVIDUAL_STRAIN], function( by_df){
						
						# -- get the current strain name
						strain_number = unique( by_df[ , INDIVIDUAL_STRAIN])
						if( length( strain_number) != 1){
							stop( paste( "ERROR :: analysis_describe_strain_phenotype : there is many strains mixed : ", paste( strain_number, collapse =",")))
						}
						current_strain = strain_number[1]
						
						# -- get the ages
						age_set = sort( unique( by_df[ , INDIVIDUAL_AGE]))
						if( length( age_set) != 1){
							stop( paste( "ERROR :: analysis_describe_strain_phenotype : there is many ages mixed : ", paste( age_set, collapse =",")))
						}
						cv_current_age = age_set[1]
						
						# -- get the CV of values
						phenotype_cv = vector()
						for( current_phenotype in PHENOTYPE_SET){
							no_na_values = na.omit( by_df[ ,current_phenotype])
							if( length( no_na_values) >= 7){
								values_cv = sd( no_na_values) / mean( no_na_values)
							}else{
								values_cv = NA
							}
							phenotype_cv = append( phenotype_cv, values_cv)
						}
						
						return( c( current_strain, cv_current_age, phenotype_cv))
					})
	), stringsAsFactors = FALSE)  

# Finalized the dataframe with computed CV
names( CV_DF[[ current_age]]) = c( "strain_name", "age", PHENOTYPE_SET)
for( phenotype in PHENOTYPE_SET){
  CV_DF[[ current_age]][ ,phenotype] = as.numeric( as.character( CV_DF[[ current_age]][ , phenotype]))
}

# Extract the information on strain/phenotype with not computed CV (due to not enough values)
retiered_strain_phenotypes = data.frame()
for( phenotype in PHENOTYPE_SET){
  for( strain in row.names( CV_DF[[ current_age]])){
    if( is.na( CV_DF[[ current_age]][ strain, phenotype])){
      retiered_strain_phenotypes = rbind( retiered_strain_phenotypes, data.frame( age=current_age, strain=strain, phenotype=phenotype))
    }
  }
}
datatable( CV_DF[[ current_age]], caption="Datatable of computed CV per phenotype and per line")
datatable( retiered_strain_phenotypes, caption="Strain/phenotype combinaison with to few values to compute CV statistics")

