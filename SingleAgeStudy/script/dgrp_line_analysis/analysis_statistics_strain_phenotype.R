# #######################################################################
# This script aims to provide complete statistics on phenotype, both
# at the level of all strains that at the level of each strain.
# #######################################################################

## @knitr statistics_phenotypes

SUMMARIZED_STATISTICS[[ current_age]] = data.frame()

dt_list = list()
for( current_phenotype in PHENOTYPE_SET){
  
  cat("<BR><H5>", current_phenotype, "</H5>")
  
  # Look at behavior of individual values
  # -- get all the DGRP values for the current age and phenotype
  current_df = DATA_TO_USE_LONG_DATA_DF[[ current_age]][ which( DATA_TO_USE_LONG_DATA_DF[[ current_age]]$strain_number %in% not_control_strain_set &
                                                                  DATA_TO_USE_LONG_DATA_DF[[ current_age]]$phenotype_name == current_phenotype &
                                                                  !is.na( DATA_TO_USE_LONG_DATA_DF[[ current_age]]$value)
  ), ]
  
  # -- get the strains that have a non NA value mean
  strains_with_means = MEAN_DF[[ current_age]][ which( !is.na( MEAN_DF[[ current_age]][, current_phenotype])), "strain_name"]
  
  # -- keep in the value dataframe only the strains with non-NA value mean
  filtered_current_df = current_df[ which( current_df$strain_number %in% strains_with_means), ]
  
  # -- order the strains by increasing means and remove the NA means
  ordered_strains = MEAN_DF[[ current_age]]$strain_name[ order( MEAN_DF[[ current_age]][, current_phenotype])]
  ordered_strains = intersect( ordered_strains, strains_with_means)
  
  # -- convert the strain column to a factor with correct order (for the ggplot)
  filtered_current_df$strain_number = factor(filtered_current_df$strain_number, levels = ordered_strains, ordered = TRUE)
  
  # -- create the boxplots of phenotype values of line ordered by increasing means
  plot_by_increasing_means = ggplot( filtered_current_df, aes( strain_number, value, color=strain_number)) + 
    geom_boxplot() +
    stat_summary(fun.y=mean, colour="red", geom="point", size=1,show.legend = FALSE) +
    theme( legend.position= "none") + theme(axis.text.x = element_text(size = 3, angle = 90, hjust = 1)) +
    ggtitle( paste( "Phenotype values ordered by strain mean<BR>", current_phenotype)) + 
    xlab("strain")
  
  # Look at behavior of mean and CV values
  # -- get the mean values of the current phenotype
  current_mean_df = MEAN_DF[[current_age]][ , c( "strain_name", "age", current_phenotype)]
  names( current_mean_df) = c( "strain_number", "age", "value")
  current_mean_df = current_mean_df[ which( !is.na( current_mean_df$value)),]
  
  # -- get the CV values of the current phenotypes
  current_cv_df = CV_DF[[current_age]][ , c( "strain_name", "age", current_phenotype)]
  names( current_cv_df) = c( "strain_number", "age", "value")
  current_cv_df = current_cv_df[ which( !is.na( current_cv_df$value)),]
  
  # -- create the boxplot of phenotype line CV values
  boxplot_of_CV_values = ggplot( current_cv_df) +
    geom_violin( aes( x=current_phenotype, y=value)) +
    geom_jitter( aes( x=current_phenotype, y=value), alpha = 0.5, width = .1) +
    ggtitle( paste( "Distribution of CV value for\n", current_phenotype)) +
    xlab( current_phenotype) + ylab( "Phenotype CV") +
    theme(axis.title.x=element_blank(), axis.text.x=element_blank(), axis.ticks.x=element_blank())
  
  # -- create the scatterplot of phenotype line mean against phenotype line CV values		
  mean_cv_df = merge( current_mean_df, current_cv_df, by = "strain_number")
  scatterplot_of_mean_and_CV = ggplot( mean_cv_df) +
    geom_point( aes( x=value.x, y=value.y)) +
    ggtitle( paste( "Correlation of MEAN and CV value for\n", current_phenotype)) + 
    xlab( "Phenotype mean") + ylab( "Phenotype CV")
  
  # Print the plots: in large the plot by increasing mean
  # side-by-side the plots of CV distribution (boxplot) and the plot of mean by CV correlation
  print( plot_by_increasing_means)
  print( plot_grid( boxplot_of_CV_values, scatterplot_of_mean_and_CV,
                    labels = c('', '', ''), ncol = 2, align = 'h'))
  
  # Compute correlation between mean and cv accross lines
  correlation_mean_cv = cor( mean_cv_df$value.x, mean_cv_df$value.y, method="spearman")
  cat("<BR> Correlation between MEAN and CV for", current_phenotype, ":", correlation_mean_cv)
  
  # Compute broad sense heritability on data
  heritability = compute_heritability( filtered_current_df)
  
  # Compute effect of covariables
  anova_df = cbind( current_mean_df, ALL_COVARIABLES_DF[ gsub( "dgrp", "line_", current_mean_df$strain_number),])
  dt_list[[ current_phenotype]] = datatable( as.data.frame( anova( lm( paste0( "value~", paste( names( ALL_COVARIABLES_DF), collapse="+")), data=anova_df))),
             caption= paste("Covariable effect on", current_phenotype))
  
  # Put all the statistics information in a single dataframe
  current_statsitics_df = data.frame( total.nb.lines = length( unique(current_df$strain_number)),
                                           total.nb.individuals = length( unique(current_df$individual_name)),
                                           total.mean = signif( mean( filtered_current_df$value), 4),
                                           total.sd = signif( sd( filtered_current_df$value) ,4),
                                           total.cv = signif( sd( filtered_current_df$value) / mean( filtered_current_df$value), 4),
                                           nb.used.lines.for.mean = length( unique( current_mean_df$strain_number)),
                                           nb.used.individuals.for.mean = length( unique( filtered_current_df[, "individual_name"])),
                                           nb.used.lines.for.cv = length( unique( current_cv_df$strain_number)),
                                           nb.used.individuals.for.cv = length( unique( filtered_current_df[, "individual_name"])),
                                           cor.mean.cv = signif( correlation_mean_cv, 4)
                                      )
  current_statsitics_df = cbind( current_statsitics_df, heritability)
  SUMMARIZED_STATISTICS[[ current_age]] = rbind( SUMMARIZED_STATISTICS[[ current_age]], current_statsitics_df)
}

# Add the names of phenotypes as row names of the summarized statistics dataframe
row.names( SUMMARIZED_STATISTICS[[ current_age]]) = PHENOTYPE_SET

# Display the summarized statistics table for all phenotypes and prefered phenotypes
datatable( SUMMARIZED_STATISTICS[[ current_age]], caption= paste( "Summarized statistics at age", current_age))
datatable( t( SUMMARIZED_STATISTICS[[ current_age]][ PREFERED_PHENOTYPE_SET, ]), 
           caption= paste( "Summarized statistics at age", current_age, "\nfor selected phenotypes"),
           options = list( pageLength = ncol( SUMMARIZED_STATISTICS[[ current_age]]), ordering=F),
           height=810, width=800)

htmltools::tagList( dt_list)
