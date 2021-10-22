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

HEADER_FASTEPISTASIS_RESULT_SNP_1 = "1_SNP"
HEADER_FASTEPISTASIS_RESULT_SNP_2 = "2_SNP"

OPTIONS = [
       ["-e", "--epistasis_result", "store", "string", "epistasis_result", None, "The path to the gwas results file to map to gene.", None],
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
ESPISTASIS_RESULT = options.epistasis_result
FAMILIES = options.families
OUTPUT = options.output
LOG = options.log
DB_PATH = options.database
    

# Initialize the Logger
Logger.get_instance( os.path.join( LOG, "epistasis_result_gene_mapping.log"))

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
epistasis_result_file = FileUtils.open_text_r( ESPISTASIS_RESULT)
# Open the output files
# - open the file for result with mapped SNP to genes
output_file_path = os.path.join( OUTPUT, os.path.basename( ESPISTASIS_RESULT) + "_genemap.txt")
output_file = FileUtils.open_text_w( output_file_path)
# - open the file for result with no mapped SNP to genes
output_file_missing_path = os.path.join( OUTPUT, os.path.basename( ESPISTASIS_RESULT) + "_genemap_missing.txt")
output_file_missing = FileUtils.open_text_w( output_file_missing_path)
# Define a reader 
snpreader = csv.reader( epistasis_result_file, delimiter=' ')
# Skip the first line that is not useful
snpreader.next()
# Read the headers on the first line and change them beacuse of repeated column names "CHR" and "SNP"
header_list = snpreader.next()
header_list =  [ "1_CHR", "1_SNP", "N_SIG", "N_TOT", "PROP", "CHISQ", "2_CHR", "2_SNP"]
# Skip the third line that is not useful
snpreader.next()
# Parse the file by classifying columns along headers
column = {}
for h in header_list:
   column[h] = []
for row in snpreader:
    # -- remove the empty string from row
    row = filter(None, row)
    # -- map the row entries to headers
    for h, v in zip(header_list, row):
        column[h].append(v)

# Write the headers in the output file
output_headers_1 = "1_ID" + "\t" + "1_FlybaseID" + "\t" + "1_GeneSymbol" + "\t" + "1_Position" + "\t" + "1_Type" + "\t" + "1_NbOfLinesForMutationInEpistasis" + "\t" + "1_NbOfLinesForMutationInDB" + "\t" + "1_TotalNbOfLinesinDB" + "\t"
output_headers_2 = "\t" + "2_ID" + "\t" + "2_FlybaseID" + "\t" + "2_GeneSymbol" + "\t" + "2_Position" + "\t" + "2_Type" + "\t" + "2_NbOfLinesForMutationInEpistasis" + "\t" + "2_NbOfLinesForMutationInDB" + "\t" + "2_TotalNbOfLinesinDB" 
output_headers = output_headers_1 + "\t".join( header_list) + output_headers_2
output_headers = output_headers + "\n"
output_file.write( output_headers)

# Get the list of SNP ids
list_snp_ids_1 = column[ HEADER_FASTEPISTASIS_RESULT_SNP_1]
list_snp_ids_2 = column[ HEADER_FASTEPISTASIS_RESULT_SNP_2]
list_snp_ids = list( set( list_snp_ids_1 + list_snp_ids_2))

print( "Number of SNP in list1: " + str( len( list_snp_ids_1)))
print( "Number of SNP in list2: " + str( len( list_snp_ids_2)))
print( "Number of SNP in list: " + str( len( list_snp_ids)))

# Query the database to get the information on lines associated to each mutations
total_number_of_lines_in_db = SqlManager.get_instance().get_session().query( AssociationMutationLine.line_id).distinct().count()
Logger.get_instance().info( "Total number of lines=" + str( total_number_of_lines_in_db) )

# Query the database to get the information on genes (effect) related to that SNPs
effect_list = SqlManager.get_instance().get_session().query( MutationEffect).filter( MutationEffect.mutation_id.in_( list_snp_ids)).all()

print( "Number of effects in list: " + str( len( effect_list)))

# Parse the list of MutationEffects and write their related information to lists
retrieved_mutation_list = []
effect_for_mutation_dict = {}
lines_for_mutation_dict = {}
lines_for_mutation_in_used_lines_dict = {}
for effect in effect_list:
    retrieved_mutation_list.append( effect.mutation_id)
    
    # Get the number of lines associated with this mutation in the database
    # and the number of lines associated with this mutation in the lines used for the GWAS
    if not effect.mutation_id in lines_for_mutation_dict.keys():
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
        # Memorize the scores and the effect
        effect_for_mutation_dict[ effect.mutation_id] = effect
        lines_for_mutation_dict[ effect.mutation_id] = nb_of_lines_for_mutation
        lines_for_mutation_in_used_lines_dict[ effect.mutation_id] = nb_of_lines_for_mutation_in_used_lines
#     
#     # Get the index of the mutation in the input file columns
#     try:
#         mutation_index = list_snp_ids.index( effect.mutation_id)
#     except:
#         Logger.get_instance().warning("PhenotypeStatisticStrategy.retrieve_genes_of_significant_snps() : Mutation found in DB is not present in GWAS result : " + effect.mutation_id)
#         continue

print( "Number of identified effects in list: " + str( len( effect_for_mutation_dict.keys())))

# Parse the list of pairs of snps
for row_index in range( 0, len( list_snp_ids_1)):
    # Get the focus SNP
    snp_id_1 = list_snp_ids_1[ row_index]
    # get the target SNP
    snp_id_2 = list_snp_ids_2[ row_index]
    print( "Looking for SNP pair:" + snp_id_1 + " vs " + snp_id_2)
    # Check if both mutation ids have an identified effect, write out their information on gene both with epistasis information
    if snp_id_1 in retrieved_mutation_list and snp_id_2 in retrieved_mutation_list:
        print( "|-- Found effects")
        # Retrieve the effects corresponding to both SNPs
        effect_1 = effect_for_mutation_dict[ snp_id_1]
        effect_2 = effect_for_mutation_dict[ snp_id_2]
        # Retrieve the information of number of lines corresponding to both SNPs
        nb_of_lines_for_mutation_in_used_lines_1 = lines_for_mutation_in_used_lines_dict[ snp_id_1]
        nb_of_lines_for_mutation_in_used_lines_2 = lines_for_mutation_in_used_lines_dict[ snp_id_2]
        nb_of_lines_for_mutation_1 = lines_for_mutation_dict[ snp_id_1]
        nb_of_lines_for_mutation_2 = lines_for_mutation_dict[ snp_id_2]
        # Build the line to write to file by concatenating the MutationEffect information and the GWAS information
        output_line = effect_1.mutation_id + "\t" + effect_1.flybase_id + "\t" + effect_1.symbol + "\t" + effect_1.position + "\t" + effect_1.type + "\t" + str( nb_of_lines_for_mutation_in_used_lines_1) + "\t" + str( nb_of_lines_for_mutation_1) + "\t" + str( total_number_of_lines_in_db) 
        for header in header_list:
            output_line = output_line + "\t" + column[ header][ row_index]
        output_line = output_line + "\t" + effect_2.mutation_id + "\t" + effect_2.flybase_id + "\t" + effect_2.symbol + "\t" + effect_2.position + "\t" + effect_2.type + "\t" + str( nb_of_lines_for_mutation_in_used_lines_2) + "\t" + str( nb_of_lines_for_mutation_2) + "\t" + str( total_number_of_lines_in_db)
        output_line = output_line + "\n"
        
        # Write the line to output file
        output_file.write( output_line)
    else:
        for header in header_list:
            output_line = output_line + "\t" + column[ header][ row_index]
        output_file_missing.write( output_line)
        

# Close the used files
# - close the file for result with mapped SNP to genes
output_file.flush()
output_file.close()
# - close the file for result with no mapped SNP to genes
output_file_missing.flush()
output_file_missing.close()
# - close the file of epistasis result
epistasis_result_file.close()

        
        
        