# models/booking_model.py
import sqlite3
from datetime import datetime

class BookingModel:
    def __init__(self):
        self.db_path = "db/pg_management.db"

    def create_booking(self, user_id, room_id, check_in_date):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO bookings (user_id, room_id, check_in_date, payment_status)
            VALUES (?, ?, ?, 'pending')
            ''',
            (user_id, room_id, check_in_date)
        )
        connection.commit()
        connection.close()

    def is_payment_clear(self, user_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT payment_status FROM bookings
            WHERE user_id = ? AND check_out_date IS NULL
            ''',
            (user_id,)
        )
        booking = cursor.fetchone()
        if not booking:
                return True
        connection.close()
        return booking and booking[0] == 'clear'

    def check_out(self, user_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''
            UPDATE bookings
            SET check_out_date = ?, payment_status = 'clear'
            WHERE user_id = ? AND check_out_date IS NULL
            ''',
            (datetime.now().strftime("%Y-%m-%d"), user_id)
        )
        connection.commit()
        connection.close()

    def calculate_current_bill(self, user_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''
            SELECT b.check_in_date, r.price_per_day
            FROM bookings b
            JOIN rooms r ON b.room_id = r.id
            WHERE b.user_id = ? AND b.check_out_date IS NULL
            ''',
            (user_id,)
        )
        booking = cursor.fetchone()
        connection.close()

        if booking:
            check_in_date = datetime.strptime(booking[0], "%Y-%m-%d")
            days_stayed = (datetime.now() - check_in_date).days + 1
            return days_stayed * booking[1]
        return 0

    def get_user_bookings(self, user_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
        bookings = cursor.fetchall()
        connection.close()
        return bookings

    def cancel_booking(self, booking_id):
        # Only allow cancellation on the day of check-in.
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT check_in_date FROM bookings WHERE id = ?", (booking_id,))
        check_in_date = cursor.fetchone()
        if not check_in_date:
            return False
        if check_in_date[0] == datetime.now().strftime("%Y-%m-%d"):
            cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
            connection.commit()
            connection.close()
            return True
        connection.close()
        return False
    
    def get_booking_details(self, booking_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,))
        booking = cursor.fetchone()
        connection.close()
        return booking

    def check_payment_status(self, booking_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT payment_status FROM bookings WHERE id = ?", (booking_id,))
        status = cursor.fetchone()
        connection.close()
        return status[0] if status else None

    def get_all_pending_bookings(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE check_out_date IS NULL")
        bookings = cursor.fetchall()
        connection.close()
        return bookings
    
    def get_all_bookings(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookings")
        bookings = cursor.fetchall()
        connection.close()
        return bookings
    
    def has_pending_bookings(self,user_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE user_id = ? AND payment_status = 'pending'", (user_id,))
        bookings = cursor.fetchall()
        connection.close()
        return len(bookings) > 0
        
    def get_available_rooms(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rooms WHERE id NOT IN (SELECT room_id FROM bookings WHERE check_out_date IS NULL)")
        rooms = cursor.fetchall()
        connection.close()
        return rooms
    
    def get_bookings_by_guest(self, user_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE user_id = ?", (user_id,))
        bookings = cursor.fetchall()
        connection.close()
        return bookings
    
    def is_room_in_use(self, room_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bookings WHERE room_id = ? AND check_out_date IS NULL", (room_id,))
        booking = cursor.fetchone()
        connection.close()
        return booking is not None