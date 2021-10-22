library(knitr)

cat("\n--------------------------------")
cat("\nPreparing Control Line Analysis")
cat("\n--------------------------------")

WORKING_DIR = getwd()

# Get the variables from the snakemake rule
strain_input_file = file.path( WORKING_DIR, snakemake@input[[ "strain_data_file"]])
individual_input_file = file.path( WORKING_DIR, snakemake@input[[ "individual_data_file"]])
phenotype_data_input_file = file.path( WORKING_DIR, snakemake@input[[ "phenotype_data_file"]])

# Create the output folder
OUTPUT_DIR = file.path( WORKING_DIR, "output/2_control_line_analysis")
dir.create( OUTPUT_DIR, showWarnings = FALSE)

# Get the folder with rule scripts
SCRIPT_DIR = file.path( WORKING_DIR, "script/control_line_analysis")

cat("\n-------------------------------")
cat("\nLaunching Control Line Analysis")
cat("\n-------------------------------")

# Launch the sweave report
opts_knit$set( base.dir = normalizePath( OUTPUT_DIR))
knit2pdf( input = file.path( SCRIPT_DIR, "control_line_analysis.Rnw"), output = file.path( OUTPUT_DIR, "control_line_analysis.tex"), quiet = TRUE)
