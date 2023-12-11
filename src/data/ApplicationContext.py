import os

import mysql.connector
from mysql.connector import Error

from src.models.BaseModel.TransientObject import TransientObject

class ApplicationContext:
    __connection = None
    __host_name = os.environ.get("DATABASE_HOST")
    __user_name = os.environ.get("DATABASE_USERNAME")
    __user_password = os.environ.get("DATABASE_PASSWORD")
    __database = os.environ.get("DATABASE_NAME")
    def __init__(self):
        pass

    def __connect(self):
        if self.__connection == None:
            try:
                self.__connection = mysql.connector.connect(
                    database=self.__database,
                    host=self.__host_name,
                    user=self.__user_name,
                    passwd=self.__user_password
                )
                print("Connection to MySQL DB successful")
            except Error as e:
                print(f"The error '{e}' occurred")

        return self.__connection

    def Get(self, table: str, column: str = "*", condition: str =  None ):
        query = f"SELECT {column} FROM {table}"

        if( condition is not None):
            query += f" WHERE {condition}"

        cursor = self.__connect().cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

        return result

    def Add(self, table: str, data: TransientObject):
        self.__execute_query(self.ins_query_maker(table, data.GetCurrent()))

    def Delete(self, table: str, Id):
        delete_comment = f"DELETE FROM {table} WHERE id = {Id}"
        self.__execute_query(delete_comment)

    def Update(self, table: str, data: dict[str, object], id):
        update_query = f"""
            UPDATE
              {table}
            SET
              {",".join([f"{key} = {value}" for key, value in data.items()])}
            WHERE
              id = {id}
        """

        self.__execute_query(update_query)

    # Helpers
    def __execute_query(self, query):
        cursor = self.__connect().cursor()
        try:
            cursor.execute(query)
            self.__connect().commit()
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def ins_query_maker(self, tablename:str, rowdict):
        keys = list(rowdict.keys())
        dictsize = len(rowdict)
        sql = ''
        for i in range(dictsize):
            if (type(rowdict[keys[i]]).__name__ == 'str'):
                sql += '\'' + str(rowdict[keys[i]]) + '\''
            else:
                sql += str(rowdict[keys[i]])
            if (i < dictsize - 1):
                sql += ', '
        return "insert into " + str(tablename) + " (" + ", ".join(keys) + ") values (" + sql + ")"
