import datetime
import os
from typing import TypeVar

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash

from src.data.UserEntity import UserEntity
from src.models.BaseModel.TransientObject import TransientObject
from src.models.ContactMessageEntity import ContactMessageEntity


class ApplicationContext:

    def __init__(self):
        self.__connection = None
        self.__host_name = os.environ.get("DATABASE_HOST")
        self.__user_name = os.environ.get("DATABASE_USERNAME")
        self.__user_password = os.environ.get("DATABASE_PASSWORD")
        self.__database = os.environ.get("DATABASE_NAME")
        self.__port = os.environ.get("DATABASE_PORT")

    def __connect(self):
        if self.__connection is None:
            try:
                self.__connection = mysql.connector.connect(
                    database=self.__database,
                    host=self.__host_name,
                    user=self.__user_name,
                    passwd=self.__user_password,
                    port=self.__port
                )
            except Error as e:
                print(f"The error '{e}' occurred")

        return self.__connection

    def First[T:TransientObject](self, itemType: T, column: str = "*", condition: str = None,
                                 join: str = None) -> T | None:
        data = self.Get(itemType, column, condition, join)

        if data is None or len(data) == 0:
            return None

        return data[0]

    def Get[T:TransientObject](self, itemType: T, column: str = "*", condition: str = None, join: str = None) -> list[
        T]:
        query = f"SELECT {column} FROM {self.__GetTableName(type(itemType))}"

        if (join is not None):
            query += f" {join}"

        if condition is not None:
            query += f" WHERE {condition}"

        print(query)

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

    def Add[T](self, data: T) -> int | None:
        return self.__execute_insert_query(self.ins_query_maker(self.__GetTableName(type(data)), data.GetCurrent()))

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

    def __execute_insert_query(self, query) -> int | None:
        cursor = self.__connect().cursor()
        try:
            cursor.execute(query)
            self.__connect().commit()
            print("Query executed successfully")
            return cursor.getlastrowid()
        except Error as e:
            print(f"The error '{e}' occurred")

        return None

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
                    housenumber=user_data['housenumber'],
                    is_admin=user_data['is_admin']  # Added is_admin attribute
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

    def get_user_id_by_username(self, username):
        query = f"SELECT id FROM users WHERE username = '{username}'"
        cursor = self.__connect().cursor(dictionary=True)
        try:
            cursor.execute(query)
            result = cursor.fetchone()  # Fetches the first row of the result
            return result['id'] if result else None
        except Error as e:
            print(f"Error fetching user id by username: {e}")
            return None
        finally:
            cursor.close()

    def save_contact_message(self, contact_message: ContactMessageEntity):
        """Slaat een chatbericht op in de database."""
        insert_query = """
        INSERT INTO contact_messages (user_id, email, name, message, sent_on) 
        VALUES (%s, %s, %s, %s, %s)
        """
        data = (
            contact_message.user_id,
            contact_message.email,
            contact_message.name,
            contact_message.message,
            contact_message.sent_on
        )

        try:
            cursor = self.__connect().cursor()
            cursor.execute(insert_query, data)
            self.__connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Fout bij het opslaan van het chatbericht: {e}")
            return False

    def get_dashboard_data(self):
        """Fetch counts for the admin dashboard from multiple tables."""
        data = {}
        cursor = None  # Initialize cursor

        try:
            self.__connect()
            cursor = self.__connection.cursor(dictionary=True)

            # Count data in the 'accommodation' table
            cursor.execute("SELECT COUNT(id) AS count FROM accommodation")
            data['total_accommodations'] = cursor.fetchone()['count']

            # Count data in the 'booking' table
            cursor.execute("SELECT COUNT(id) AS count FROM booking")
            data['total_bookings'] = cursor.fetchone()['count']

            # Count data in 'contact_messages' table
            cursor.execute("SELECT COUNT(inzending_id) AS count FROM contact_messages")
            data['total_contact_messages'] = cursor.fetchone()['count']

            # Count data in 'users' table
            cursor.execute("SELECT COUNT(id) AS count FROM users")
            data['total_users'] = cursor.fetchone()['count']

        except Error as e:
            print(f"The error '{e}' occurred")
        finally:
            if cursor is not None:
                cursor.close()

        return data

    def get_all_users(self):
        """Fetch all users from the users table."""
        users = []
        try:
            self.__connect()
            if self.__connection.is_connected():
                cursor = self.__connection.cursor(dictionary=True)
                cursor.execute("SELECT id, username, email, city, postcode, address, housenumber, created_at, "
                               "credit_card, is_admin FROM users")
                users = cursor.fetchall()
                cursor.close()
            else:
                print("Failed to connect to the database")
        except Error as e:
            print(f"Error fetching users: {e}")
        finally:
            if self.__connection and self.__connection.is_connected():
                self.__connection.close()
        return users

    def register_user(self, user_data):
        """
        Registers a new user in the database.
        """
        try:
            self.__connect()
            cursor = self.__connection.cursor()

            # Prepare the SQL query
            query = """
            INSERT INTO users (username, email, password, city, postcode, address, housenumber, is_admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            # Unpack user data and insert into the database
            cursor.execute(query, (
                user_data['username'],
                user_data['email'],
                user_data['password'],  # Assuming password is already hashed
                user_data['city'],
                user_data['postcode'],
                user_data['address'],
                user_data['housenumber'],
                user_data['is_admin']  # Should be an integer (1 or 0)
            ))

            self.__connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error registering user: {e}")
        finally:
            if self.__connection and self.__connection.is_connected():
                self.__connection.close()

    def submit_booking(self, booking_data):
        """Submits a new booking to the database."""
        cursor = None
        booking_date = datetime.datetime.now()  # or the appropriate date-time value

        # Add the booking_date
        booking_data['booking_date'] = booking_date
        try:
            self.__connect()
            cursor = self.__connection.cursor()
            query = """
            INSERT INTO booking (user_id, booking_date, start_date, end_date, accommodation_id, special_requests)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                booking_data['user_id'],
                booking_data['booking_date'],
                booking_data['start_date'],
                booking_data['end_date'],
                booking_data['accommodation_id'],
                booking_data['special_requests']
            ))
            self.__connection.commit()
        except Error as e:
            print(f"Error submitting booking: {e}")
            return False
        finally:
            if cursor:
                cursor.close()
            if self.__connection.is_connected():
                self.__connection.close()
        return True

    def get_all_accommodations(self):
        """Fetches all accommodation IDs and names."""
        accommodations = []
        cursor = None
        try:
            connection = self.__connect()  # Get a connection
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id, name FROM accommodation"  # Adjust to select id and name
            cursor.execute(query)
            accommodations = cursor.fetchall()  # Fetches a list of dictionaries
        except Error as e:
            print(f"Error fetching accommodations: {e}")
        finally:
            if cursor:
                cursor.close()
        return accommodations

    def get_all_usersnamess(self):
        """Fetches all user IDs and usernames."""
        users = []
        cursor = None
        try:
            connection = self.__connect()  # Get a connection
            cursor = connection.cursor(dictionary=True)
            query = "SELECT id, username FROM users"  # Adjust to select id and username
            cursor.execute(query)
            users = cursor.fetchall()  # Fetches a list of dictionaries
        except Error as e:
            print(f"Error fetching users: {e}")
        finally:
            if cursor:
                cursor.close()
        return users

    def delete_user(self, user_id):
        try:
            self.__connect()
            cursor = self.__connection.cursor()
            query = "DELETE FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            self.__connection.commit()
            cursor.close()
        except Error as e:
            print(f"Error deleting user: {e}")
            raise e

    def get_user_by_id(self, user_id):
        """
        Fetches a user by their ID from the database.
        """
        cursor = None
        try:
            self.__connect()
            cursor = self.__connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user_data = cursor.fetchone()
            return user_data  # This will be a dictionary with the user's data
        except Error as e:
            print(f"Error fetching user by ID: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def get_all_accommodations_manage(self):
        """
        Retrieves all accommodations along with their Price and Max Persons from the database.
        """
        accommodations = []
        cursor = None
        try:
            self.__connect()
            cursor = self.__connection.cursor(dictionary=True)
            query = "SELECT id, name, price, max_persons, location FROM accommodation"
            cursor.execute(query)
            accommodations = cursor.fetchall()
        except Error as e:
            print(f"Error fetching accommodations: {e}")
        finally:
            if cursor:
                cursor.close()
        return accommodations

    def add_accommodation(self, accommodation_data):
        """
        Adds a new accommodation record to the database.
        """
        cursor = None
        try:
            self.__connect()
            cursor = self.__connection.cursor()

            query = """
            INSERT INTO accommodation (name, price, description, created_at, max_persons, thumbnail_image, images)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (
                accommodation_data['name'],
                accommodation_data['price'],
                accommodation_data['description'],
                datetime.datetime.now(),  # current timestamp
                accommodation_data['max_persons'],
                accommodation_data['thumbnail_image'],
                accommodation_data['images']  # this is a string representing image filenames
            ))

            self.__connection.commit()
            return True

        except Error as e:
            print(f"Error adding accommodation: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def get_all_contact_messages(self):
        """
        Fetches all chat messages with associated user names from the database.
        """
        messages = []
        cursor = None
        try:
            connection = self.__connect()
            cursor = connection.cursor(dictionary=True)
            # Adjust the SQL query according to your database schema
            query = """
                SELECT *
                FROM contact_messages
            """
            cursor.execute(query)
            messages = cursor.fetchall()
        except Error as e:
            print(f"Error fetching chat messages: {e}")
        finally:
            if cursor:
                cursor.close()
        return messages
