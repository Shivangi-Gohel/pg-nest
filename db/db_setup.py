# db_setup.py
import sqlite3

def setup_database():
    connection = sqlite3.connect('db/pg_management.db')
    cursor = connection.cursor()

    ### -> This is only when you have to delete the tables 
    # cursor.execute('''
    #     DROP TABLE IF EXISTS rooms
    # ''') 
    # cursor.execute('''
    #     DROP TABLE IF EXISTS users
    # ''')
    # cursor.execute('''
    #     DROP TABLE IF EXISTS bookings
    # ''')
    
    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            password_hashed TEXT NOT NULL
        )
    ''')
    
   
    # Create Rooms table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_type TEXT NOT NULL,
            capacity INTEGER NOT NULL,
            price_per_day REAL NOT NULL,
            is_meal_included INTEGER NOT NULL,
            is_wifi INTEGER NOT NULL,
            is_usable INTEGER DEFAULT 1
        )
    ''')

    # Create Bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            room_id INTEGER NOT NULL,
            check_in_date TEXT NOT NULL,
            check_out_date TEXT,
            payment_status TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(room_id) REFERENCES rooms(id)
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    setup_database()
