import os

from util.sql.SqlManager import SqlManager
from util.log.Logger import Logger
from optparse import OptionParser

OPTIONS = [
       ["-i", "--input", "store", "string", "input", None, "The path to the input data folder.", None],
       ["-o", "--output", "store", "string", "output", None, "The path to the output folder.", None],
       ["-l", "--log", "store", "string", "log", None, "The path to the log folder.", None],
       ["-d", "--database", "store", "string", "database", None, "The name of the SQlite database to read.", None],
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
    
# Initialize the Logger
Logger.get_instance( os.path.join( LOG, "export_sql_table.log"))

# Initialize the SqlManager
SqlManager.get_instance().set_DBpath( os.path.join( INPUT, DB_NAME))

# Set the output folder
output_folder = os.path.join( OUTPUT, "1_export_sql_tables")
if not os.path.exists( output_folder):
   os.makedirs( output_folder)

# Export the SQL tables
for table_name in [ "strain", "individual", "phenotype_data"]:
   # build the path to the output file
   out_file_path = os.path.join( output_folder, table_name + ".csv")
   print( "DB=" + SqlManager.get_instance().get_DBpath())
   print( "TABLE=" + table_name + "->" + out_file_path) 
   # export the table to file
   SqlManager.get_instance().export_table( table_name, out_file_path)

