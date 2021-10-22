
from util.log.Logger import Logger
from util.file.FileUtils import FileUtils
from util.gwas.FastLMMWrapper import FastLMMWrapper  


class GwasUtil( ExecutionStrategy):

    #
    # Read the file containing the definition of the Fast-LMM analysis to perform produced by the single age analysis (step 3)
    #
    # @param file_path : string - The path to the Fast-LMM analysis definition file
    #
    # @return tuple - A list of dictionary containing the Fast-LMM analysis to perform (one dictionary per analysis)
    @staticmethod
    def read_fastlmm_gwas_analysis_definition( file_path):
        
        # Open a file_handle in reading mode for the data file.
        file_handle = FileUtils.open_text_r( file_path )

        # 'data_file' contains list of lines in the data file.
        fatslmm_data_file = file_handle.readlines()
        
        #Parse the line of the file and keep build a list of dictionary containing the
        # parameters of the Fast-LMM command to execute.
        command_dict_list = []
        first_line = True
        line_number = 0
        for line in fatslmm_data_file:
            line_number += 1
            
            # Ignore void lines
            if line == None:
                continue
            line = line.strip('\n\r')
            if line == '':
                continue
            
            # The first line is the header line
            if first_line:
                first_line = False
                # Get the headers
                headers = line.split( ";")
                Logger.get_instance().info(" Headers of Fast-LMM definition file are:\n" + str( headers))
            # The other lines may contain the parameters of a Fast-LMM command
            else:
                values= line.split( ";")
                # If the line does not have the same number of columns that the headers, the line is ignored
                # and an error message is launched
                if len( values) != len( headers):
                    Logger.get_instance().error( "ERROR: Abnormal line (bad column number) in Fast-LMM execution file (line " + str( line_number) + ":" + \
                                                 "\n-->Values are : " + str( values) + \
                                                 "\n-->Headers are: " + str( headers))
                    continue
                
                # Build the dictionary of parameters
                current_dict = {}
                for column_index in range(0, len( headers)):
                    current_dict[ headers[ column_index]] = values[column_index]
                
                # Store the dictionary
                command_dict_list.append( current_dict)
        
        Logger.get_instance().info("Number of Fast-LMM analysis to perform: " + str( len( command_dict_list)))
            
        return( command_dict_list)

    
    #
    # Execute the Fast-LMM analysis using the parameters provided in the dictionaries in the list
    #
    # @param analysis_command_list : tuple - A list of dictionary containing the Fast-LMM analysis to perform (one dictionary per analysis)
    #
    @staticmethod
    def execute_fastlmm_analysis( analysis_command_list, genotype_file_name, covariable_file_name, dgrp_file_path, alpha):
        
        for analysis_dict in analysis_command_list:
            
            # Get the value of the options build the FastLMM object 
            input_path = analysis_dict[ "input"]
            #genotype_file_name = analysis_dict[ "genotype"] 
            phenotype_file_name = analysis_dict[ "phenotype"]
            #covariable_file_name = analysis_dict[ "covariable"]
            no_plink = False
            #dgrp_file_path = analysis_dict[ "dgrp"]
            families_file_path = analysis_dict[ "families"]
            #alpha = 0.05
            
            genotype_file_name = "GWAS_DGRP";
            
            # Inform user about Analysis launched
            Logger.get_instance().info( "Executing Fast-LMM GWAS with options:")
            Logger.get_instance().info( "----------------------------")
            Logger.get_instance().info( "  input folder = " + str( input_path))
            Logger.get_instance().info( "  genotype     = " + str( genotype_file_name))
            Logger.get_instance().info( "  covariable   = " + str( covariable_file_name))
            Logger.get_instance().info( "  phenotype    = " + str( phenotype_file_name))
            Logger.get_instance().info( "  no plink     = " + str( no_plink))
            Logger.get_instance().info( "  DGRP file    = " + str( dgrp_file_path))
            Logger.get_instance().info( "  families     = " + str( families_file_path))
            Logger.get_instance().info( "  alpha        = " + str( alpha))
            
            # Check if one of the required option is missing
            if( input_path == None or genotype_file_name == None or phenotype_file_name == None or covariable_file_name == None):
                parser.print_help()
                
            # Insert the data to be treated with GWAS to database
            self.insert_gwas_data_to_db( input_path, genotype_file_name, phenotype_file_name, covariable_file_name, alpha)
            
            # Build the FastLMM object and execute it
            fastlmm_gwas = FastLMMWrapper( input_path, genotype_file_name, phenotype_file_name, covariable_file_name, alpha, dgrp_file_path, families_file_path)
            fastlmm_gwas.execute( no_plink)


    
    