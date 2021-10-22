import os
import csv
import ast

from optparse import OptionParser

from sqlalchemy import and_

from model.Mutation import Mutation

from util.sql.SqlManager import SqlManager
from util.log.Logger import Logger


OPTIONS = [
       ["-i", "--input", "store", "string", "input", None, "The path to the input data folder.", None],
       ["-o", "--output", "store", "string", "output", None, "The path to the output folder.", None],
       ["-l", "--log", "store", "string", "log", None, "The path to the log folder.", None],
       ["-d", "--database", "store", "string", "database", None, "The name of the SQlite database to read.", None],
       ["-p", "--phenotypesnps", "store", "string", "phenotypesnps", None, "The list of files of phenotype to take as focus snp (setA).", None],
       ["-a", "--age", "store", "string", "age", None, "The age associated to the phenotype data.", None],
       ["-t", "--data_stat_type", "store", "string", "data_stat_type", None, "The type of statistical data used (CV, MEAN...).", None],
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
INPUT = options.input
OUTPUT = options.output
LOG = options.log
DB_NAME = options.database
AGE = options.age
DATA_STAT_TYPE = options.data_stat_type

# Manage the provided list of files to get SNP. It is provided as a string in snakemake format. Needs to convert it to tuple of strings
PHENOTYPE_SNP_FILE_LIST = options.phenotypesnps.split( " ")
PHENOTYPE_SNP_FILE_LIST = [r.strip() for r in PHENOTYPE_SNP_FILE_LIST]
    
# Initialize the Logger
Logger.get_instance( os.path.join( LOG, "prepare_snp_sets.log"))

# Initialize the SqlManager
SqlManager.get_instance().set_DBpath( os.path.join( INPUT, DB_NAME))

# Set the output folder
output_folder = os.path.join( OUTPUT, "8_epistasis_snp_sets")
if not os.path.exists( output_folder):
   os.makedirs( output_folder)

#
# First get all the SNP from database with a MAF > 5%
#

# -- query from the database the list of SNP with MAF>5%
all_snp_list = SqlManager.get_instance().get_session().query( Mutation.mutation_id).filter( and_(Mutation.refCount >=10, Mutation.altCount >=10, Mutation.type_mutation=="SNP")).all()
# Convert the list of objects provided as result to strings
all_snp_list = [r[0].encode("utf-8") for r in all_snp_list]
# Convert the list to set (for unicity)
all_snp_set = set( all_snp_list)

#
# Second, from the list of phenotype GWAS SNP, build the SNP sets file used for the Epistasis analysis
#
snp_set_A = set()
for current_snp_file in PHENOTYPE_SNP_FILE_LIST:
    with open( current_snp_file) as snpfile:
        snpreader = csv.DictReader( snpfile, delimiter ="\t")
        for row in snpreader:
            snp_id = row[ "ID"]
            if "SNP" in snp_id:
                snp_set_A.add( snp_id)

# Add the setA to the complete list
all_snp_set = all_snp_set.union( snp_set_A)
            
#  Create the CSV output file for SNP to keep in analysis
outfile_kept = open( os.path.join( output_folder, "snpkept_" + str( AGE) + "W_" + DATA_STAT_TYPE +".txt"), "w")

# -- dump the SNPs to file
outfile_kept.write( "\n".join( all_snp_set))

# -- close the file
outfile_kept.close()

# Create the CSV output file for SNP to be analyzed in epistasis (setA = focus, setB=test)
outfile_setA_and_B = open( os.path.join( output_folder, "snpsets_" + str( AGE) + "W_" + DATA_STAT_TYPE +".txt"), "w")

# -- dump the SNPs setA to file
outfile_setA_and_B.write( "SET_A\n")
outfile_setA_and_B.write( "\n".join( snp_set_A) + "\n")
outfile_setA_and_B.write( "END\n")

# -- dump the SNPs setB to file
outfile_setA_and_B.write( "SET_B\n")
outfile_setA_and_B.write( "\n".join( all_snp_set)  + "\n")
outfile_setA_and_B.write( "END\n")

# -- close the file
outfile_setA_and_B.close()


