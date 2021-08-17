"""Database Utilities

This script creates a connection to the walk2zero database. It also contains
all of the functions that query the database. These are within the
DbQueryFunction class.
"""

import mysql.connector as mysql
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass


class DbConnection:

    # Create connection
    @staticmethod
    def connect_to_db():
        cnx = mysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            auth_plugin='mysql_native_password',
            database='walk2zero'
        )
        return cnx


class DbQueryFunction:

    @staticmethod
    def check_email(email):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()

            query = f"SELECT email FROM users WHERE email = '{email}'"
            cur.execute(query)
            result = cur.fetchall()
            # email found     -> returns [('ewillams@gemail.com',)]
            # email not found -> returns []

            try:
                if result[0][0] == email:
                    return True
            except IndexError:  # if email not found, getting index [0][0] of
                return False    # empty list would through IndexError

        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def authenticate(check_email, check_password):
        try:
            # calling DB connection
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()

            # defining the query
            query = "SELECT email, pword FROM users"
            cur.execute(query)
            result = cur.fetchall()

            # converting the tuple query output to dictionary to have Key as email
            # and value as password
            user_dict = dict((x, y) for x, y in result)

            # Comparing the email and password in the dictionary to check_email and
            # check_password
            for key in user_dict.keys():
                if key == check_email:
                    if user_dict[key] == check_password:
                        return True
                    else:
                        return False

        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def fetch_user_details(email):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    SELECT user_id, fname, lname
                    FROM users 
                    WHERE email = '{email}'
                    """
            cur.execute(query)
            result = cur.fetchall()  # example output [(2, 'Owen', 'Parry')]
            user_dict = {
                "user_id": result[0][0],
                "fname": result[0][1],
                "lname": result[0][2]
            }
            return user_dict

        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def new_user(fname, lname, email, pword):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    INSERT INTO users (fname, lname, email, pword) 
                    VALUES ('{fname}', '{lname}', '{email}', '{pword}')
                    """
            cur.execute(query)
            db_connection.commit()

        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def get_new_user_id(email):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"SELECT user_id FROM users WHERE email = '{email}'"
            cur.execute(query)
            result = cur.fetchall()
            return result

        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def get_total_user_journeys(user_id):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    SELECT COUNT(journey_id)
                    FROM journeys
                    WHERE user_id = '{user_id}'
                    """
            cur.execute(query)
            result = cur.fetchall()
            total_user_journeys = result[0][0]
            return total_user_journeys

        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def get_total_co2_emitted(user_id):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    SELECT SUM(carbon_emitted)
                    FROM emissions
                    WHERE user_id = '{user_id}'
                    """
            cur.execute(query)
            result = cur.fetchall()
            total_co2_emitted = result[0][0]
            return total_co2_emitted

        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def get_total_co2_saved(user_id):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    SELECT SUM(carbon_saved)
                    FROM emissions
                    WHERE user_id = '{user_id}'
                    """
            cur.execute(query)
            result = cur.fetchall()
            total_co2_saved = result[0][0]
            return total_co2_saved

        except Exception:
            raise DbConnectionError("Failed to read data from DB")

        finally:
            if db_connection:
                db_connection.close()
