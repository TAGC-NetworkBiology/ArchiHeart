#
# Retrieve the result of Fast-LMM GWAS to get the most significant SNPs
# and extract the genes associated to these SNPs from the database
#

import os
import csv
from optparse import OptionParser

from util.sql.SqlManager import SqlManager
from util.log.Logger import Logger
from util.file.FileUtils import FileUtils

from model.Mutation import Mutation
from model.Line import Line
from model.MutationEffect import MutationEffect
from model.AssociationMutationLine import AssociationMutationLine

HEADER_FASTLMM_RESULT_SNP = "SNP"

OPTIONS = [
       ["-g", "--gwas_result", "store", "string", "gwas_result", None, "The path to the gwas results file to map to gene.", None],
       ["-f", "--families", "store", "string", "families", None, "The path to the file listing the DGRP lines used by the GWAS.", None],
       ["-o", "--output", "store", "string", "output", None, "The path to the output folder.", None],
       ["-l", "--log", "store", "string", "log", None, "The path to the log folder.", None],
       ["-d", "--database", "store", "string", "database", None, "The path to the database file (SQlite database )to read.", None],
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
GWAS_RESULT = options.gwas_result
FAMILIES = options.families
OUTPUT = options.output
LOG = options.log
DB_PATH = options.database
    

# Initialize the Logger
Logger.get_instance( os.path.join( LOG, "gwas_result_gene_mapping.log"))

# Initialize the SqlManager
SqlManager.get_instance().set_DBpath( DB_PATH)

# Extract the list of DGRP lines used by the GWAS
# ---------------------------------------------------------------
# Open the file to read
families_file = FileUtils.open_text_r( FAMILIES)
# Define a reader 
familiesreader = csv.reader( families_file, delimiter=' ')
# read the lines
used_lines = []
for row in familiesreader:
    used_lines.append( row[0])
    
# Extract the list of SNP and get the corresponding genes from DB
# ---------------------------------------------------------------
# Open the file to read
gwas_result_file = FileUtils.open_text_r( GWAS_RESULT)
# Open the output file
output_file_path = os.path.join( OUTPUT, os.path.splitext( os.path.basename( GWAS_RESULT))[0] + "_genemap.txt")
output_file = FileUtils.open_text_w( output_file_path)
# Define a reader 
snpreader = csv.reader( gwas_result_file, delimiter='\t')
# Read the headers on the first line
header_list = snpreader.next()
# Parse the file by classifying columns along headers
column = {}
for h in header_list:
   column[h] = []
for row in snpreader:
    for h, v in zip(header_list, row):
        column[h].append(v)

# Write the headers in the output file
output_headers = "ID" + "\t" + "FlybaseID" + "\t" + "GeneSymbol" + "\t" + "Position" + "\t" + "Type" + "\t" + "NbOfLinesForMutationInGWAS" + "\t" + "NbOfLinesForMutationInDB" + "\t" + "TotalNbOfLinesinDB" + "\t" 
output_headers = output_headers + "\t".join( header_list)
output_headers = output_headers + "\n"
output_file.write( output_headers)

# Get the list of SNP ids
list_snp_ids = column[ HEADER_FASTLMM_RESULT_SNP]

# Query the database to get the information on lines associated to each mutations
total_number_of_lines_in_db = SqlManager.get_instance().get_session().query( AssociationMutationLine.line_id).distinct().count()
Logger.get_instance().info( "Total number of lines=" + str( total_number_of_lines_in_db) )

# Query the database to get the information on genes (effect) related to that SNPs
effect_list = SqlManager.get_instance().get_session().query( MutationEffect).filter( MutationEffect.mutation_id.in_( list_snp_ids)).all()

# Parse the list of MutationEffects and write their related information to output file
retrieved_mutation_list = []
lines_for_mutation_dict = {}
lines_for_mutation_in_used_lines_dict = {}
for effect in effect_list:
    retrieved_mutation_list.append( effect.mutation_id)
    
    # Get the number of lines associated with this mutation in the database
    # and the number of lines associated with this mutation in the lines used for the GWAS
    if effect.mutation_id in lines_for_mutation_dict.keys():
        nb_of_lines_for_mutation = lines_for_mutation_dict[ effect.mutation_id]
        nb_of_lines_for_mutation_in_used_lines = lines_for_mutation_in_used_lines_dict[ effect.mutation_id]
    else:
        # Get the lines associated to that mutation
        lines_for_mutation = SqlManager.get_instance().get_session().query( AssociationMutationLine.line_id).filter( AssociationMutationLine.mutation_id == effect.mutation_id).all()
        # Convert the list of objects provided as result to strings
        lines_for_mutation = [r[0].encode("utf-8") for r in lines_for_mutation]
        # Remove the string "dgrp" in the line name and replace it by "line_"
        lines_for_mutation = [w.replace( 'dgrp', 'line_') for w in lines_for_mutation]
        # Get the list of lines with the mutation that were used by the GWAS
        lines_for_mutation_in_used_lines = [value for value in lines_for_mutation if value in used_lines]
        # Count the lines
        nb_of_lines_for_mutation = len( lines_for_mutation)
        nb_of_lines_for_mutation_in_used_lines = len( lines_for_mutation_in_used_lines)
        # Memorize the scores 
        lines_for_mutation_dict[ effect.mutation_id] = nb_of_lines_for_mutation
        lines_for_mutation_in_used_lines_dict[ effect.mutation_id] = nb_of_lines_for_mutation_in_used_lines
    
    # Get the index of the mutation in the input file columns
    try:
        mutation_index = list_snp_ids.index( effect.mutation_id)
    except:
        Logger.get_instance().warning("PhenotypeStatisticStrategy.retrieve_genes_of_significant_snps() : Mutation found in DB is not present in GWAS result : " + effect.mutation_id)
        continue
    # Build the line to write to file by concatenating the MutationEffect information and the GWAS information
    output_line = effect.mutation_id + "\t" + effect.flybase_id + "\t" + effect.symbol + "\t" + effect.position + "\t" + effect.type + "\t" + str( nb_of_lines_for_mutation_in_used_lines) + "\t" + str( nb_of_lines_for_mutation) + "\t" + str( total_number_of_lines_in_db) 
    for header in header_list:
        output_line = output_line + "\t" + column[ header][ mutation_index]
    output_line = output_line + "\n"
    # Write the line to output file
    output_file.write( output_line)

# Close the used files
output_file.flush()
output_file.close()
gwas_result_file.close()

# Look at the mutations that were not found with corresponding gene information
missing_mutation_list = list( set( list_snp_ids) - set( retrieved_mutation_list))
# If some missing mutations exists, write them to file
if len( missing_mutation_list) > 0:
    # Open the output file where the missing mutation will be written
    output_file_path = os.path.join( OUTPUT, os.path.splitext( os.path.basename( GWAS_RESULT))[0] + "_genemapmissing.txt")
    output_file = FileUtils.open_text_w( output_file_path)
    # Write the headers of details of missing mutations to file
    output_headers = "\t".join( header_list)
    output_headers = output_headers + "\n"
    output_file.write( output_headers)
    # Write the details of missing mutations to file
    for mutation_id in missing_mutation_list:
        # Get the index of the mutation in the input file columns
        try:
            mutation_index = list_snp_ids.index( mutation_id)
        except:
            Logger.get_instance().warning("PhenotypeStatisticStrategy.retrieve_genes_of_significant_snps() : Mutation NOT found in DB is not present in GWAS result : " + mutation_id)
            continue
        output_line = ""
        for header in header_list:
            output_line = output_line + column[ header][ mutation_index] + "\t"
        output_line = output_line + "\n"
        output_file.write( output_line)
    # Close the used files
    output_file.flush()
    output_file.close()
        
        
        