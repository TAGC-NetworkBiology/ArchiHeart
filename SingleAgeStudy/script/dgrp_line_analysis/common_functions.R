
## @knitr load_common_functions

cat("<BR>")

# ##########################################################################################
# Compute the genetic broad-sense heritability of trait with or without the correction
# from the Wolbachia contamination
# ##########################################################################################
# Given a population where each genotype is phenotyped for a number of genetically identical replicates 
# (either individual plants or plots in a field trial), the repeatability or intra-class correlation can be 
# estimated by V_g / (V_g + V_e), where V_g = (MS(G) - MS(E)) / r and V_e = MS(E). In these expressions, 
# r is the number of replicates per genotype, and MS(G) and MS(E) are the mean sums of squares for genotype 
# and residual error obtained from analysis of variance. In case MS(G) < MS(E), V_g is set to zero. 
# See Singh et al. (1993) or Lynch and Walsh (1998), p.563. When the genotypes have differing numbers of replicates,
# r is replaced by \bar r = (n-1)^{-1} (R_1 - R_2 / R_1), where R_1 = ∑ r_i and R_2 = ∑ r_i^2. 
# Under the assumption that all differences between genotypes are genetic, repeatability equals broad-sense 
# heritability; otherwise it only provides an upper-bound for broad-sense heritability. 
compute_heritability <- function( heritability_df, correction=FALSE, analyzed_data_name= "INDIVIDUALS"){  
  
  # Get the list of strain and change "dgrp" in their name to "line_"
  strain_set = heritability_df$strain_number
  strain_set = unlist( lapply( strain_set, function( x){
    return( gsub ("dgrp", "line_", x, ignore.case = TRUE))
  }))
  heritability_df$strain.set = strain_set
  heritability_df$value = as.numeric( heritability_df$value)
  
  if( analyzed_data_name == "INDIVIDUALS"){
    
    # First compute the H2 with homemade script
    # .........................................
    # Compute the mean number of replicates through the genotypes
    n.rep.vector <- as.integer(table(heritability_df$strain.set))
    average.number.of.replicates <- (sum(n.rep.vector) - sum(n.rep.vector^2)/sum(n.rep.vector))/(length(n.rep.vector) - 1)
    # Compute the anova of phenotype values versus strains
    anova_result = anova( lm( value ~ strain.set, data= heritability_df))
    # Extract the genotype variance and environmental variance (residual variance)
    gen.variance <- max( 0, (anova_result[[3]][1] - anova_result[[3]][2])/average.number.of.replicates)
    res.variance <- anova_result[[3]][2]
    homemade_computed_H2 = gen.variance/(gen.variance + res.variance)
    
    # Then compute the H2 with external script
    # .........................................
    external_computed_heritability  = repeatability( data.vector = heritability_df$value, geno.vector = strain_set)
    external_compute_H2 = external_computed_heritability$repeatability
    external_computed_H2_CI = paste( signif( external_computed_heritability$conf.int,3) , collapse=";")
    external_computed_H2_mean_replicates = external_computed_heritability$average.number.of.replicates
    
    result = data.frame( gen.variance = signif( gen.variance, 3),
                         env.variance = signif( res.variance, 3),
                         phenotype.variance =  signif( gen.variance + res.variance, 3),
                         H2.homemade = signif( homemade_computed_H2, 3),
                         H2.external = signif( external_compute_H2, 3),
                         H2.CI.external = external_computed_H2_CI,
                         H2.mean.replicates.external = signif( external_computed_H2_mean_replicates, 4))
    
    # if( correction){
    #   # Get the wolbachia covariable with the same rows as data
    #   cov_df = data.frame( cov.wol = WOLBACHIA_COVARIABLE_DF[ strain_set, ])
    #   row.names( cov_df) = row.names( heritability_df)
    #   
    #   # Build a datframe with phenotype value and worlbachia covariable for model building
    #   model_df = data.frame( name = heritability_df$individual_name, value = as.numeric( heritability_df$value), cov = cov_df[,1])
    #   model_df$cov=as.factor( model_df$cov)  
    #   model = lm( value ~ cov, data = model_df)  
    #   
    #   # Get the correction due to Wolbachia
    #   cov_correction = summary( model)$coefficients[2,1]
    #   
    #   # Apply the correction to suitable data lines
    #   cov1_index_set = which( model_df$cov == 1)
    #   model_df[ cov1_index_set, "value"] = model_df[ cov1_index_set, "value"] - cov_correction
    #   
    #   # Compute the H2 index with the correction
    #   external_computed_corrected_heritability = repeatability( data.vector = as.numeric( model_df$value),
    #                                       geno.vector = as.factor( strain_set))
    #   external_compute_corrected_H2 = external_computed_corrected_heritability$repeatability
    #   external_computed_corrected_H2_CI = paste( external_computed_corrected_heritability$conf.int, collapse=";")
    #   external_computed_corrected_H2_mean_replicates = external_computed_corrected_heritability$average.number.of.replicates
    #   
    #   result = cbind( result, data.frame( H2.external.corrected = external_compute_corrected_H2,
    #                                       H2.CI.external.corrected = external_computed_corrected_H2_CI,
    #                                       H2.mean.replicates.external.corrected = external_computed_corrected_H2_mean_replicates))
    # }
  }
  
  return( result)
}


# ##########################################################################################
# Define function providing names of files exported during the analysis pipeline
# ##########################################################################################

# Provide the name of the file containing the mean of phenotype for each strains at a given age
get_phenotype_stat_file <- function( output_dir, phenotype, age, data_type){
  file_name = paste0( PHENOTYPE_MEAN_FILE_PREFIX, "_", phenotype, "_", age, "W_", data_type, ".txt")
  if( is.null( output_dir)){
    return( file_name)
  }else{
    return( file.path( output_dir, file_name))
  }
}

# # Provide the name of the file containing the list of strains available in phenotype data at a given age
# get_age_families_file <- function( output_dir, age){
#   return( file.path( output_dir, paste0( AGE_FAMILIES_FILE_PREFIX, "_", age, "W.txt")))
# }

# Provide the name of the file containing the list of strains available in phenotype data at a given age
get_pheno_age_families_file <- function( output_dir, phenotype, age, data_type){
  return( file.path( output_dir, paste0( PHENOTYPE_MEAN_FILE_PREFIX, "_", phenotype, "_", AGE_FAMILIES_FILE_PREFIX, "_", age, "W_", data_type, ".txt")))
}

# ##########################################################################################
# plot a PNG image imported from external file
# ##########################################################################################

plotPNG <- function( image_path){
  
  # Load the PNG image
  img = readPNG( image_path)
  
  # Create a plot with no axes, no box and no label
  plot( 1:2, type='n',  xaxt='n',  yaxt='n', xlab="", ylab="", bty="n")
  
  # Raster the image to the plot
  rasterImage(img, 1, 1, 2, 2)
}

# ##########################################################################################
# Define a function that remove the values in a set that are outside the segment
# [ Q1 - 1.5*IQR ; Q3 + 1.5*IQR]
# ##########################################################################################

get_15IQR_outliers_indexes <- function(x, na_rm = TRUE) {
  qnt = quantile(x, probs=c(.25, .75), na.rm = na_rm)
  H = 1.5 * (qnt[2] - qnt[1])
  outliers_indexes = which( x < (qnt[1] - H) | x > (qnt[2] + H))
  return( outliers_indexes)
}


# ###########################################################################################
# Define a function that produces a pairwise scatterplot comparison with correlation
# computation using ggplot2
# ###########################################################################################

#define a helper function (borrowed from the "ez" package)
ezLev=function(x,new_order){
  for(i in rev(new_order)){
    x=relevel(x,ref=i)
  }
  return(x)
}

# define the main pairwise scatterplot function
ggcorplot = function(data,var_text_size,cor_text_limits){
  # normalize data
  for(i in 1:length(data)){
    data[,i]=(data[,i]-mean(data[,i]))/sd(data[,i])
  }
  # obtain new data frame
  z=data.frame()
  i = 1
  j = i
  while(i<=length(data)){
    if(j>length(data)){
      i=i+1
      j=i
    }else{
      x = data[,i]
      y = data[,j]
      temp=as.data.frame(cbind(x,y))
      temp=cbind(temp,names(data)[i],names(data)[j])
      z=rbind(z,temp)
      j=j+1
    }
  }
  names(z)=c('x','y','x_lab','y_lab')
  z$x_lab = ezLev(factor(z$x_lab),names(data))
  z$y_lab = ezLev(factor(z$y_lab),names(data))
  z=z[z$x_lab!=z$y_lab,]
  #obtain correlation values
  z_cor = data.frame()
  i = 1
  j = i
  while(i<=length(data)){
    if(j>length(data)){
      i=i+1
      j=i
    }else{
      x = data[,i]
      y = data[,j]
      x_mid = min(x)+diff(range(x))/2
      y_mid = min(y)+diff(range(y))/2
      this_cor = cor(x,y, method="spearman")
      this_cor.test = cor.test(x,y, method="spearman")
      this_col = ifelse(this_cor.test$p.value<.05,'<.05','>.05')
      this_size = (this_cor)^2
      cor_text = ifelse(
        this_cor>0
        ,substr(format(c(this_cor,0.123456789),digits=2)[1],1,4)
        ,paste('-',substr(format(c(this_cor,0.123456789),digits=2)[1],2,5),sep='')
      )
      b=as.data.frame(cor_text)
      b=cbind(b,x_mid,y_mid,this_col,this_size,names(data)[j],names(data)[i])
      z_cor=rbind(z_cor,b)
      j=j+1
    }
  }
  names(z_cor)=c('cor','x_mid','y_mid','p','rsq','x_lab','y_lab')
  z_cor$x_lab = ezLev(factor(z_cor$x_lab),names(data))
  z_cor$y_lab = ezLev(factor(z_cor$y_lab),names(data))
  diag = z_cor[z_cor$x_lab==z_cor$y_lab,]
  z_cor=z_cor[z_cor$x_lab!=z_cor$y_lab,]
  #start creating layers
  points_layer = layer(
    geom = 'point'
    , data = z
    , mapping = aes(
      x = x
      , y = y
    )
  )
  lm_line_layer = layer(
    geom = 'line'
    , geom_params = list(colour = 'red')
    , stat = 'smooth'
    , stat_params = list(method = 'lm')
    , data = z
    , mapping = aes(
      x = x
      , y = y
    )
  )
  lm_ribbon_layer = layer(
    geom = 'ribbon'
    , geom_params = list(fill = 'green', alpha = .5)
    , stat = 'smooth'
    , stat_params = list(method = 'lm')
    , data = z
    , mapping = aes(
      x = x
      , y = y
    )
  )
  cor_text = layer(
    geom = 'text'
    , data = z_cor
    , mapping = aes(
      x=y_mid
      , y=x_mid
      , label=cor
      , size = rsq
      , colour = p
    )
  )
  var_text = layer(
    geom = 'text'
    , geom_params = list(size=var_text_size)
    , data = diag
    , mapping = aes(
      x=y_mid
      , y=x_mid
      , label=x_lab
      , angle=-45
      
    )
  )
  f = facet_grid(y_lab~x_lab,scales='free')
  o = theme(
    panel.grid.minor = element_blank()
    ,panel.grid.major = element_blank()
    ,axis.ticks = element_blank()
    ,axis.text.y = element_blank()
    ,axis.text.x = element_blank()
    ,axis.title.y = element_blank()
    ,axis.title.x = element_blank()
    ,legend.position='none'
  )
  size_scale = scale_size(range = cor_text_limits)
  return(
    ggplot()+
      points_layer+
      lm_ribbon_layer+
      lm_line_layer+
      var_text+
      cor_text+
      f+
      o+
      size_scale+
      theme(strip.text.x = element_text(size = 5), strip.text.y = element_text(size = 5))
  )
}


# ###########################################################################################
# Define a function that count the number of element in the provided set of values
# and return a object able to be used with the stat_summary function of ggplot
# ###########################################################################################
n_count_1 <- function(x){
  return(data.frame(y = ypos_1, label = paste0( "", length(x))))
}
n_count_2 <- function(x){
  return(data.frame(y = ypos_2, label = paste0( "", length(x))))
}
