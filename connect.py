import mysql.connector
from mysql.connector import Error

try:
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_notes',  
        port=3308  #SESUAIN PORTNYA
    )

    if db.is_connected():
        print("Koneksi ke database berhasil.")
except Error as e:
    print(f"Error: {e}")
finally:
    if 'db' in locals() and db.is_connected():
        db.close()
        print("Koneksi ke database ditutup.")
