# models/room_model.py
import sqlite3
from models.booking_model import BookingModel

class RoomModel:
    def __init__(self):
        self.booking_model = BookingModel()
        self.db_path = "db/pg_management.db"

    def add_room(self, room_type, capacity, price_per_day, is_meal_included, is_wifi):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO rooms (room_type, capacity, price_per_day, is_meal_included, is_wifi)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (room_type, capacity, price_per_day, is_meal_included, is_wifi)
        )
        connection.commit()
        connection.close()

    def get_all_rooms(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        connection.close()
        return rooms

    def disband_room(self, room_id):
        try:
            # Check if the room is currently in use
            if self.booking_model.is_room_in_use(room_id):
                print("Cannot disband the room because it is currently in use.")
                return False
            
            # Proceed to disband the room if it is not in use
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("UPDATE rooms SET is_usable = 0 WHERE id = ? AND is_usable = 1", (room_id,))
            connection.commit()
            
            if cursor.rowcount > 0:
                print(f"Room {room_id} successfully disbanded.")
                return True
            else:
                print(f"Room {room_id} is already disbanded or does not exist.")
                return False
        except Exception as e:
            print(f"Error disbanding room: {e}")
            return False

    def get_revenue_by_room_type(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        query = "SELECT room_type, SUM(price_per_day) FROM bookings JOIN rooms ON bookings.room_id = rooms.id GROUP BY room_type"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return {row[0]: row[1] for row in result}

    def activate_room(self, room_id):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("UPDATE rooms SET is_usable = 1 WHERE id = ? AND is_usable = 0", (room_id,))
            connection.commit()
            return cursor.rowcount > 0  
        except Exception as e:
            print(f"Error activating room: {e}")
            return False

    def search_room_by_price_range(self, min_price, max_price):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rooms WHERE price_per_day BETWEEN ? AND ? AND is_usable = 1", (min_price, max_price))
        rooms = cursor.fetchall()
        connection.close()
        return rooms

    def get_rooms_by_capacity(self, capacity):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM rooms WHERE capacity >= ? AND is_usable = 1 AND id NOT IN (SELECT room_id FROM bookings WHERE check_out_date IS NULL)", 
            (capacity,)
        )
        rooms = cursor.fetchall()
        connection.close()
        return rooms
    
    def sort_by_price(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT * FROM rooms 
        WHERE is_usable = 1 
        AND id NOT IN (SELECT room_id FROM bookings WHERE check_out_date IS NULL) 
        ORDER BY price_per_day ASC
        """)
        sorted_rooms = cursor.fetchall()
        connection.close()
        return sorted_rooms
    
    def get_room_by_id(self, room_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
        room = cursor.fetchone()
        connection.close()
        return room