import sqlite3
from cryptography.fernet import Fernet

# Initialize the database
def init_db():
    create_patients_table()
    create_doctors_table()
    create_personal_data_table()
    return connect_db()  # Ensure a connection is returned

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Get database connection
def get_db():
    conn = connect_db()
    return conn

# Encrypt patient data
def encrypt_data(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Decrypt patient data
def decrypt_data(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

# Connect to the database
def connect_db():
    conn = sqlite3.connect('patients.db')
    return conn

# Create patients table
def create_patients_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            code TEXT NOT NULL,
            medical_history TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Create doctors table
def create_doctors_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Create personal data table
def create_personal_data_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_data (
            id INTEGER PRIMARY KEY,
            patient_code TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Add a new patient
def add_patient(name, code, medical_history):
    key = generate_key()  # Use a secure method to retrieve the key
    encrypted_name = encrypt_data(name, key)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, code, medical_history) VALUES (?, ?, ?)
    ''', (encrypted_name, code, medical_history))
    conn.commit()
    conn.close()


# Function to add test data
def add_test_data():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Add test doctor
    cursor.execute('''
        INSERT INTO doctors (username, password) VALUES (?, ?)
    ''', ('test_doctor', 'test_password'))
    
    # Add test patient
    cursor.execute('''
        INSERT INTO personal_data (patient_code, full_name, phone) VALUES (?, ?, ?)
    ''', ('test_code', 'Test Patient', '1234567890'))
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()
add_test_data()
