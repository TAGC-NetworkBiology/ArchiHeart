# ########################################################################
# This scripts launch the Sweave report that produces statistics on
# the various phenotypes at various ages.
# The data must be provided in a file given as argument when launching
# this script with Rscript command. The data file is classically produced
# from the SQlite DB by the python script launching this script.
# ########################################################################

library(knitr)

cat("\n-------------------------------")
cat("\nPreparing DGRP line Analysis")
cat("\n-------------------------------")

WORKING_DIR = getwd()

# Get the required variables from the snakemake rule
strain_input_file = file.path( WORKING_DIR, snakemake@input[[ "strain_data_file"]])
individual_input_file = file.path( WORKING_DIR, snakemake@input[[ "individual_data_file"]])
phenotype_data_input_file = file.path( WORKING_DIR, snakemake@input[[ "phenotype_data_file"]])

wolbachia_covariable_file = file.path( WORKING_DIR, snakemake@input[[ "wolbachia_covariable_file"]])
covariable_file = file.path( WORKING_DIR, snakemake@input[[ "covariables_file"]])

PREFERED_PHENOTYPE_SET = snakemake@params[[ "prefered_phenotypes"]]
PHENOTYPE_CORRECTION_MODE = snakemake@params[[ "phenotype_correction_mode"]]
GWAS_TRANSFORMATION_MODE = snakemake@params[[ "gwas_transformation_mode"]]

#phenotype_data_no_outlier_file = snakemake@input[[ "phenotype_data_no_outlier_file"]]
date_correction_file = file.path( WORKING_DIR, snakemake@input[[ "date_correction_file"]])

# Create the output folder
OUTPUT_DIR = file.path( WORKING_DIR, "output/3_dgrp_line_analysis")
dir.create( OUTPUT_DIR, showWarnings = FALSE)
setwd( OUTPUT_DIR)

# Get the folder with rule scripts
SCRIPT_DIR = file.path( WORKING_DIR, "script/dgrp_line_analysis")

cat("\n-------------------------------")
cat("\nLaunching DGRP line Analysis")
cat("\n-------------------------------")

# Launch the markdown report
opts_knit$set( base.dir = normalizePath( OUTPUT_DIR))

rmarkdown::render( input = file.path( SCRIPT_DIR, "dgrp_line_analysis.Rmd"), 
					output_format = "html_document",
					output_file = file.path( OUTPUT_DIR, "dgrp_line_analysis.html"), 
					output_dir = OUTPUT_DIR)

