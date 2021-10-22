import os
from optparse import OptionParser

from util.epistasis.FastEpistasisWrapper import FastEpistasisWrapper

OPTIONS = [
       ["-p", "--phenotype", "store", "string", "phenotype", None, "The path to the phenotype data file.", None],
       ["-s", "--snpsetfile", "store", "string", "snpsetfile", None, "The path to the covariables data file.", None],
       ["-k", "--snpkeptfile", "store", "string", "snpkeptfile", None, "The path to the file containing the list of SNP to keep from original genetic data.", None],
       ["-a", "--alpha", "store", "string", "alpha", None, "The value of the first species error.", None],
       ["-g", "--genotype", "store", "string", "genotype", None, "The path to the genotype file.", None],
       ["-f", "--families", "store", "string", "families", None, "The path to the families (lines) file.", None],
       ["-l", "--log", "store", "string", "log", None, "The path to the log folder.", None],
    ]

    
# Parse the options provided in command line
parser = OptionParser()
for element in OPTIONS:
    parser.add_option(element[0], element[1], action=element[2], type=element[3],
                      dest=element[4], default=element[5],
                      help=element[6], metavar=element[7])
    
# Retrieve options and argument
(options, args) = parser.parse_args()
    
# Get the value of the options 
PHENOTYPE_FILE = options.phenotype
SNPSET_FILE = options.snpsetfile
SNPKEPT_FILE = options.snpkeptfile
ALPHA = float( options.alpha)
GENOTYPE_FILE = options.genotype
FAMILIES_FILE = options.families
LOG = options.log

# Define the output folder
OUTPUT_FOLDER = "output/9_epistasis_execution"

# Build the FastLMM Wrapper and launch the GWAS analysis
fastlmm_gwas = FastEpistasisWrapper( PHENOTYPE_FILE, SNPSET_FILE, SNPKEPT_FILE, ALPHA, GENOTYPE_FILE, FAMILIES_FILE, OUTPUT_FOLDER, LOG)
fastlmm_gwas.execute()