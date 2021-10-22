# -*- coding: utf-8 -*-

import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import exc

from posix import remove

from util import Constants

from util.log.Logger import Logger
from util.sql.Base import Base
from util.exception.SNPnetException import SNPnetException


from model.DBParameter import DBParameter


class SqlManager(object) :

    __instance = None

    def __init__(self):
        self.DBPath = None
        self.session = None

    def get_session(self):
        if(self.session == None):
            # Create engine to dedicated database
            engine = create_engine(Constants.PATH_SQL_BASE + self.DBPath)

            # Open the DB session
            session = sessionmaker()
            session.configure(bind=engine, autoflush=True, expire_on_commit=False)

            # Get the session and insert several objects in ENSEMBL table
            self.session = session()

        return self.session


    def close_session(self):
        self.session.close()
        self.session = None
        return

    # #
    # Set the path to the DB file
    #
    # @param path : string - the path to the DB file
    #    
    def set_DBpath(self, path):
        self.DBPath = path

    # #
    # Returns the path to the DB file
    #
    # @return the path to the DB file
    #        
    def get_DBpath(self):
        
        return self.DBPath
    
    # #
    # Returns the folder the DB is located in
    #
    # @return the folder the DB is located in
    #
    def get_DBfolder(self):
        
        return os.path.dirname( self.DBPath)

    # #
    # Returns a SQLalchemy engine to the DB file
    #
    # @return a SQLalchemy engine to the DB file
    #    
    def get_engine( self):

        if self.DBPath != None:
            engine = create_engine(Constants.PATH_SQL_BASE + self.DBPath)
            return engine
        
        return None

    # #
    # Commit the actual session and close it after
    #
    # @return None
    def commit( self ):
        
        try:
            self.session.commit()
        except exc.SQLAlchemyError as sqle:
            self.rollback_session()
            raise SNPnetException( "SqlManager.commit : An error occurred while committing the session.", sqle )
        finally:
            self.close_session()

    # #
    # Rollback the actual session
    #
    # @return None
    def rollback_session(self):
        
        try:
            self.session.rollback()
        except exc.SQLAlchemyError as sqle:
            raise SNPnetException( "SqlManager.rollback : An error occurred while rollbacking the session.", sqle )
        
        

    def commit_to_base(self, sessionSQL):
        try:
            sessionSQL.commit()
        except:
            Logger.get_instance().critical('Impossible to commit')


    def delete(self, obj):
        
        if obj != None:
            self.session.delete( obj)
        

    def build_database(self, path, keep_file=True):
        if keep_file == False:
            try:
                remove(path)
                Logger.get_instance().info('File : "' + str(path) + '" deleted.')
            except:
                Logger.get_instance().info('Can not delete file : ' + str(path))
                pass

        # Create engine to dedicated database
        engine = create_engine(Constants.PATH_SQL_BASE + path)

        # Open the DB session
        session = sessionmaker()
        session.configure(bind=engine)

        # Create all the required table in DB according to class model
        Base.metadata.create_all(engine)

        self.DBPath = path

        Logger.get_instance().info('File created : ' + str(path))

    @staticmethod
    def get_instance():

        if SqlManager.__instance == None:
            SqlManager.__instance = SqlManager()
        return SqlManager.__instance
    
    
    
    
    # 
    # Check if the database contains a value for the provided parameter in the DBParameter table
    # If not, the parameter with the user value is inserted in the database
    # If so, check if the provided user value is consistent with the database value
    # If there is an inconsistency, process is aborted
    #
    # @param sql_session : The SQL session
    # @param parameter_name : string - the name of the parameter
    # @param user_value : any - the value provided by the user for the parameter
    # 
    # @return None
    # @raise SNPnetException : if there is inconsistency between parameter the database value and the user value
    @staticmethod
    def check_db_parameter( sql_session, parameter_name, user_value):
        
        log_instance = Logger.get_instance()
        query = sql_session.query( DBParameter.parameterValue).filter( DBParameter.parameterName == parameter_name).first()
        if query == None or len( query) == 0:
            log_instance.info( "DataProcessor.__init__ : Database was set in mode '" + parameter_name + "=" + str( user_value) + "'")
            norm_parameter = DBParameter( parameter_name, Constants.BOOLEAN_TYPE_STRING, str( user_value))
            sql_session.add( norm_parameter)
            sql_session.commit()
        else:
            db_value = str( query[0])
            if( db_value != str( user_value)):
                log_instance.error( "DataProcessor.__init__ : Database is set in mode '" + parameter_name + "=" + db_value +
                                    "' whereas user asked for mode '" + parameter_name + "= " + str( user_value) + "'.\nThis inconsistency force to abort the process.")
                raise SNPnetException( "ExecutionStrategy.check_db_parameter : Database is set in mode '" + parameter_name + "=" + db_value +
                                    "' whereas user asked for mode '" + parameter_name + "= " + str( user_value) + "'. This inconsistency force to abort the process.")



    # #
    # Export the content of the given table to CSV file (tab separated)
    # 
    # @param table_name : string - the name of the DB table to export
    # @param output_path : string - the path to the output file
    def export_table( self, table_name, output_path):
        
        # Connect to the database
        import sqlite3
        con = sqlite3.connect( self.DBPath)
        
        # Create the CSV output file
        import csv
        outfile = open( output_path, "w")
        outcsv = csv.writer( outfile,  delimiter='\t')
        
        # Execute the query on DB
        cursor = con.execute( "select * from " + table_name)
        
        # Dump table column headers
        headers = []
        for header in cursor.description:
            headers.append( header[0])
        outcsv.writerow( headers)
        
        # Dump the table rows
        outcsv.writerows(cursor.fetchall())
        
        # Close the file
        outfile.close()
        
        
        
        
        
        
        
        