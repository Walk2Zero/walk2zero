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


class DbQueryFunctions:

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
