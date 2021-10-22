import os
import gc
import csv
import sys
import subprocess
import shutil
import glob

#import pylab
#import pandas as pd

import logging

from util.log.Logger import Logger

# Execute FastEpistasis Analysis
#
# - Requires for the genotype a ped and a map files (plink will be used to generated required bed, bim and fam files) 
# - Requires a space separated file for the phenotype with three column and headers "fid iid <pheno_name>" : 
#     column 1: family ID, column 2: Individual ID, column 3 phenotype value
# - Requires a file describing the two sets of SNP to be tested. The file contains two list of SNP (one SNP per line). The first set
# start by a line with "SET_A" and end with a line with "END". The second set start with a line with "SET_B" and end with a line with "END.
# 
# Note: A validation of the order of the family/individuals in the genotype file is done.
# If the order differ from the one in the ped file, a new ordered file will be produced for the genotype
#
# Outputs:
# - a summary of the best pairs
#
# To produce the genotype files in plink format (ped and map) from the DGRP complete file, use the following commands
# plink --noweb --bfile dgrp2 --recode --out dgrp2
# To produce the genotype files in plink format (ped and map) from the DGRP complete file with limitation on strains and SNPs, use the following commands
# (selection_files.txt contains the list of SNP ids to keep, and selection_strains.txt contains the list of strains to keep (two columns file))
# plink --noweb --bfile dgrp2 --recode --extract selection_file.txt --keep selected_strains.txt --out dgrp2_selected
#
# IMPORTANT NOTE: since long path are not accepted by plink, we copy the required files to a single folder (self.outputPlinkPath)

class FastEpistasisWrapper:
    
    PHENOTYPE_FILE_FAMILY_HEADER = "fid"
    PHENOTYPE_FILE_INDIVIDUAL_HEADER = "iid"
    PHENOTYPE_FILE_GENERIC_HEADERS = [ "fid", "iid", "value"]
#     PHENOTYPE_FILE_ORDERED_EXTENSION = "_ordered.txt"
    PHENOTYPE_FILE_ORDERED_EXTENSION = "_or.txt"
    
    RESULT_FILE_SIGNIFICANT_EXTENSION = "_signif.txt"
    
    
    #
    # Instantiate the FastEpistasisWrapper object
    # IMPORTANT NOTE: since long path are not accepted by plink, we copy the required files to a single folder (self.outputPlinkPath)
    #
    # @param phenotype_file_name : string - The name of the file containing the phenotype data
    # @param set_file_name : string - The path to the file containing the set (SETA and SETB) of SNP to compare
    # @param snp_kept_file_name : string - The path to the file containing the list of SNP to keep (should be the union of SETA and SETB)
    # @param alpha : float - The significant level used to filter out the results.
    # @param dgrp_file : string - the path to the genotype .ped and .map files (name with no extension)
    # @param families : string - the path to the file containing th list of strain to use
    # @param output_path : string - the path to the output folder
    # @param log_path : string - the path to the log folder
    #
    def __init__(self, phenotype_file_name, set_file_name, snp_kept_file_name, alpha, dgrp_file, families, output_path, log_path):
        
        self.alpha = alpha
        self.originalPhenotypeFileName = os.path.splitext( os.path.basename( phenotype_file_name))[0]
        
        # Define the log file name
        self.logFileName = "FastEpistasisWrapper_" + os.path.splitext( os.path.basename( phenotype_file_name))[0] +".log"
        
        # Check and create the output folders
        self.outputPath = output_path
        if not os.path.isdir( self.outputPath):
            os.mkdir(self.outputPath, 0777)
            
        self.outputPlinkPath = os.path.join( self.outputPath, "plink_" + str( hash( os.path.splitext( os.path.basename( phenotype_file_name))[0])))
        if not os.path.isdir( self.outputPlinkPath):
            os.mkdir(self.outputPlinkPath, 0777)
        
        # Copy the phenotype file to plink folder
#         self.phenotypeFileName = os.path.join( self.outputPlinkPath, os.path.basename( phenotype_file_name))
        self.phenotypeFileName = os.path.join( self.outputPlinkPath, "Pheno.txt")
        shutil.copyfile( phenotype_file_name, self.phenotypeFileName)
        
        # Copy the sets of SNP to plink folder
#         self.setFileName = os.path.join( self.outputPlinkPath, os.path.basename( set_file_name))
        self.setFileName = os.path.join( self.outputPlinkPath, "Sets.txt")
        shutil.copyfile( set_file_name, self.setFileName)
        
#         self.snpKeptFileName = os.path.join( self.outputPlinkPath, os.path.basename( snp_kept_file_name))
        self.snpKeptFileName = os.path.join( self.outputPlinkPath, "Kept.txt")
        shutil.copyfile( snp_kept_file_name, self.snpKeptFileName)
        
        # Copy the dgrp file to plink folder
        self.dgrpFile = os.path.join( self.outputPlinkPath, os.path.basename( dgrp_file))
        for file in glob.glob( dgrp_file + ".*"):
            shutil.copyfile( file, os.path.join( self.outputPlinkPath, os.path.basename( file)))
        
        # Copy the families file  to plink folder
#         self.families = os.path.join( self.outputPlinkPath, os.path.basename( families))
        self.families = os.path.join( self.outputPlinkPath, "Fami.txt")
        shutil.copyfile( families, self.families)
        
        # Initialize the name of the computed genotype file
#         self.genotypeFileName = "genotype_" + os.path.splitext( os.path.basename( self.phenotypeFileName))[0]
        self.genotypeFileName = "geno"
            
        # Initialize the Logger
        Logger.get_instance( os.path.join( log_path, self.logFileName))
    
    #
    # Execute the FastEpistasisWrapper
    #
    # @param no_plink : boolean - True if the plink utility must not be run before execute Fast-LMM
    def execute(self, no_plink = False):
        
        # Open the output file of execution log
        outfile = open( os.path.join( self.outputPath, self.logFileName), "wb")
        
        # If required build the suitable genotype file from global DGRP file
        if( self.dgrpFile != None and self.families != None):
            Logger.get_instance().info("\nBuilding the genotype file from DGRP global data...\n-----------------------------------------------------------")
            self.build_family_genotype( outfile)
        
        
        # Check the phenotype file (if plink required because it means .ped file is present)
        if no_plink == False:
            try:
                Logger.get_instance().info("\nChecking the phenotype file...\n------------------------------")
                self.check_phenotype_file()
            except Exception as e:
                Logger.get_instance().error( "An exception occurred while checking the phenotype data file:")
                Logger.get_instance().error( str(e))
                return

            
        # Launch the plink utility to build the binary version of ped and map files if it does not exists
        if no_plink == False:
            Logger.get_instance().info( "\nGenerating Bed file of DGRP SNP information...\n------------------------------")
            plink_out_file = "bed." + self.genotypeFileName
            # -- Check if a previous Bed file exists in order to remove it before creating the new one
            if os.path.isfile( plink_out_file + ".bed"):
                try:
                    os.remove( plink_out_file)
                except:
                    Logger.get_instance().error( "ERROR: Unable to remove DGRP Bed file : " + plink_out_file + ".bed")
                    Logger.get_instance().error( "       check if Bed file was updated.")
            else:
                Logger.get_instance().info("No previous bed file found")
            # -- build the plink command to generate the bed/map files and execute it
            Logger.get_instance().info( "Generating bed file") 
            plink_command = "cd " + self.outputPlinkPath + ";plink --noweb --file " + self.genotypeFileName + " --make-bed --out " + plink_out_file
            self.launch_command( plink_command, outfile)
            # -- the files produced by plink are the files to use 
            self.genotypeFileName = plink_out_file
            Logger.get_instance().info( "  Bed file generated")
        else:
            Logger.get_instance().info( "\nBypassing plink execution on genotype data\n--------------------------------------------")
        
        
        # Run Espistasis analysis
        Logger.get_instance().info("\nExecuting fastEpistasis....\n------------------")
        geno_epistasis = self.genotypeFileName
        pheno_epistasis = self.phenotypeFileName
        snp_set_epistasis = self.setFileName
        Logger.get_instance().info(" Genotype = " + geno_epistasis)
        Logger.get_instance().info(" Phenotype = " + pheno_epistasis)
        Logger.get_instance().info(" SNP set = " + snp_set_epistasis)
        try:
            # Launch the PreFastEpistasis utility that manage the data from plink into data for FastEpistasis
            print( "|--Executing PreFastEpistasis...")

            previous_working_dir = os.getcwd()
            pre_fast_command = "cd " + self.outputPlinkPath + ";preFastEpistasis --bfile " + os.path.basename( geno_epistasis) + " --pheno " + os.path.basename( pheno_epistasis) + " --set " + os.path.basename( snp_set_epistasis) + ";cd " + previous_working_dir
            self.launch_command( pre_fast_command, outfile)
            
            # Launch the FastEspistatis analysis
            print( "|--Executing FastEpistasis...")

            previous_working_dir = os.getcwd()
            fast_epistasis_command = "cd " + self.outputPlinkPath + ";smpFastEpistasis " + os.path.basename(geno_epistasis) +".bin --method 4 --epi1 0.0" + ";cd " + previous_working_dir
            self.launch_command( fast_epistasis_command, outfile)

        except Exception as e:
            print( "ERROR: an exception occurred during FastEpistasis of '" + pheno_epistasis + "' on genotype '" + geno_epistasis + "' with SNP sets '" + snp_set_epistasis + "'")
            print( "  error is : " + str( e))
            return
        except Error as e:
            print( "ERROR: an error occurred during FastEpistasis of '" + pheno_epistasis, "' on genotype '" + geno_epistasis + "' with SNP sets '" + snp_set_epistasis + "'")
            print( "  error is : " + str( e))
            return
        
        # Rename and move the output file to get a file with the phenotype name
        # and remove the plink result folder
        try:
            print( "|--Renaming and moving results...")
            print( "|--|-- Trying to move " + os.path.join( self.outputPlinkPath, geno_epistasis + ".epi.qt.lm.summary") + " to " + os.path.join( self.outputPath, self.originalPhenotypeFileName + ".epi.qt.lm.summary"))
            shutil.move( os.path.join( self.outputPlinkPath, geno_epistasis + ".epi.qt.lm.summary"), os.path.join( self.outputPath, self.originalPhenotypeFileName + ".epi.qt.lm.summary"))
            print( "|--Deleting plink folder...")
            shutil.rmtree( self.outputPlinkPath)
            
        except Exception as e:
            print( "ERROR: an exception occurred during file moving and removing of results of FastEpistasis of '" + pheno_epistasis + "' on genotype '" + geno_epistasis + "' with SNP sets '" + snp_set_epistasis + "'")
            print( "  error is : " + str( e))
            return
        except Error as e:
            print( "ERROR: an error occurred during file moving and removing of results of FastEpistasis of '" + pheno_epistasis, "' on genotype '" + geno_epistasis + "' with SNP sets '" + snp_set_epistasis + "'")
            print( "  error is : " + str( e))
            return
        
        print( "\nFinished.\n")
        sys.stdout.flush()
    
    
    #
    # Build the plink files required by the fast-LMM starting from the global GDRP file and
    # keeping only the desired families
    #
    # @param outfile : File - the file where the output of the used shell command will be written
    #
    def build_family_genotype(self, outfile):

        # Create the ped file from the DGRP and families file
        command = "cd " + self.outputPlinkPath + \
                    ";plink --noweb --recode" + \
                    " --bfile "+ os.path.basename( self.dgrpFile) +\
                    " --keep " + os.path.basename( self.families) + \
                    " --extract " + os.path.basename( self.snpKeptFileName) + \
                    " --out " + self.genotypeFileName + \
                    " > my_plink.out"
                    
        self.launch_command( command, outfile)
    
    #
    # Check if the phenotype file has the family and individuals classified in the same order
    # If not create a file of ordered family and individuals
    # 
    def check_phenotype_file(self):
        
        # Read the genotype data file
        geno_csv_path = os.path.join( self.outputPlinkPath, self.genotypeFileName + ".ped")
        Logger.get_instance().info( "Reading filtered genotype file : " + geno_csv_path)
        geno_csv_file = open( geno_csv_path)
        geno_reader = csv.reader( geno_csv_file, delimiter=' ', quoting=csv.QUOTE_NONE)
        
        # Get the list of family names with the order in the .ped file
        family_names = []
        for row in geno_reader:
            family_names.append( self.getKey( row[0], row[1]))
        
        # Read the phenotype data file
        Logger.get_instance().info( "Reading phenotype file : " + self.phenotypeFileName)
        pheno_csv_file = open( self.phenotypeFileName)
        pheno_reader = csv.reader( pheno_csv_file, delimiter=' ', quoting=csv.QUOTE_NONE)

        # Parse the phenotype data file
        # If the columns are not the correct ones, an exception is raised
        # If ok, keep the headers and store the list of family name both as a list and a dict mapping them to their file line
        fid_dict ={}
        fid_list = []
        count = 0
        for row in pheno_reader:
            if len( row) != 3:
                raise Exception( "ERROR : bad number of columns in phenotype file (must be 3 columns (fid iid <phenoname>) separated with spaces")
            if count == 0:
                if len( row) != 3:
                    raise Exception( "ERROR : bad number of columns in phenotype file (must be 'fid iid <phenoname>' separated with spaces")
                if row[ 0] == FastEpistasisWrapper.PHENOTYPE_FILE_FAMILY_HEADER and row[ 1] == FastEpistasisWrapper.PHENOTYPE_FILE_INDIVIDUAL_HEADER:
                    missing_headers = False
                    continue
                else:
                    missing_headers = True

            fid = row[ 0]
            iid = row[ 1]
            key = self.getKey( fid,iid)
            fid_list.append( key)
            fid_dict[ key] = " ".join( row)
            count = count + 1
            
        
        # Look if the phenotype family order is the same as the genotype family order
        Logger.get_instance().info( "Checking families order in phenotype file...")
        produce_order = False
        for index in range( 0, len( fid_list)):
            if family_names[ index] != fid[ index]:
                Logger.get_instance().info( "  WARNING : phenotype data are not organized by family like genotype data. Generating ordered file...")
                produce_order = True
                break
        
        # Copy the phenotype file to plink working folder changing its name for "ordered" one or,
        # if required, create a phenotype data file ordered by family like the genotype data
        ordered_filename = os.path.splitext( os.path.basename( self.phenotypeFileName))[0] + FastEpistasisWrapper.PHENOTYPE_FILE_ORDERED_EXTENSION
        ordered_filepath = os.path.join( self.outputPlinkPath, ordered_filename)
        if produce_order:
            Logger.get_instance().info( "Writing ordered phenotype file...")
            try:
                # Produce the name of the ordered file and open it
                ordered_file = open( ordered_filepath, "w")
                # Write the headers
                if missing_headers:
                    ordered_file.write( " ".join( FastEpistasisWrapper.PHENOTYPE_FILE_GENERIC_HEADERS) + "\n")
                # Add the phenotype information ordered by family like genotype file
                for family_name in family_names:
                    ordered_file.write( fid_dict[ family_name] + "\n")
                    ordered_file.flush()
                # Close the file
                ordered_file.close()
                Logger.get_instance().info( "  Ordered phenotype data file produced : " + ordered_filename + "\n")
            except KeyError:
                raise Exception( "ERROR : A family name does not exist in phenotype data but is present in genotype data:" + family_name)
        else:
            copyfile( self.phenotypeFileName, ordered_filepath)
    
        # Replace the original phenotype file by the ordered one
        self.phenotypeFileName = ordered_filepath
    
    
    #
    # Return a Key compsoed by the two given strings
    # 
    def getKey(self, string1, string2):
        
        return (str( string1) + ":" + str(string2))


    #
    # Launch the provided command line, redirecting the standard output and error to the given outfile
    #
    # @param command : string - the command line to execute
    # @param outfile : file - the output file object
    #
    def launch_command(self, command, outfile):
        
        Logger.get_instance().info( "  command = " + command)
        
        # -- run the command in a subprocess
        gc.collect()
        p = subprocess.Popen( command, shell=True, stdout=outfile, stderr=outfile)
        while True:
            if p.poll() != None:
                break
    

    #
    # Concatanate the sets of files 
    #
    # @param file1 : string - The path to the files containing the first set of SNP
    # @param file2 : string - The path to the files containing the second set of SNP
    #
    # @returm string - The string of the concatenated file
    @staticmethod
    def concat_set_of_snp( input_path, file1, file2):

    #	outfile_path = os.path.join( input_path, file1 + "_" + file2 + "_SNPsets.txt")
    	outfile_path = os.path.join( input_path, "SNPsets")
    	with open( outfile_path, 'w') as outfile:
    	    outfile.write( "SET_A\n")
            with open( os.path.join( input_path, file1)) as infile:
	        for line in infile:
	            outfile.write( line)
    	    outfile.write( "END\n")
    	    outfile.write( "\n")
    	    outfile.write( "SET_B\n")
            with open( os.path.join( input_path, file2)) as infile:
	        for line in infile:
	            outfile.write( line)            
    	    outfile.write( "END\n")
    	    outfile.flush()
    	    outfile.close()
            return outfile_path
    	return None
            
# #######################
# The main script
# #######################
if __name__ == '__main__':
    from optparse import OptionParser
    
    # Parse the options provided in command line
    parser = OptionParser()
    for element in FastEpistasisWrapper.OPTIONS:
        parser.add_option(element[0], element[1], action=element[2], type=element[3],
                          dest=element[4], default=element[5],
                          help=element[6], metavar=element[7])
        
    # Retrieve options and argument
    (options, args) = parser.parse_args()
        
    # Get the value of the options build the FastEpistasis object 
    input_path = options.input
    genotype_file_name = options.genotype
    phenotype_file_name = options.phenotype
    bothsets_file_name = options.bothsets
    seta_file_name = options.seta
    setb_file_name = options.setb
    dgrp_file_path = options.dgrp
    families_file_path = options.families
    snp_kept_file_name = options.keepsnp
    alpha = options.alpha

    print( "Options:")
    print( "--------")
    print( "  input folder            = " + str( input_path))
    print( "  genotype                = " + str( genotype_file_name))
    print( "  phenotype               = " + str( phenotype_file_name))
    if bothsets_file_name != None:
	print( "  SNP both sets           = " + str( bothsets_file_name))
    else:
	print( "  SNP sets                = " + str( seta_file_name) + " vs " + str( setb_file_name))
    print( "  DGRP file (optionnal)   = " + str( dgrp_file_path))
    print( "  families (optionnal)    = " + str( families_file_path))
    print( "  SNP to keep (optionnal) = " + str( snp_kept_file_name))
    print( "  alpha                   = " + str( alpha))
    print( "  ")

    if bothsets_file_name == None:
	set_file_name = FastEpistasisWrapper.concat_set_of_snp( input_path, seta_file_name, setb_file_name)
    else:
	set_file_name = os.path.join( input_path, bothsets_file_name)

    # Since FastEpistasis don't like long file name, we use a short one for SNP set file name
    short_set_file_name = os.path.join( input_path, "SNPsets.txt")
    try:
	os.remove( short_set_file_name)
    except OSError:
	pass
    shutil.copyfile( set_file_name, short_set_file_name)
    
    # Since FastEpistasis don't like long file name, we use a short one for SNP list file name
    short_list_file_name = os.path.join( input_path, "SNPlist.txt")
    try:
	os.remove( short_list_file_name)
    except OSError:
	pass
    shutil.copyfile( snp_kept_file_name, short_list_file_name)

    # Check if one of the required option is missing
    if( input_path == None or genotype_file_name == None or phenotype_file_name == None or set_file_name == None):
        parser.print_help()
    
    # Build the FastEpistasis object and execute it
    fastlmm_gwas = FastEpistasisWrapper( input_path, genotype_file_name, phenotype_file_name, short_set_file_name, dgrp_file_path, families_file_path, short_list_file_name, alpha)
    fastlmm_gwas.execute( False)

