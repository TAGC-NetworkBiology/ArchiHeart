# -*- coding: utf-8 -*-

import os, shutil
# from string import rfind

import util.Constants as Constants

from util.exception.FileFormatException import FileFormatException
from util.exception.SNPnetException import SNPnetException

from util.log.Logger import Logger

## Class FileUtils
#  ===============
#
# This class contains static methods which allow to open, read, write file,
# or find extension of a file, in order to convert it.
class FileUtils(object):

    ## check_sql_file
    #  --------------
    #
    # Check if the sql_file_path exists
    #
    @staticmethod
    def check_sql_file( sql_file_path):

        if os.path.exists( str(sql_file_path)) == False:
            Logger.get_instance().critical( 'The SQLite file does not exist: ' + str(sql_file_path))
            raise SNPnetException( "The SQLite file does not exist" + str(sql_file_path))

    ## initialize_rep
    #  --------------
    #
    # Initialize all Phenosnip repertories
    #
    # Return nothing
    @staticmethod
    def initialize_rep():
        # If Phenosnip repertory does not exist
        try:
            # Create result repertory : '/home/Penosnip/'
            os.mkdir(Constants.DIR_RESULTS)
        except OSError as os_error:
            pass

        # Try to create Phenosnip/results
        try:
            os.mkdir(Constants.PATH_RESULTS)
        except OSError as os_error:
            pass

        # Try to create Phenosnip/results/images
        try:
            os.mkdir(Constants.IMAGES_RESULTS)
        except OSError as os_error:
            pass

        # Try to create Phenosnip/results/images/TEST
        try:
            os.mkdir(Constants.IMAGES_RESULTS_TEST)
        except OSError as os_error:
            pass

        # Try to create Phenosnip/results/reports
        try:
            os.mkdir(Constants.PATH_REPORTS)
        except OSError as os_error:
            pass

        # Try to create Phenosnip/results/reports
        try:
            os.mkdir(Constants.PATH_REPORTS_TEST)
        except OSError as os_error:
            pass


        return

    ##  open_text_r
    #   --------
    #
    # Open a text file in reading mode.
    # Write a critical error in log file in case of IOError
    #
    #    @param path : the input file's path
    #
    # Return :
    #    - file_handle : is an object of type 'file'
    @staticmethod
    def open_text_r(path):
        try:
            file_handle = open(path, 'r')
        except IOError as detail:
            raise SNPnetException( "FileUtils.open_text_r: Unable to open " + path + " : " + str(detail))

        return file_handle

    ## open_text_w
    #  -----------
    #
    # Open a text file in writing mode
    # Write a critical error in log file in case of IOError
    #
    #    @param path : the input file's path
    #
    # Return :
    #    - file_handle : is an object of type 'file'
    @staticmethod
    def open_text_w(path):
        try:
            file_handle = open(path, 'w')
        except IOError as detail:
            raise SNPnetException( "FileUtils.open_text_w: Unable to open " + path + " : " + str(detail))

        return file_handle

    # 
    # Create/open a file a file touching it 
    #
    @staticmethod 
    def touch_file(path, times=None):
        
        try:
            touched_file = FileUtils.open_text_w( path)
            os.utime( path, times)
            touched_file.close()
        except IOError as detail:
            raise SNPnetException( "FileUtils.touch_file: Unable to touch " + path + " : " + str(detail))        

    #
    # Copy a file provided in src to path in dest
    #
    # @param src : string - The path to the file to copy
    # @param dest : string - The destination file (complete file path)
    @staticmethod
    def copy_file( src, dest):
        
        try:
            shutil.copyfile( src, dest)
        except IOError as detail:
            raise SNPnetException( "FileUtils.copy_file: Unable to copy file " + src + " to " + dest + " : " + str(detail))
        

    #
    # Rename a file provided in src to path in dest
    #
    # @param src : string - The path to the file to rename
    # @param dest : string - The destination file (complete file path)
    @staticmethod
    def rename_file( src, dest):
        
        try:
            os.rename( src, dest)
        except IOError as detail:
            raise SNPnetException( "FileUtils.rename_file: Unable to rename file " + src + " to " + dest + " : " + str(detail))
                
    ##
    # Remove the file extension from the file name if it exists
    #
    # @param file_name the file name or file path
    #
    # @return the file_name without the file extension
    @staticmethod
#     def remove_extension( file_name):
#         
#         dot_index = rfind( ".", file_name)
#         
#         if( dot_index >0):
#             return file_name[0:dot_index]
#         else:
#             return file_name
        

    ## find_extension
    #  --------------
    #
    # Find extension of the given file in path by searching in path's name
    # the extension : 'txt', 'ods', 'xls', 'xlsx'
    #
    # @param path: file path from which it is needed to find extension.
    #
    # Return the extension in string uppercased format.
    #
    # @return String
    @staticmethod
    def find_extension(path):
        # Split the path name on the '.'
        path_name_list = path.split('.')

        # Keep the extension ( last item on the list)
        extension = path_name_list[-1]

        # Transform all letters of extension in uppercase
        extension = extension.upper()

        if extension not in Constants.EXTENSION_LIST:
            raise FileFormatException\
            ("FileFormatException when call FileUtils.find_extension( path) : " + path + \
            " is not a file among 'ODS', 'XLS', 'XLSX', 'TXT'. Extension '" + extension + \
            "' is not recognized. Please verify that the file indicates its extension after a '.' and that the extension is comprised in 'ODS, 'XLS', 'XLSX', or 'TXT'.")

        return extension
