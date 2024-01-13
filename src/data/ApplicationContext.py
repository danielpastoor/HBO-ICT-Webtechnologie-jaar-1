import os
from typing import TypeVar

import mysql.connector
from mysql.connector import Error

from src.models.BaseModel.TransientObject import TransientObject


class ApplicationContext:

    def __init__(self):
        self.__connection = None
        self.__host_name = os.environ.get("DATABASE_HOST")
        self.__user_name = os.environ.get("DATABASE_USERNAME")
        self.__user_password = os.environ.get("DATABASE_PASSWORD")
        self.__database = os.environ.get("DATABASE_NAME")
        self.__port = os.environ.get("DATABASE_PORT")

    def __connect(self):
        if self.__connection == None:
            try:
                self.__connection = mysql.connector.connect(
                    database=self.__database,
                    host=self.__host_name,
                    user=self.__user_name,
                    passwd=self.__user_password,
                    port=self.__port
                )
                print("Connection to MySQL DB successful")
            except Error as e:
                print(f"The error '{e}' occurred")

        print("Connection to MySQL DB successful")
        return self.__connection

    def Get[T:TransientObject](self, itemType:T, column: str = "*", condition: str =  None ) -> list[T]:
        query = f"SELECT {column} FROM {self.__GetTableName(type(itemType))}"

        if( condition is not None):
            query += f" WHERE {condition}"

        cursor = self.__connect().cursor(dictionary=True)

        result: list[T] = list[T]()
        try:
            cursor.execute(query)
            tmpResult = cursor.fetchall()

            for r in tmpResult:
                tmpItem : TransientObject = type(itemType)()
                tmpItem.SetCurrent(r)
                result.append(tmpItem)

        except Error as e:
            print(f"The error '{e}' occurred")

        return result

    def Add[T](self, data: T):
        self.__execute_query(self.ins_query_maker(self.__GetTableName(type(data)), data.GetCurrent()))

    def Delete[T](self, itemType:T, Id):
        delete_comment = f"DELETE FROM {self.__GetTableName(type(itemType))} WHERE id = {Id}"
        self.__execute_query(delete_comment)

    def Update[T](self, itemType:T, data: dict[str, object], id):
        update_query = f"""
            UPDATE
              {self.__GetTableName(type(itemType))}
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
            print(keys[i])
            print(type(rowdict[keys[i]]).__name__)
            print(type(rowdict[keys[i]]).__name__ == 'NoneType')
            if (type(rowdict[keys[i]]).__name__ == 'str' or type(rowdict[keys[i]]).__name__ == 'datetime'):
                sql += '\'' + str(rowdict[keys[i]]) + '\''
            elif (type(rowdict[keys[i]]).__name__ == 'NoneType'):
                print("add null")
                print(sql)
                sql += ' NULL'

                print(sql)
            else:
                sql += str(rowdict[keys[i]])

            if (i < dictsize - 1):
                sql += ', '
                print("insert into " + str(tablename) + " (" + ", ".join(keys) + ") values (" + sql + ")")
        return "insert into " + str(tablename) + " (" + ", ".join(keys) + ") values (" + sql + ")"

    def __GetTableName(self, type) -> str:
        name = type.__name__

        return name.replace("Entity", " ").lower()

