# #########################################################
# This script load the data from the given files and
# declare some constants
# #########################################################


## @knitr load_data

# Path to the output folder for GWAS files
GWAS_OUTPUT_SUBFOLDER = "gwas"
GWAS_RESULT_OUTPUT_SUBFOLDER = paste( GWAS_OUTPUT_SUBFOLDER, "result", sep="")
EPISTASIS_OUTPUT_SUBFOLDER = "epistasis"

# Some string constant used to build filenames at various stages of the pipeline
PHENOTYPE_MEAN_FILE_PREFIX = "phenotype"
AGE_FAMILIES_FILE_PREFIX = "age_families"

# Load the data containing the definition of strains
# Headers:
STRAIN_CONTROL = "control" #control BOOLEAN
STRAIN_NUMBER = "number" #number VARCHAR

RAW_DATA_STRAIN_DF = read.table( strain_input_file, stringsAsFactors = FALSE, header = TRUE, sep="\t")

# Load the data containing the definition of individual drome
# Headers : 
INDIVIDUAL_NAME = "name" #name VARCHAR 
INDIVIDUAL_ID = "id" #id INTEGER
INDIVIDUAL_DATE = "date" #date VARCHAR
INDIVIDUAL_AGE = "age" #age INTEGER
INDIVIDUAL_SEX = "sex" #sex VARCHAR
INDIVIDUAL_USER = "user" #user VARCHAR
INDIVIDUAL_STRAIN = "strain_number" #strain_number VARCHAR

RAW_DATA_INDIVIDUAL_DF = read.table( individual_input_file, stringsAsFactors = FALSE, header = TRUE, sep="\t")

# Load the data containing the definition of phenotype data
# Headers : 
PHENOTYPE_NAME = "phenotype_name" #phenotype_name VARCHAR
PHENOTYPE_VALUE = "value" #value FLOAT
PHENOTYPE_AGE = "age" #age INTEGER 
PHENOTYPE_INDIVIDUAL = "individual_name" #individual_name VARCHAR

RAW_DATA_PHENOTYPE_DF = read.table( phenotype_data_input_file, stringsAsFactors = FALSE, header = TRUE, sep="\t")

# Load the data containing the correction to apply to phenotype according to date
RAW_DATA_PHENOTYPE_DATE_CORRECTION_DF = read.table( date_correction_file, stringsAsFactors = FALSE, header = TRUE, sep="\t")

# Get the strains that are control strains and not control strains
not_control_strain_set = RAW_DATA_STRAIN_DF[ which( RAW_DATA_STRAIN_DF[ , STRAIN_CONTROL] == 0), STRAIN_NUMBER]
control_strain_set = RAW_DATA_STRAIN_DF[ which( RAW_DATA_STRAIN_DF[ , STRAIN_CONTROL] == 1), STRAIN_NUMBER]

# Get the name of individuals that are in control strains and non-control strains
not_control_individual_set = RAW_DATA_INDIVIDUAL_DF[ which( RAW_DATA_INDIVIDUAL_DF[ , INDIVIDUAL_STRAIN] %in% not_control_strain_set), INDIVIDUAL_NAME]
control_individual_set = RAW_DATA_INDIVIDUAL_DF[ which( RAW_DATA_INDIVIDUAL_DF[ , INDIVIDUAL_STRAIN] %in% control_strain_set), INDIVIDUAL_NAME]

# Get the list of available ages
AGE_SET = sort( unique( RAW_DATA_INDIVIDUAL_DF[, INDIVIDUAL_AGE]))

# Get the list of available phenotypes
PHENOTYPE_SET = sort( unique( RAW_DATA_PHENOTYPE_DF[ , PHENOTYPE_NAME]))
PHENOTYPE_SET = PHENOTYPE_SET[ which( PHENOTYPE_SET != "Pcent_DI_sup3")]

# Merge de raw df to get a complete information
ALL_DATA_DF = merge( RAW_DATA_PHENOTYPE_DF[ , c(PHENOTYPE_NAME, PHENOTYPE_VALUE, PHENOTYPE_INDIVIDUAL, PHENOTYPE_AGE)], 
                     RAW_DATA_INDIVIDUAL_DF[ c( INDIVIDUAL_DATE, INDIVIDUAL_NAME, INDIVIDUAL_STRAIN)], 
                     by.x=PHENOTYPE_INDIVIDUAL, by.y=INDIVIDUAL_NAME)

ALL_WIDE_DATA_DF = wide <- reshape(ALL_DATA_DF, v.names = "value", idvar = "individual_name", timevar = "phenotype_name", direction = "wide")

names( ALL_WIDE_DATA_DF) = unlist( sapply( names( ALL_WIDE_DATA_DF), function( name){
  if( grepl( "value.", name)){
    return( substr( name, start = 7, stop = nchar( name)))
  }else{
    return ( name)
  }
}), use.names = FALSE)

#
# Load the covariable data for Wolbachia contamination
# format: line_id line_id cov1
#
# -- Load the file with the first column as row names (line names)
temp_df = read.table( file=wolbachia_covariable_file, header=FALSE, row.names=1, sep="\t")
# -- remove the first column of the DF that is a repetition of the line names
rownames = row.names( temp_df)
WOLBACHIA_COVARIABLE_DF = data.frame( cov.wol = temp_df[ ,2])
row.names( WOLBACHIA_COVARIABLE_DF) = rownames

if( ncol( WOLBACHIA_COVARIABLE_DF) != 1){
  stop( "ERROR : The Wolbachia covariable file is not correctly formated. It should be formated like: line_id line_id cov1")
}

#
# Load the covariables data for all covariables
# format: line_id line_id cov1 cov2 cov3.... with 17 covariables
#
# -- load the file with the first column as row names (line names)
all_cov_temp_df = read.table( file=covariable_file, header=FALSE, row.names=1, sep="\t")
if( ncol( all_cov_temp_df) != 18){
  stop( "ERROR : The covariables file is not correctly formated. It should be formated like: line_id line_id cov1 cov2 cov3... with 17 covariables")
}
# -- Build a dataframe with suitables column names and row names
ALL_COVARIABLES_DF = data.frame( cov.wolbachia = all_cov_temp_df[ ,2])
for( inv_index in 1:16){
  ALL_COVARIABLES_DF[ , paste0( "cov.inv", inv_index)] = all_cov_temp_df[ , inv_index+1]
}
row.names( ALL_COVARIABLES_DF) = row.names( all_cov_temp_df)

# -- check if the resulting dataframe as the right number of colums
if( ncol( ALL_COVARIABLES_DF) != 17){
  stop( "ERROR : The covariables resulting dataframe is not correctly formated. It should be formated like: cov1 cov2 cov3... with 17 covariables")
}

#
# Fix the vairables
#
lockBinding("RAW_DATA_STRAIN_DF", globalenv())
lockBinding("RAW_DATA_INDIVIDUAL_DF", globalenv())
lockBinding("RAW_DATA_PHENOTYPE_DF", globalenv())
lockBinding("ALL_DATA_DF", globalenv())
lockBinding("ALL_WIDE_DATA_DF", globalenv())
lockBinding("AGE_SET", globalenv())
lockBinding("WOLBACHIA_COVARIABLE_DF", globalenv())
lockBinding("ALL_COVARIABLES_DF", globalenv())
lockBinding("ALL_COVARIABLES_DF", globalenv())

#
# Datatable on type of lines and on lines per age
#
cat("<H3>Statistics on strains used for analysis</H3>")
datatable( t( data.frame( Number.of.control.strains = length( RAW_DATA_STRAIN_DF[ which( RAW_DATA_STRAIN_DF[ , STRAIN_CONTROL] == 1), STRAIN_NUMBER]),
                          Number.of.DGRP.strains = length( not_control_strain_set))),
            colnames = " ",  options = list( pageLength = 2), height= 230,  width=400)

age_stat_datatable = data.frame()
for( age in AGE_SET){
  age_stat_datatable = rbind( age_stat_datatable, data.frame( age= age, 
                                                             strain.number=length( unique( RAW_DATA_INDIVIDUAL_DF[ which( 
                                                              RAW_DATA_INDIVIDUAL_DF[ , INDIVIDUAL_STRAIN] %in% not_control_strain_set
                                                              & RAW_DATA_INDIVIDUAL_DF[ , INDIVIDUAL_AGE] == age),
                                                              INDIVIDUAL_STRAIN]))
                                                             )
                      )
}
datatable( age_stat_datatable, options = list( pageLength = 2), height= 250,  width=400, rownames = FALSE)

#
# datatable of files and options used for analysis
#
cat("<H3>Files and options used for analysis</H3>")

datatable( t(data.frame(strain.input.file = strain_input_file,
                        individual.input.file = individual_input_file,
                        phenotype.data.input.file = phenotype_data_input_file,
                        covariable.file = covariable_file,
                        wolbachia.covariable.file = wolbachia_covariable_file,
                        phenotype.correction.mode = PHENOTYPE_CORRECTION_MODE,
                        gwas.transformation.mode = GWAS_TRANSFORMATION_MODE,
                        date.correction.file = date_correction_file)),
           colnames = c(" "), options = list( pageLength = 9), height=810, width=800)

