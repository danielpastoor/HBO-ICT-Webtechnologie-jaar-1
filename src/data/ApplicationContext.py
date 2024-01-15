import os
from typing import TypeVar

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

from src.data.ContactFormEntity import ContactFormEntity
from src.data.UserEntity import UserEntity
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

    def First[T:TransientObject](self, itemType: T, column: str = "*", condition: str = None) -> T | None:
        data = self.Get(itemType, column, condition)

        if data is None or len(data) == 0:
            return None

        return data[0]

    def Get[T:TransientObject](self, itemType: T, column: str = "*", condition: str = None, join: str = None) -> list[T]:
        query = f"SELECT {column} FROM {self.__GetTableName(type(itemType))}"

        if (join is not None):
            query += f" {join}"

        if condition is not None:
            query += f" WHERE {condition}"

        cursor = self.__connect().cursor(dictionary=True)

        result: list[T] = list[T]()
        try:
            cursor.execute(query)
            tmpResult = cursor.fetchall()

            for r in tmpResult:
                tmpItem: TransientObject = type(itemType)()
                tmpItem.SetCurrent(r)
                result.append(tmpItem)

        except Error as e:
            print(f"The error '{e}' occurred")

        return result

    def Add[T](self, data: T):
        self.__execute_query(self.ins_query_maker(self.__GetTableName(type(data)), data.GetCurrent()))

    def Delete[T](self, itemType: T, Id):
        delete_comment = f"DELETE FROM {self.__GetTableName(type(itemType))} WHERE id = {Id}"
        self.__execute_query(delete_comment)

    def Update[T](self, itemType: T, data: dict[str, object], id):
        update_dict = {}

        for key, value in data.items():
            if type(value).__name__ == 'str' or type(value).__name__ == 'datetime':
                update_dict[key] = '\'' + str(value) + '\''
            elif type(value).__name__ == 'NoneType':
                update_dict[key] = ' NULL'
            else:
                update_dict[key] = str(value)

        update_query = f"""
            UPDATE
              {self.__GetTableName(type(itemType))}
            SET
              {",".join([f"{key} = {value}" for key, value in update_dict.items()])}
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

    def ins_query_maker(self, tablename: str, rowdict):
        keys = list(rowdict.keys())
        dictsize = len(rowdict)
        sql = ''
        for i in range(dictsize):
            if type(rowdict[keys[i]]).__name__ == 'str' or type(rowdict[keys[i]]).__name__ == 'datetime':
                sql += '\'' + str(rowdict[keys[i]]) + '\''
            elif type(rowdict[keys[i]]).__name__ == 'NoneType':
                sql += ' NULL'
            else:
                sql += str(rowdict[keys[i]])

            if i < dictsize - 1:
                sql += ', '
        return "insert into " + str(tablename) + " (" + ", ".join(keys) + ") values (" + sql + ")"

    def __GetTableName(self, type) -> str:
        # Check if the entity class has a __tablename__ attribute
        if hasattr(type, '__tablename__'):
            return type.__tablename__
        else:
            # Fallback to default naming convention
            name = type.__name__
            return name.replace("Entity", "").lower()

    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        cursor = self.__connect().cursor(dictionary=True)
        try:
            cursor.execute(query, (username,))
            user_data = cursor.fetchone()  # Fetching the user data as a dictionary

            if user_data:
                # Create and return a UserEntity object
                return UserEntity(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    city=user_data['city'],
                    postcode=user_data['postcode'],
                    address=user_data['address'],
                    housenumber=user_data['housenumber']
                )
            else:
                return None

        except Error as e:
            print(f"Error fetching user: {e}")
            return None

    def update_user_password(self, username, new_password):

        hashed_password = generate_password_hash(new_password)
        update_query = "UPDATE users SET password = %s WHERE username = %s"

        try:
            cursor = self.__connect().cursor()
            cursor.execute(update_query, (hashed_password, username))
            self.__connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error updating user password: {e}")
            return False

    def submit_contact_form(self, contact_form_entity: ContactFormEntity):
        """Inserts contact form data into the database."""
        insert_query = """
        INSERT INTO contactformulier_inzendingen (name, email, message, sent_on) 
        VALUES (%s, %s, %s, %s)
        """
        data = (
            contact_form_entity.name,
            contact_form_entity.email,
            contact_form_entity.message,
            contact_form_entity.sent_on
        )

        try:
            cursor = self.__connect().cursor()
            cursor.execute(insert_query, data)
            self.__connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error inserting contact form data: {e}")
            return False


