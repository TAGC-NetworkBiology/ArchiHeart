# ######################################################################################################
# This script aims to analyse the control strain in order to evaluate the values to keep for 
# next analysis analysis
# ######################################################################################################

library( ggplot2)

control_all_data_df = ALL_DATA_DF[ which( ALL_DATA_DF[ , INDIVIDUAL_STRAIN] %in% control_strain_set),]
control_all_data_df[ ,"yeardate"] = as.character( convert_dates( control_all_data_df[ , INDIVIDUAL_DATE]))

# Initialize the dataframe that will contain the phenotype correction
phenotype_correction = data.frame( age = character(),
                                    phenotype_name = character(),
                                    date = character(),
                                    yeardate = character(),
                                    correction = character(), 
                                    stringsAsFactors=FALSE) 

# initialize the vector that will contain all the outliers indexes
all_outliers_global_indexes = vector()

# Look at the distributions for each age
for( current_age in AGE_SET){
  
  
  cat("\n##########################")
  cat("\n AGE", current_age, "W")
  cat("\n##########################")
  
  # Make report for each phenotype
  for( current_phenotype in PHENOTYPE_SET){
    
    cat("\n----------------------------------------------")
    cat("\n PHENOTYPE-----", current_phenotype)
    cat("\n----------------------------------------------")
    
    # Get the values for the current phenotype and current age
    current_pheno_age_df = control_all_data_df[ which( control_all_data_df[ ,PHENOTYPE_NAME] == current_phenotype &
                                                         control_all_data_df[ , INDIVIDUAL_AGE] == current_age), ]
    
    # ---------------------------
    # STUDY WITH ALL THE VALUES
    # ---------------------------
    
    # -- plot the phenotype values, first classified by date, then through all the dates
    plots = list()
    
    plots[[ 1]] = ggplot( data = current_pheno_age_df, aes( yeardate, value, color=yeardate)) + 
                                geom_boxplot() +
                                theme( legend.position= "none") + theme(axis.text.x = element_text(size = 3, angle = 90, hjust = 1))+
                                ggtitle( paste( "All control data for phenotype\n", current_phenotype)) + 
                                xlab("Date")
    
    plots[[ 2]] = ggplot( data = current_pheno_age_df, aes( strain_number, value)) + 
                                        geom_boxplot() +
                                        theme( legend.position= "none") +
                                        ggtitle( paste( "All control data for phenotype\n", current_phenotype)) + 
                                        xlab("Strain")
    
    # -- compute an anova test on a linear model to look at the effect of date
    cat("\n-------------------------------")
    cat("\n Model with raw values")
    cat("\n-------------------------------\n")
    print( summary( current_pheno_age_df))
    model = lm( value ~ yeardate, data = current_pheno_age_df)
    cat("\nSummary of anova test of model 'value ~ yeardate'\n")
    anova_test = aov( model)
    print( summary( anova_test))
    cat("\nSummary of Cook distances for model\n")
    cook_distances = cooks.distance( model)
    print( summary( cook_distances))
    
    # -----------------------------
    # STUDY WITH NO OUTLIERS VALUES
    # -----------------------------
    
    # -- get the outliers indexes and restrict the studied values to the non-outliers
    outlier_indexes = get_15IQR_outliers_indexes( current_pheno_age_df$value)
    if( length( outlier_indexes) > 0){
      current_filtered_pheno_age_df = current_pheno_age_df[-outlier_indexes,]
    }else{
      current_filtered_pheno_age_df = current_pheno_age_df
    }
    
    # -- plot the phenotype values (with no outliers), first classified by date, then through all the dates
    plots[[ 3]] = ggplot( data = current_filtered_pheno_age_df, aes( yeardate, value, color=yeardate)) + 
      geom_boxplot() +
      theme( legend.position= "none") + theme(axis.text.x = element_text(size = 3, angle = 90, hjust = 1))+
      ggtitle( paste( "Control data (no outliers) for phenotype\n", current_phenotype)) + 
      xlab("Date")
    
    plots[[ 4]] = ggplot( data = current_filtered_pheno_age_df, aes( strain_number, value)) + 
      geom_boxplot() +
      theme( legend.position= "none") +
      ggtitle( paste( "Control data (no outliers) for phenotype\n", current_phenotype)) + 
      xlab("Strain")
    
    # -- compute an anova test on a linear model to look at the effect of date
    cat("\n-------------------------------")
    cat("\n Model with no outliers values")
    cat("\n-------------------------------")
    cat("\nNumber of outliers values:", length( outlier_indexes),"\n")
    print( summary( current_filtered_pheno_age_df))
    model_nooutliers = lm( value ~ yeardate, data = current_filtered_pheno_age_df)
    cat("\nSummary of anova test of model 'value ~ yeardate'\n")
    anova_test_nooutliers = aov( model_nooutliers)
    print( summary( anova_test_nooutliers))
    current_anova_pval = summary( anova_test_nooutliers)[[1]][1,5]
    cat("\nSummary of Cook distances for model\n")
    cook_distances_nooutliers = cooks.distance( model_nooutliers)
    print( summary( cook_distances_nooutliers))

    # -- test if the model report a significant effect of data on phenotype value
    if( current_anova_pval < 0.05){
      cat("\n The data is has a SIGNIFICANT effect on", current_phenotype, "values => values will be fixed")
    }else{
      cat("\n The data is has a no significant effect on", current_phenotype, "values")
    }
    
    # -- plot the graph that permit to estimate the validity of the linear model
    old_par = par
    par(mfrow = c(2, 2), oma = c(0, 0, 0, 0))
    plot( anova_test_nooutliers, which = 1)
    plot( density( residuals(anova_test_nooutliers)), main="Residual distribution")
    xnorm = seq( min( residuals(anova_test_nooutliers)),max( residuals(anova_test_nooutliers)),length=1000)
    lines( xnorm, dnorm(xnorm,mean=mean( residuals(anova_test_nooutliers)), sd=sd(residuals(anova_test_nooutliers))), col="red")
    plot( anova_test_nooutliers, which = 2)
    plot( anova_test_nooutliers, which = 4)
    par = old_par
    
    # --------------------------------------------
    # STUDY WITH NO OUTLIERS AND CORRECTED VALUES
    # --------------------------------------------
    
    # -- prepare the columns that will contain the correction to apply and the corrected values
    current_filtered_pheno_age_df$corrected.value = current_filtered_pheno_age_df$value
    current_filtered_pheno_age_df$value.correction = rep( 0, nrow( current_filtered_pheno_age_df))
    
    # -- correct the values of the phenotype using the linear model residus
    corrections_set = model_nooutliers[[1]]
    for( yeardate_index in 2:length( corrections_set)){
      current_yeardate = gsub( "yeardate", "", names( corrections_set[ yeardate_index]))
      current_correction = corrections_set[ yeardate_index]
      index_to_correct = which( current_filtered_pheno_age_df$yeardate == current_yeardate
                                & current_filtered_pheno_age_df$age == current_age
                                & current_filtered_pheno_age_df$phenotype_name == current_phenotype)
      current_filtered_pheno_age_df[ index_to_correct, "value.correction"] = current_correction
      current_filtered_pheno_age_df[ index_to_correct, "corrected.value"] = current_filtered_pheno_age_df[ index_to_correct, "value"] - current_correction
    }
    # -- get the information on correction per date only
    extracted_correction_per_phenotype_and_age = current_filtered_pheno_age_df[ ,c("age", "phenotype_name", "date", "yeardate", "value.correction")]
    # -- remove the duplicate lines in order to keep oneline per age/phenotype/date/correction
    extracted_correction_per_phenotype_and_age =extracted_correction_per_phenotype_and_age[ !duplicated(extracted_correction_per_phenotype_and_age), ]
    # -- accumulate the phenotype correction through phenotypes in a single dataframe
    phenotype_correction = rbind( phenotype_correction, extracted_correction_per_phenotype_and_age)

    # -- plot the phenotype values (with no outliers and corrected), first classified by date, then through all the dates
    plots[[ 5]] = ggplot( data = current_filtered_pheno_age_df, aes( yeardate, corrected.value, color=yeardate)) + 
      geom_boxplot() +
      theme( legend.position= "none") + theme(axis.text.x = element_text(size = 3, angle = 90, hjust = 1))+
      ggtitle( paste( "Control data (no outliers & fixed)\nfor phenotype", current_phenotype)) + 
      xlab("Date")
    
    plots[[ 6]] = ggplot( data = current_filtered_pheno_age_df, aes( strain_number, corrected.value)) + 
      geom_boxplot() +
      theme( legend.position= "none") +
      ggtitle( paste( "Control data (no outliers & fixed)\nfor phenotype", current_phenotype)) + 
      xlab("Strain")
    
    # -----------------------------
    # FINALISATION
    # -----------------------------
    
    # Print the boxplots of values that were prepared in the previous steps
    multiplot( plots, ncols=2, nrows=3)

    # Memorize the list of outliers
    for( outlier_index in outlier_indexes){
      current_individual = current_pheno_age_df[ outlier_index, PHENOTYPE_INDIVIDUAL]
      outlier_global_index = which( RAW_DATA_PHENOTYPE_DF[, PHENOTYPE_INDIVIDUAL] == current_individual &
                                    RAW_DATA_PHENOTYPE_DF[, PHENOTYPE_NAME] == current_phenotype &
                                    RAW_DATA_PHENOTYPE_DF[, PHENOTYPE_AGE] == current_age)
      if( length( outlier_global_index) != 1){
        stop( paste( "Error while filtering phenotype data for individual", current_individual, ": corresponding values in raw data = ", length( outlier_global_index)))
      }
      all_outliers_global_indexes = append( all_outliers_global_indexes, outlier_global_index)
    }
  }
  
}

# Build the output file base name
base_output_file_path = file.path( OUTPUT_DIR, tools::file_path_sans_ext( basename( phenotype_data_input_file)))

# Export the correction to apply to phenotypes/age according to date
write.table( phenotype_correction, file=paste0( base_output_file_path, "_date_correction.csv"), col.names=TRUE, row.names=FALSE, sep="\t", quote = FALSE)

# Build the final global dataframe ignoring the outliers values for each phenotype
if( length( all_outliers_global_indexes) > 0){
  RAW_DATA_PHENOTYPE_FILTERED_CONTROL_DF = RAW_DATA_PHENOTYPE_DF[ -all_outliers_global_indexes,]
}else{
  RAW_DATA_PHENOTYPE_FILTERED_CONTROL_DF = RAW_DATA_PHENOTYPE_DF
}
write.table( RAW_DATA_PHENOTYPE_FILTERED_CONTROL_DF, file=paste0( base_output_file_path, "_control_nooutliers.csv"), col.names=TRUE, row.names=FALSE, sep="\t", quote = FALSE)
    