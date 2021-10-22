# ########################################################################
# This scripts launch the Sweave report that produces statistics on
# the various phenotypes at various ages.
# The data must be provided in a file given as argument when launching
# this script with Rscript command. The data file is classically produced
# from the SQlite DB by the python script launching this script.
# ########################################################################

library( knitr)
library( rmarkdown)

cat("\n--------------------------------------")
cat("\nPreparing GWAS gene mapping Analysis")
cat("\n--------------------------------------")

WORKING_DIR = getwd()

# Get the required variables from snakemake
phenotype_name_list = snakemake@params[[ "phenotype_name_list"]]
age_list = snakemake@params[[ "age_list"]]
data_stat_type_list = snakemake@params[[ "data_stat_type_list"]]
suffix_list = unique( snakemake@params[[ "suffix_list"]])
prefered_phenotypes = snakemake@params[[ "prefered_phenotypes"]]

gene_mapping_file_list = snakemake@input[[ "signif_snp_result_genemap"]]

# Create the output folder
OUTPUT_DIR = file.path( WORKING_DIR, "output/7_gwas_gene_mapping_analysis")
dir.create( OUTPUT_DIR, showWarnings = FALSE)
setwd( OUTPUT_DIR)

# Get the folder with rule scripts
SCRIPT_DIR = file.path( WORKING_DIR, "script/gwas_gene_mapping")

cat("\n-------------------------------------")
cat("\nLaunching GWAS gene mapping Analysis")
cat("\n-------------------------------------")

# Launch the sweave report
opts_knit$set( base.dir = normalizePath( OUTPUT_DIR))
rmarkdown::render( input = file.path( SCRIPT_DIR, "gwas_gene_mapping_analysis.Rmd"), 
				   output_format = "html_document", 
				   output_dir = OUTPUT_DIR, 
				   output_file = "gwas_gene_mapping_analysis.html")

