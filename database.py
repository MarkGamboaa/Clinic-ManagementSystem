import sqlite3
import random

def connect_db():
    conn = sqlite3.connect('Systemdb.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # Create Doctors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # Create Appointments Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        doctor TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    );
    """)

    # Insert Predefined Doctor if Not Exists
    cursor.execute("SELECT COUNT(*) FROM doctors WHERE username = ?", ("dr_marlo",))
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO doctors (name, specialty, username, password) VALUES (?, ?, ?, ?)",
                       ("Dr. Marlo Veluz", "General Medicine", "dr_marlo", "marlo"))
        conn.commit()

    conn.close()

def insert_user(username, password):
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        if cursor.fetchone()[0] > 0:
            raise ValueError("Username already exists. Please choose a different one.")

        random_id = random.randint(10000, 99999)  # Generates a 5-digit random ID
        cursor.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (random_id, username, password))
        conn.commit()
        return random_id  # Return generated ID
    except sqlite3.Error:
        raise
    finally:
        conn.close()

def validate_user(username, password):
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        return bool(user)
    finally:
        conn.close()

def validate_doctor(username, password):
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE username = ? AND password = ?", (username, password))
        doctor = cursor.fetchone()
        return bool(doctor)
    finally:
        conn.close()

def get_doctors():
    conn = sqlite3.connect('Systemdb.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM doctors")
    doctors = [row[0] for row in cursor.fetchall()]
    conn.close()
    return doctors if doctors else ["No Doctors Available"]

def book_appointment(patient_name, doctor, date, time):
    try:
        conn = sqlite3.connect('Systemdb.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appointments (patient_name, doctor, date, time) VALUES (?, ?, ?, ?)", 
                       (patient_name, doctor, date, time))
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error:
        return False
