import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    'host': 'x-e.h.filess.io',
    'database': 'sertifikat_cheesemood',
    'user': 'sertifikat_cheesemood',
    'password': 'a3d775699a18566273a5f5072be7c09d96f29b6c',
    'port': 3305
}

def insert_file_to_db(file_data, filename, file_type):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        query = """
        INSERT INTO files (name, filename, filedata)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (file_type, filename, file_data))
        connection.commit()
    except Error as e:
        print(f"Error while inserting file to database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_file_from_db(filename, file_type):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT filedata FROM files
        WHERE filename = %s AND name = %s
        """
        cursor.execute(query, (filename, file_type))
        result = cursor.fetchone()
        return result['filedata'] if result else None
    except Error as e:
        print(f"Error while retrieving file from database: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
