import mysql.connector
from config import USER, PASSWORD, HOST


class DbConnectionError(Exception):
    pass

# file to create functions to communicate with the database