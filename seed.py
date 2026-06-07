import sqlite3

# Connect to the database
conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

# Insert test patient
cursor.execute('''
    INSERT INTO personal_data (patient_code, full_name, phone, birth_date, created_at)
    VALUES (?, ?, ?, ?, ?)
''', ('test_code', 'Test Patient', '1234567890', '2000-01-01', '2026-06-07'))

# Insert test doctor
cursor.execute('''
    INSERT INTO doctors (username, password)
    VALUES (?, ?)
''', ('test_doctor', 'test_password'))

# Commit changes and close the connection
conn.commit()
conn.close()