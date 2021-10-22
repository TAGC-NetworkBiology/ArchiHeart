# -*- coding: utf-8 -*-


## SQLAlchemyUtil
#  ==============
#
# Utils for SQL Alchemy returns objects.
class SQLAlchemyUtil(object):

    # format_list_column
    # ------------------
    #
    #    @param sql_alchemy_list : sql query result list (proceed on column).
    #
    # Loop on sql_alchemy_list and format the value, then append it into
    # the result list.
    #
    # Return result.
    #
    # @return list<String> or list<Integer> or list<Float>
    @staticmethod
    def format_list_column(sql_alchemy_list):
        result = [e[0] for e in sql_alchemy_list]
        return result

    # format_list_object
    # ------------------
    #
    #    @param sql_alchemy_list : sql query result list
    #                                            (proceed on complete object).
    #
    # Loop on sql_alchemy_list and format the value, then append it into
    # the result list.
    #
    # Return result.
    #
    # @return list<object>
    @staticmethod
    def format_list_object(sql_alchemy_list):
        result = [e for e in sql_alchemy_list]
        return result
