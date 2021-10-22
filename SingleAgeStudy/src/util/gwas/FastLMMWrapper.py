
import os
import gc
import csv
import subprocess
from shutil import copyfile

import pylab
import pandas as pd

# from util.cluster.ClusterData import ClusterData

from fastlmm.association import single_snp
import fastlmm.util.util as flutil
from fastlmm.util.stats import plotp
import logging

from util.log.Logger import Logger

# Execute Fast-LMM GWAS
# https://github.com/MicrosoftGenomics/FaST-LMM/blob/master/doc/ipynb/FaST-LMM.ipynb
#
# - Requires for the genotype:
#     - or a ped and a map files (default usage as plink will be used to generated required bed, bim and fam files) 
#     - or a bed, a bim and a fam files (use the -x option to disable plink usage)
# - Requires a space separated file for the phenotype with three columns and no header : 
#     column 1: family ID, column 2: Individual ID, column 3 phenotype value
# - Requires a tab separated file for the covariate with at least three columns and no header :
#     column 1: family ID, column 2: Individual ID, column 3 and next covariable values
# 
# Note: if plink is used (ped and map files provided), a validation of the order of the family/individuals in the genotype and
# covariate files will also be done. If the order differ from the one in the ped file, new ordered files willbe produced for the genotype
# and covariates
#
# Outputs:
# - A Manhattan plot
# - A QQ-plot
# - The complete result dataframe as csv file
# Columns in the output are as follows:
#  * SNP or Set The SNP or set identifier tested.
#  * PValue The P value computed for the SNP tested.
#  * NullLogLike The log likelihood of the null model.
#  * AltLogLike The log likelihood of the alternative model.
# Single-SNP testing only:
#  * Chr The chromosome identifier for the SNP tested or 0 if unplaced. Taken from the PLINK file.
#  * GenDist The genetic distance of the SNP on the chromosome. Taken from the PLINK file. Any units are allowed, but typically centimorgans or morgans are used.
#  * ChrPos The base-pair position of the SNP on the chromosome (bp units). Taken from the PLINK file.
#  * SnpWeight The fixed-effect weight of the SNP.
#  * SnpWeightSE The standard error of the SnpWeight.
#  * Nullh2 The narrow sense heritability given by h2 =sigma2g/(sigma2g+sigma2e) on the null model.
# SNP-set testing only:
#  * SNPs_in_Set The number of markers in the set.
#  * Alt_h2 The value found in the alt. model, given by sigma2(h2(a2*KS+(1-a2)*KC)+(1-h2)*I), where KC is the NxN matrix to correct for confounding,
#      and KS is the matrix containing SNPs to be tested.
#  * Alt_a2 See Alt_h2.
#  * Null_h2 The value found in the null model, given by sigma3(h2*KC+1-h2)*I), where KC is the NxN matric to correct for confounding.
#
# To produce the genotype files in plink format (ped and map) from the DGRP complete file, use the following commands
# plink --noweb --bfile dgrp2 --recode --out dgrp2
# To produce the genotype files in plink format (ped and map) from the DGRP complete file with limitation on strains and SNPs, use the following commands
# (selection_files.txt contains the list of SNP ids to keep, and selection_strains.txt contains the list of strains to keep (two columns file))
# plink --noweb --bfile dgrp2 --recode --extract selection_file.txt --keep selected_strains.txt --out dgrp2_selected
#

class FastLMMWrapper:
        
    PHENOTYPE_FILE_FAMILY_HEADER = "fid"
    PHENOTYPE_FILE_INDIVIDUAL_HEADER = "iid"
    PHENOTYPE_FILE_ORDERED_EXTENSION = "_ordered"
    
    RESULT_FILE_SIGNIFICANT_EXTENSION = "_signif"
    
    #
    # Instantiate the fastLMM object
    #
    # @param phenotype_file_name : string - The name of the file containing the phenotype data
    # @param covariable_file_name : string - The name of the file containing the covariable definition
    # @param alpha : float - The significant level used to filter out the results.
    # @param dgrp_file : string - the path to the genotype .ped and .map files (name with no extension)
    # @param families : string - the path to the file containing th list of strain to use
    # @param output_path : string - the path to the output folder
    # @param log_path : string - the path to the log folder
    #
    def __init__(self, phenotype_file_name, covariable_file_name, alpha, dgrp_file, families, output_path, log_path):
        
        self.phenotypeFileName = phenotype_file_name
        self.covariableFileName = covariable_file_name
        
        self.dgrpFile = dgrp_file
        self.families = families
        
        self.alpha = alpha
        self.outputPath = output_path
        self.outputPlinkPath = os.path.join( self.outputPath, "plink")
        self.genotypeFileName = "filtered_dgrp_" + os.path.splitext( os.path.basename( self.phenotypeFileName))[0]
        
        if not os.path.isdir( self.outputPath):
            os.mkdir(self.outputPath, 0777)
        if not os.path.isdir( self.outputPlinkPath):
            os.mkdir(self.outputPlinkPath, 0777)
            
        # Initialize the Logger
        Logger.get_instance( os.path.join( log_path, "FastLMMWrapper_" + os.path.splitext( os.path.basename( self.phenotypeFileName))[0] +".log"))
    
    #
    # Execute the Fast-LMM GWAS
    #
    # @param no_plink : boolean - True if the plink utility must not be run before execute Fast-LMM
    def execute(self, no_plink = False):
        
        # Open the output file of execution log
        outfile = open( os.path.join( self.outputPath, "FastLMM_analysis.log"), "wb")
        
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
            
        # Check the covariable file (if plink required because it means .ped file is present)
        if no_plink == False:   
            try:
                Logger.get_instance().info("\nChecking the covariable file...\n------------------------------")
                self.check_covariable_file()
            except Exception as e:
                Logger.get_instance().error( "An exception occurred while checking the covariable data file:")
                Logger.get_instance().error( str(e))
                return
            
        # Launch the plink utility to build the binary version of ped and map files if it does not exists
        if no_plink == False:
            Logger.get_instance().info( "\nGenerating Bed file of DGRP SNP information...\n------------------------------")
            plink_out_file = os.path.join( self.outputPlinkPath, "FastLMM.data." + self.genotypeFileName)
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
            plink_command = "plink --noweb --file " + os.path.join( self.outputPlinkPath, self.genotypeFileName) + " --make-bed --out " + plink_out_file
            self.launch_command( plink_command, outfile)
            # -- the files produced by plink are the files to use 
            self.genotypeFileName = plink_out_file
            Logger.get_instance().info( "  Bed file generated")
        else:
            Logger.get_instance().info( "\nBypassing plink execution on genotype data\n--------------------------------------------")
        
        # Show the cluster of genotypes using the bed file
#         gsm_fig_path = self.genotypeFileName + "_gsm.png"
#         if not os.path.isfile( gsm_fig_path):
#             Logger.get_instance().info( "\nGenerating Similarity Matrix from BED file...\n------------------------------")
#             clusterer = ClusterData()
#             clusterer.execute( self.genotypeFileName + ".bed", gsm_fig_path)
        
        # Run GWAS
        Logger.get_instance().info("\nExecuting fast-LMM GWAS....\n------------------")
        geno_gwas = self.genotypeFileName
        pheno_gwas = self.phenotypeFileName
        cov_gwas = self.covariableFileName
        Logger.get_instance().info(" Genotype = " + geno_gwas)
        Logger.get_instance().info(" Phenotype = " + pheno_gwas)
        Logger.get_instance().info(" covariable = " + cov_gwas)
        try:
            #-- execute the GWAS in mode LMM(all)
            results_df = single_snp( geno_gwas, pheno_gwas, covar = cov_gwas)
        except Exception as e:
            Logger.get_instance().error( "ERROR: an exception occurred during Fast-LMM GWAS of '" + pheno_gwas, "' on genotype '" + geno_gwas + "' with covariable '" + cov_gwas + "'")
            Logger.get_instance().error( "  error is : " + str( e))
            return
        except Error as e:
            Logger.get_instance().error( "ERROR: an error occurred during Fast-LMM GWAS of '" + pheno_gwas, "' on genotype '" + geno_gwas + "' with covariable '" + cov_gwas + "'")
            Logger.get_instance().error( "  error is : " + str( e))
            return
        
        # Generating the analysis results
        
        # -- Plot the Manhattan plot of the result
        chromosome_starts = flutil.manhattan_plot(results_df.as_matrix(["Chr", "ChrPos", "PValue"]),pvalue_line=1e-5,xaxis_unit_bp=False)
        manathan_plot_filename = os.path.join( self.outputPath, os.path.splitext( os.path.basename( self.phenotypeFileName))[0] + "_manathanPlot.png")
        Logger.get_instance().info( "|--Saving Manhattan plot in" + manathan_plot_filename) 
        pylab.savefig( fname = manathan_plot_filename, format = "png")
        Logger.get_instance().info("|--Manhattan plot saved.")
        
        # -- Plot the QQ-plot
        fighandle, qnull, qemp = plotp.qqplot( results_df["PValue"].values)
        qqplot_plot_filename = os.path.join( self.outputPath, os.path.splitext( os.path.basename( self.phenotypeFileName))[0] + "_QQPlot.png")
        Logger.get_instance().info( "|--Saving QQplot in" + qqplot_plot_filename) 
        pylab.savefig( fname = qqplot_plot_filename, format = "png")
        pd.set_option('display.width', 1000)
        Logger.get_instance().info("|--QQplot saved.")
        
        # -- Save the complete result to file
        result_file_path = os.path.join(  self.outputPath, os.path.splitext( os.path.basename( self.phenotypeFileName))[0] + "_GWASresults.txt")
        results_df.to_csv( result_file_path, sep='\t', index= False)
        Logger.get_instance().info( "|--Result file created : " + result_file_path)
        
        # -- Filter the significant results to a new file
        signif_result_path = self.filterSignificantSNP( result_file_path)
        Logger.get_instance().info( "|--Significant result file created:" + signif_result_path)
        
        Logger.get_instance().info( "\nFinished.\n")
        
        # Close log file
        Logger.get_instance().close()
    
    
    #
    # Build the plink files required by the fast-LMM starting from the global GDRP file and
    # keeping only the desired families
    #
    # @param outfile : File - the file where the output of the used shell command will be written
    #
    def build_family_genotype(self, outfile):

        # Create the ped file from the DGRP and families file
        command = "plink --noweb --recode" + \
                    " --bfile "+ self.dgrpFile +\
                    " --keep " + self.families + \
                    " --out " + os.path.join( self.outputPlinkPath, self.genotypeFileName)
                    
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
                raise Exception( "ERROR : A phenotype file does not have 3 columns (" + str( len( row)) + " instead) separated by spaces:" + self.phenotypeFileName)
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
        ordered_filename = os.path.splitext( os.path.basename( self.phenotypeFileName))[0] + FastLMMWrapper.PHENOTYPE_FILE_ORDERED_EXTENSION + ".txt"
        ordered_filepath = os.path.join( self.outputPlinkPath, ordered_filename)
        if produce_order:
            Logger.get_instance().info( "Writing ordered phenotype file...")
            try:
                # Produce the name of the ordered file and open it
                ordered_file = open( ordered_filepath, "w")
                # Write the headers
                #ordered_file.write( " ".join( headers) + "\n")
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
    # Check if the covariable file has the family and individuals classified in the same order
    # If not create a file of ordered family and individuals
    #
    # @param outfile : File - the file where the output of the used shell command will be written
    #
    def check_covariable_file( self):
        
        # Read the genotype data file
        Logger.get_instance().info( "Reading genotype file : " + self.genotypeFileName)
        geno_csv_file = open( os.path.join( self.outputPlinkPath, self.genotypeFileName + ".ped"))
        geno_reader = csv.reader( geno_csv_file, delimiter=' ', quoting=csv.QUOTE_NONE)
        
        # Get the list of family names with the order in the .ped file
        family_names = []
        for row in geno_reader:
            family_names.append( self.getKey( row[0], row[1]))
        
        # Read the covariable data file
        Logger.get_instance().info( "Reading covariable file : " + self.covariableFileName)
        cov_csv_file = open( self.covariableFileName)
        cov_reader = csv.reader( cov_csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)

        # Parse the covariable data file
        # If the columns are not the correct ones, an exception is raised
        # If ok, keep the headers and store the list of family name both as a list and a dict mapping them to their file line
        fid_dict ={}
        fid_list = []
        for row in cov_reader:
            if len( row) < 3:
                raise Exception( "ERROR : A covariable file does not have more than 3 columns (" + str( len( row)) + " instead) separated by tab:" + self.covariableFileName)
            fid = row[ 0]
            iid = row[ 1]
            key = self.getKey( fid, iid)
            fid_list.append( key)
            fid_dict[ key] = " ".join( row)
        
        # Look if the phenotype family order is the same as the genotype family order
        produce_order = False
        for index in range( 0, len( fid_list)):
            if family_names[ index] != fid[ index]:
                Logger.get_instance().info( "  WARNING : covariable data are not organized by family like genotype data. Generating ordered file...")
                produce_order = True
                break

        # Copy the covariable file to plink working folder changing its name to avoid multi-thread collision or,
        # if required, create a covariable data file ordered by family like the genotype data
        ordered_filename = os.path.splitext( os.path.basename( self.covariableFileName))[0] + "_" + os.path.splitext( os.path.basename( self.phenotypeFileName))[0] + FastLMMWrapper.PHENOTYPE_FILE_ORDERED_EXTENSION + ".txt"
        ordered_filepath = os.path.join( self.outputPlinkPath, ordered_filename)
        if produce_order:
            Logger.get_instance().info( "Writing ordered covariable file...")
            try:
                # Produce the name of the ordered file and open it
                ordered_file = open( ordered_filepath, "w")
                # Add the phenotype information ordered by family like genotype file
                for family_name in family_names:
                    ordered_file.write( fid_dict[ family_name] + "\n")
                    ordered_file.flush()
                # Close the file
                ordered_file.close()
                Logger.get_instance().info( "  Ordered covariable data file produced : " + ordered_filename + "\n")
            except KeyError:
                raise Exception( "ERROR : A family name does not exist in covariable data but is present in genotype data:" + family_name)
        else:
            copyfile( self.covariableFileName, ordered_filepath)
        
        # Replace the original covariable file by the ordered one
        self.covariableFileName = ordered_filepath
    
    
    #
    # Filter out the significant SNP from the whole result file and write them to a new file
    #
    # @param result_file_path : string -the path to the GWAS result file
    # 
    def filterSignificantSNP(self, result_file_path):
        
        header_line = ""
        significant_lines = []
        
        with open( result_file_path) as result_file:
            for line in result_file:
                tokens = line.split( "\t")
                try:
                    pvalue = float( tokens[5])
                    if( pvalue < self.alpha):
                       significant_lines.append( line) 
                except ValueError:
                    header_line = line

        signif_result_path = os.path.splitext( result_file_path)[0] + FastLMMWrapper.RESULT_FILE_SIGNIFICANT_EXTENSION + str(self.alpha) + ".txt"
        output_file = open( signif_result_path, "w")
        output_file.write( header_line)
        for line in significant_lines:
            output_file.write( line)
            
        output_file.close()
        
        return signif_result_path
            
                    
    
    
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
    


