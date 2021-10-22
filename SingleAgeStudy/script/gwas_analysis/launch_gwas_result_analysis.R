# ########################################################################
# This scripts launch the Sweave report that produces statistics on
# the various phenotypes at various ages.
# The data must be provided in a file given as argument when launching
# this script with Rscript command. The data file is classically produced
# from the SQlite DB by the python script launching this script.
# ########################################################################

library(knitr)

cat("\n-------------------------------")
cat("\nPreparing GWAS result Analysis")
cat("\n-------------------------------")

WORKING_DIR = getwd()

# Get the required variables from snakemake
phenotype_name_list=snakemake@params[[ "phenotype_name_list"]]
age_list=snakemake@params[[ "age_list"]]
data_stat_type_list=snakemake@params[[ "data_stat_type_list"]]

phenotype_strain_values_file_list = snakemake@input[[ "ordered_phenotype_values_list"]]
signif_result_file_list = snakemake@input[[ "signif_snp_results_list"]]
manathanplot_file_list = snakemake@input[[ "manathan_plot_list"]]
QQplot_file_list = snakemake@input[[ "qqplot_list"]]

# Create the output folder
OUTPUT_DIR = file.path( WORKING_DIR, "output/5_gwas_result_analysis")
dir.create( OUTPUT_DIR, showWarnings = FALSE)
setwd( OUTPUT_DIR)

# Get the folder with rule scripts
SCRIPT_DIR = file.path( WORKING_DIR, "script/gwas_analysis")

cat("\n-------------------------------")
cat("\nLaunching GWAS result Analysis")
cat("\n-------------------------------")

# Launch the sweave report
opts_knit$set( base.dir = normalizePath( OUTPUT_DIR))
knit2pdf( input = file.path( SCRIPT_DIR, "gwas_result_analysis.Rnw"), output = file.path( OUTPUT_DIR, "gwas_result_analysis.tex"), quiet = TRUE)

