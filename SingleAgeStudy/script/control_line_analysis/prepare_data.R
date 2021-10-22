# #########################################################
# This script load the data from the given files and
# declare some constants
# #########################################################

source( file.path( SCRIPT_DIR, "common_functions.R"))


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

# Get the strains that are control strains and not control strains
not_control_strain_set = RAW_DATA_STRAIN_DF[ which( RAW_DATA_STRAIN_DF[ , STRAIN_CONTROL] == 0), STRAIN_NUMBER]
control_strain_set = RAW_DATA_STRAIN_DF[ which( RAW_DATA_STRAIN_DF[ , STRAIN_CONTROL] == 1), STRAIN_NUMBER]

# Get the name of individuals that are in control strains and non-control strains
not_control_individual_set = RAW_DATA_INDIVIDUAL_DF[ which( RAW_DATA_INDIVIDUAL_DF[ , INDIVIDUAL_STRAIN] %in% not_control_strain_set), INDIVIDUAL_NAME]
control_individual_set = RAW_DATA_INDIVIDUAL_DF[ which( RAW_DATA_INDIVIDUAL_DF[ , INDIVIDUAL_STRAIN] %in% control_strain_set), INDIVIDUAL_NAME]

# Get the list of available ages
AGE_SET = sort( unique( RAW_DATA_INDIVIDUAL_DF[, INDIVIDUAL_AGE]))

# Make plots of phenotype data through dates
PHENOTYPE_SET = sort( unique( RAW_DATA_PHENOTYPE_DF[ , PHENOTYPE_NAME]))
PHENOTYPE_SET = PHENOTYPE_SET[ which( PHENOTYPE_SET != "Pcent_DI_sup3")]



# Merge de raw df to get a complete information
ALL_DATA_DF = merge( RAW_DATA_PHENOTYPE_DF[ , c(PHENOTYPE_NAME, PHENOTYPE_VALUE, PHENOTYPE_INDIVIDUAL, PHENOTYPE_AGE)], 
                     RAW_DATA_INDIVIDUAL_DF[ c( INDIVIDUAL_DATE, INDIVIDUAL_NAME, INDIVIDUAL_STRAIN)], 
                     by.x=PHENOTYPE_INDIVIDUAL, by.y=INDIVIDUAL_NAME)

lockBinding("RAW_DATA_STRAIN_DF", globalenv())
lockBinding("RAW_DATA_INDIVIDUAL_DF", globalenv())
lockBinding("RAW_DATA_PHENOTYPE_DF", globalenv())
lockBinding("AGE_SET", globalenv())
lockBinding("ALL_DATA_DF", globalenv())

