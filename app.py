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
            port=3307  #SESUAIN PORTNYA
        )
        return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Fungsi untuk enkripsi Columnar Transposition Cipher
def columnar_encrypt(plaintext, key):
    key_order = sorted(range(len(key)), key=lambda x: key[x])
    col_count = len(key)
    row_count = (len(plaintext) + col_count - 1) // col_count
    grid = [plaintext[i * col_count:(i + 1) * col_count].ljust(col_count, '_') for i in range(row_count)]
    encrypted_text = ''.join(''.join(row[idx] for row in grid) for idx in key_order)
    return encrypted_text

# Fungsi untuk dekripsi Columnar Transposition Cipher
def columnar_decrypt(ciphertext, key):
    key_order = sorted(range(len(key)), key=lambda x: key[x])
    col_count = len(key)
    row_count = len(ciphertext) // col_count
    grid = [''] * col_count
    index = 0
    for idx in key_order:
        grid[idx] = ciphertext[index:index + row_count]
        index += row_count
    decrypted_text = ''.join(''.join(row) for row in zip(*grid)).rstrip('_')
    return decrypted_text

# Fungsi untuk enkripsi Vigenere Cipher
def vigenere_encrypt(plaintext, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    encrypted_text = ""
    key_index = 0

    for char in plaintext:
        if char.upper() in alphabet:
            p_index = alphabet.index(char.upper())
            k_index = alphabet.index(key[key_index % len(key)])
            c_index = (p_index + k_index) % len(alphabet)
            encrypted_char = alphabet[c_index]
            encrypted_text += encrypted_char if char.isupper() else encrypted_char.lower()
            key_index += 1
        else:
            encrypted_text += char

    return encrypted_text

# Fungsi untuk dekripsi Vigenere Cipher
def vigenere_decrypt(ciphertext, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    decrypted_text = ""
    key_index = 0

    for char in ciphertext:
        if char.upper() in alphabet:
            c_index = alphabet.index(char.upper())
            k_index = alphabet.index(key[key_index % len(key)])
            p_index = (c_index - k_index + len(alphabet)) % len(alphabet)
            decrypted_char = alphabet[p_index]
            decrypted_text += decrypted_char if char.isupper() else decrypted_char.lower()
            key_index += 1
        else:
            decrypted_text += char

    return decrypted_text

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

            # Enkripsi password dengan Columnar Transposition Cipher
            key = "secretkey"  # Gunakan kunci tetap untuk Columnar
            encrypted_password = columnar_encrypt(password, key)

            # Insert pengguna baru ke tabel user
            cursor.execute(
                "INSERT INTO user (username, password) VALUES (%s, %s)",
                (username, encrypted_password)
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
            # Ambil data pengguna berdasarkan username
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                # Dekripsi password dengan Columnar Transposition Cipher
                key = "secretkey"
                decrypted_password = columnar_decrypt(user['password'], key)
                if decrypted_password == password:
                    return user
            return None
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
def add_note(user_id, note_title, note_text, key):
    encrypted_note = vigenere_encrypt(note_text, key)
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO note (user_id, title, notes) VALUES (%s, %s, %s)",
                (user_id, note_title, encrypted_note)
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

        # Tab untuk menambah dan membaca catatan
        tab1, tab2 = st.tabs(["Tambah Catatan", "Baca Catatan"])

        with tab1:
            # Form untuk menambahkan catatan baru
            with st.form("add_note_form"):
                note_title = st.text_input("Judul Catatan")
                new_note = st.text_area("Tambahkan catatan baru")
                cipher_key = st.text_input("Masukkan kunci untuk enkripsi Vigenere")
                submitted = st.form_submit_button("Simpan")
                if submitted and new_note and cipher_key:
                    add_note(user['user_id'], note_title, new_note, cipher_key)

        with tab2:
            # Menampilkan catatan yang sudah disimpan
            user_notes = get_user_notes(user['user_id'])
            if user_notes:
                st.subheader("Daftar Catatan")
                for idx, note in enumerate(user_notes, start=1):
                    st.write(f"### {note['title']}")
                    cipher_key = st.text_input(f"Masukkan kunci untuk mendekripsi catatan {idx}", key=f"key_{idx}")
                    if cipher_key:
                        decrypted_note = vigenere_decrypt(note['notes'], cipher_key)
                        st.text_area(f"Catatan {idx}", decrypted_note, height=100, disabled=True)
                    st.write("---")
            else:
                st.info("Belum ada catatan.")

        # Tombol Logout
        if st.button("Logout"):
            st.session_state.user = None
            st.experimental_rerun()

# Menjalankan aplikasi
app()
