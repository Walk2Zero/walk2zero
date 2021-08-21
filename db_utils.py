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
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            # email found     -> returns [('ewillams@gemail.com',)]
            # email not found -> returns []
            try:
                if result[0][0] == email:
                    return True
            except IndexError:  # if email not found, getting index [0][0] of
                return False    # empty list would through IndexError
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def authenticate(email, pword):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"SELECT email, pword FROM users WHERE email = '{email}'"
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            if pword == result[0][1]:
                return True
            else:
                return False
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def fetch_user_details(email):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    SELECT user_id, fname, lname, pword
                    FROM users 
                    WHERE email = '{email}'
                    """
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()  # example output [(1, 'Elen', 'Williams', 'ewill95')]
            user_dict = {
                "user_id": result[0][0],
                "fname": result[0][1],
                "lname": result[0][2],
                "pword": result[0][3]
            }
            return user_dict
            # example output {'user_id': 1,
            #                 'fname': 'Elen',
            #                 'lname': 'Williams',
            #                 'pword': 'ewill95'}
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def enter_new_user(fname, lname, email, pword):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    INSERT INTO users (fname, lname, email, pword) 
                    VALUES ('{fname}', '{lname}', '{email}', '{pword}')
                    """
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            db_connection.commit()
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
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            return result[0][0]
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
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            total_user_journeys = result[0][0]
            return total_user_journeys
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
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            total_co2_emitted = result[0][0]
            return total_co2_emitted
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
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            total_co2_saved = result[0][0]
            return total_co2_saved[0][0]
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def fetch_all_vehicles():
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = """
                    SELECT vehicle_id, vehicle_name, carb_emit_km 
                    FROM vehicles
                    """
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            # Robyn's initial idea (remove from notes later):
            # vehicle_list = []
            # for i in result:
            #     vehicle = {
            #         "vehicle_id": i[0],
            #         "vehicle_name": i[1],
            #         "carb_emit_km": i[2]
            #     }
            #     vehicle_list.append(vehicle)
            #
            # Would have returned:
            #     [
            #         {
            #             'vehicle_id': 1,
            #              'vehicle_name': 'foot',
            #              'carb_emit_km': 0
            #          },
            #          {
            #              'vehicle_id': 2,
            #              'vehicle_name': 'bicycle',
            #              'carb_emit_km': 0
            #           }
            #           etc. ...
            #     ]
            return result
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def fetch_user_vehicles(user_id):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    SELECT uv.user_id, uv.vehicle_id 
                    FROM user_vehicles AS uv 
                    WHERE user_id = {user_id}
                    """
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            # Initial thoughts (remove from notes later):
            # user_vehicles = dict(result)  # e.g. {'foot': 0, 'transit': 127}
            return result
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def write_user_vehicles(user_id, vehicle_id):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    INSERT INTO user_vehicles (user_id, vehicle_id) 
                    VALUES ({user_id}, {vehicle_id})
                    """
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to write data from DB")
        else:
            db_connection.commit()
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def write_journey(user_id, journey_id, j_datetime, origin, destination,
                      distance, vehicle_id):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    INSERT INTO journeys 
                    (user_id, journey_id, j_datetime, origin, destination, 
                    distance, vehicle_id) 
                    VALUES 
                    ({user_id}, {journey_id}, '{j_datetime}', '{origin}', 
                    '{destination}', {distance}, {vehicle_id})
                    """
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to write data from DB")
        else:
            db_connection.commit()
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def write_journey_emissions(user_id, journey_id, carbon_emitted,
                                carbon_saved):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    INSERT INTO emissions 
                    (user_id, journey_id, carbon_emitted, carbon_saved) 
                    VALUES 
                    ({user_id}, {journey_id}, {carbon_emitted}, {carbon_saved})
                    """
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to write data from DB")
        else:
            db_connection.commit()
        finally:
            if db_connection:
                db_connection.close()

    @staticmethod
    def get_new_journey_id(user_id):
        try:
            db_connection = DbConnection.connect_to_db()
            cur = db_connection.cursor()
            query = f"""
                    SELECT max(journey_id) 
                    FROM journeys 
                    WHERE user_id = {user_id}
                    """
            cur.execute(query)
        except Exception:
            raise DbConnectionError("Failed to read data from DB")
        else:
            result = cur.fetchall()
            journey_id = result[0][0]
            return journey_id
        finally:
            if db_connection:
                db_connection.close()
