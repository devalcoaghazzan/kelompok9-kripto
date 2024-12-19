import mysql.connector
from mysql.connector import Error

try:
    # Koneksi ke database MySQL
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_notes',  
        port=3308  
    )

    if connection.is_connected():
        print("Koneksi berhasil ke database test_db!")
        
        # Membuat cursor untuk menjalankan query
        cursor = connection.cursor()

        # Query untuk membuat tabel
        create_table_query = """
        CREATE TABLE IF NOT EXISTS coba (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        print("Tabel 'coba' berhasil dibuat atau sudah ada.")

except Error as e:
    print(f"Error: {e}")

finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()
        print("Koneksi ke database ditutup.")

# ini DIBAWAH BUAT DROP TABEL COBA ITUM GW NYOBA AJA UDH BISA KONEK BLM
#  if connection.is_connected():
#         print("Koneksi berhasil ke database test_db!")
        
#         # Membuat cursor untuk menjalankan query
#         cursor = connection.cursor()

#         # Query untuk menghapus tabel
#         drop_table_query = "DROP TABLE IF EXISTS coba;"
#         cursor.execute(drop_table_query)
#         print("Tabel 'coba' berhasil dihapus.")

# except Error as e:
#     print(f"Error: {e}")

# finally:
#     if 'connection' in locals() and connection.is_connected():
#         connection.close()
#         print("Koneksi ke database ditutup.")