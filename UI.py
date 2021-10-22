from getpass import getpass
# importing 'mysql.connector' as mysql 
import mysql.connector as mysql

class DbConnectionError(Exception):
    pass

#DB Connection
def _connect_to_db():
    cnx = mysql.connect(
        host = "localhost",
        user = "root",
        passwd = "password",    #Reviewer Password
        database = "walk2zero"
    )
    return cnx

#Function to accept User Input
def user_reg():
    first_name = input("Please enter your first name = ")
    last_name = input("Please enter your last name = ")
    email = input("Please enter your email address = ")
    password = getpass("Please enter a desired password = ")
    new_registration(first_name,last_name,email,password)

#Function to log-in an exisiting user
def login():
    check_email = input("Please enter your email address = ")
    check_password = getpass("Please enter your password = ")
    verify_login(check_email,check_password)


#Function to register new user details into the DB
def new_registration(first_name,last_name,email,password):
    #calling DB connection
    db_connection = _connect_to_db()
    cur = db_connection.cursor()
    
    #defining the Query
    query = "INSERT INTO users (fname, lname, email, pword) VALUES (%s, %s,%s,%s)"
    
    #storing values in a variable
    values = (first_name, last_name,email,password)

    #executing the query with values
    cur.execute(query, values)
    db_connection.commit()  
    cur.close()
    print("Successful Registration!")
    print("")


#Function to verify login
def verify_login(check_email,check_password):
    try:
        #calling DB connection
        db_connection = _connect_to_db()
        cur = db_connection.cursor()

        #defining the query
        query = "SELECT email,pword FROM users"
        cur.execute(query)
        result = cur.fetchall()  

        #converting the tuple query output to dictionary to have Key as email and value as password       
        user_dict = dict((x, y) for x, y in result)

        #Comparing the email and password in the dictionary to check_email and check_password
        for key in user_dict.keys():
            if key == check_email:
                if user_dict[key] == check_password:
                    print("Successful Login!")
                else:
                    print("Incorrect Credentials. Please try logging in again!")
                    login()
            
    except Exception:
        raise DbConnectionError("Failed to read data from DB")
    
    finally:
        if db_connection:
            db_connection.close()
        print("")
      
        
#menu function
def menu():
    print ("Welcome to Walk2Zero!")
    print("")
    print ("Taking Climate Conscious Steps for a Cooler Earth!")
    print("")
    print ("1. New user. Register to the service")
    print ("2. Existing user. Login->")
    choice = int(input("Enter your choice = "))

    if choice == 1:
        user_reg()
    elif choice == 2:
        login()

def main():
    menu()
 
if __name__ == "__main__":
    main()




