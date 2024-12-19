import streamlit as st
import mysql.connector
from mysql.connector import Error

# Fungsi untuk koneksi ke database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_notes',  
            port=3308  #SESUAIN PORTNYA
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Fungsi untuk registrasi pengguna baru
def register_user(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Periksa apakah username sudah ada
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            if cursor.fetchone():
                st.error("Username sudah digunakan.")
                return False

            # Insert pengguna baru ke tabel user
            cursor.execute(
                "INSERT INTO user (username, password) VALUES (%s, %s)",
                (username, password)
            )
            connection.commit()
            st.success("Registrasi berhasil. Silakan login.")
            return True
        except Error as e:
            st.error(f"Error during registration: {e}")
        finally:
            cursor.close()
            connection.close()
    return False

# Fungsi untuk validasi login
def validate_user(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            # Periksa username dan password di database
            cursor.execute(
                "SELECT * FROM user WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cursor.fetchone()
            return user
        except Error as e:
            st.error(f"Error during login: {e}")
        finally:
            cursor.close()
            connection.close()
    return None

# Fungsi untuk mendapatkan catatan pengguna tertentu
def get_user_notes(user_id):
    connection = create_connection()
    notes = []
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM note WHERE user_id = %s", (user_id,))
            notes = cursor.fetchall()
        except Error as e:
            st.error(f"Error fetching notes: {e}")
        finally:
            cursor.close()
            connection.close()
    return notes

# Fungsi untuk menambahkan catatan baru
def add_note(user_id, note_text):
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO note (user_id, notes) VALUES (%s, %s)",
                (user_id, note_text)
            )
            connection.commit()
            st.success("Catatan berhasil disimpan.")
        except Error as e:
            st.error(f"Error adding note: {e}")
        finally:
            cursor.close()
            connection.close()

# Aplikasi utama
def app():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        # Pilihan Login atau Registrasi
        st.title("Login atau Register")
        option = st.radio("Pilih opsi", ["Login", "Register"])

        if option == "Login":
            # Halaman Login
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                user = validate_user(username, password)
                if user:
                    st.session_state.user = user
                    st.success(f"Selamat datang, {user['username']}!")
                    st.experimental_rerun()
                else:
                    st.error("Username atau password salah.")

        elif option == "Register":
            # Halaman Register
            username = st.text_input("Username (baru)")
            password = st.text_input("Password (baru)", type="password")
            if st.button("Register"):
                if username and password:
                    register_user(username, password)
                else:
                    st.error("Harap isi username dan password.")

    else:
        # Halaman Catatan
        user = st.session_state.user
        st.title(f"Catatan {user['username']}")

        # Form untuk menambahkan catatan baru
        with st.form("add_note_form"):
            new_note = st.text_area("Tambahkan catatan baru")
            submitted = st.form_submit_button("Simpan")
            if submitted and new_note:
                add_note(user['user_id'], new_note)

        # Menampilkan catatan yang sudah disimpan
        user_notes = get_user_notes(user['user_id'])
        if user_notes:
            st.subheader("Daftar Catatan")
            for idx, note in enumerate(user_notes, start=1):
                st.write(f"### Note {idx}")
                st.write(note['notes'])
                st.write("---")
        else:
            st.info("Belum ada catatan.")

        # Tombol Logout
        if st.button("Logout"):
            st.session_state.user = None
            st.experimental_rerun()

# Menjalankan aplikasi
app()
