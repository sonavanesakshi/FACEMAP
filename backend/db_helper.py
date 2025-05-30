import mysql.connector
import json
global cnx

#Create a connection to the database
cnx = mysql.connector.connect(
    host="localhost", 
    user="root", 
    password="Sakshi@123#", 
    database="project"
)

def login_user(username, password):
    try:
        cursor = cnx.cursor()

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        return user

    except mysql.connector.Error as err:
        print('err', err)
        return None
    
    except Exception as e:
        print(e, 'in the exception')
        cnx.rollback()
        return -1
    return None

def signup_user(username, password):
    try:
        cursor = cnx.cursor()

        fetch_query = "SELECT * FROM users WHERE username = %s"
        
        cursor.execute(fetch_query, (username,))
        user = cursor.fetchone()
        if user:
            return {"success": False, "message": "Username already exists."}
        
        signup_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(signup_query, (username, password))
        cnx.commit()
        cursor.close()
        return {"success": True, "message": "Signup successful!"}

    except mysql.connector.Error as err:
        print('err', err)
        return -1
    
    except Exception as e:
        print(e, 'in the exception')
        cnx.rollback()
        return -1
    return None

def insert_analysis_results(gender, age, acne_type, suggestions, filename):
    try:
        cursor = cnx.cursor()

        query = """
        INSERT INTO project.skin_analysis (gender, age, acne_type, suggestions, filename)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        cursor.execute(query, (gender, age, acne_type, json.dumps(suggestions), filename))
        cnx.commit()
        cursor.close()
        return 1

    except mysql.connector.Error as err:
        print('err', err)
        cnx.rollback()
        return -1
    
    except Exception as e:
        print(e, 'in the exception')
        cnx.rollback()
        return -1
    return None
