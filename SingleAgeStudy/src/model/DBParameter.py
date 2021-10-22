from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import String

from util.sql.Base import Base

# #
# This class represent the status of the DB table, indicating if the table was correctly filled,
# filled with warning or with error or not filled
# 
class DBParameter( Base ):
    __tablename__ = "db_parameter"
    
    # The name of the parameter
    parameterName = Column( String, primary_key = True )
    # The parameter type
    parameterType = Column( String )
    # The parameter value
    parameterValue = Column( String )
    
    
    def __init__(self, p_name, p_type, p_value):
        
        self.parameterName = p_name
        self.parameterType = p_type
        self.parameterValue = p_value
        
    
        
        
    
