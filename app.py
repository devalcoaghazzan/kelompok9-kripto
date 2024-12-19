import streamlit as st

# Data contoh dari struktur database
users = [
    {"user_id": 1, "username": "alice", "password": "pass1234"},
    {"user_id": 2, "username": "bob", "password": "secure5678"}
]

notes = [
    {"note_id": 1, "user_id": 1, "notes": "Catatan pertama Alice."},
    {"note_id": 2, "user_id": 1, "notes": "Catatan kedua Alice."},
    {"note_id": 3, "user_id": 2, "notes": "Catatan pertama Bob."}
]

# Fungsi untuk memvalidasi login
def validate_user(username, password):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user
    return None

# Fungsi untuk mendapatkan catatan pengguna tertentu
def get_user_notes(user_id):
    return [note for note in notes if note['user_id'] == user_id]

# Simulasi ID catatan baru (untuk UI saja, tanpa database)
def get_next_note_id():
    return max(note['note_id'] for note in notes) + 1 if notes else 1

# State untuk login
def app():
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        # Halaman Login
        st.title("Login")
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
    else:
        # Halaman Catatan
        user = st.session_state.user
        st.title(f"Catatan {user['username']}")

        # Form untuk menambahkan catatan baru
        with st.form("add_note_form"):
            new_note = st.text_area("Tambahkan catatan baru")
            submitted = st.form_submit_button("Simpan")
            if submitted and new_note:
                notes.append({
                    "note_id": get_next_note_id(),
                    "user_id": user['user_id'],
                    "notes": new_note
                })
                st.success("Catatan berhasil disimpan.")

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
