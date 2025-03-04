import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from models.room_model import RoomModel
from models.booking_model import BookingModel
from utils.payment_utils import generate_receipt
from datetime import datetime


class GuestGUI:
    def __init__(self, guest_id , guest_name, login_screen):
        self.guest_id = guest_id
        self.guest_name = guest_name
        self.window = tk.Tk()
        self.login_screen_callback = login_screen
        self.window.title("Guest Dashboard | PG-Nest")
        self.window.geometry("900x700")
        self.window.configure(bg="#f0f8ff")

        self.room_model = RoomModel()
        self.booking_model = BookingModel()

        self.main_frame = tk.Frame(self.window, bg="#f0f8ff")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.dashboard_screen()

    def run(self):
        self.window.mainloop()

    def logout(self):
        self.window.destroy()
        self.login_screen_callback.deiconify()  # Show login screen

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def back_to_dashboard(self):
        self.dashboard_screen()

    def dashboard_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Guest Dashboard", font=("Arial", 24, "bold"), bg="#f0f8ff").pack(pady=10)

        active_booking = self.booking_model.has_pending_bookings(self.guest_id)
        
        if active_booking:
            tk.Button(self.main_frame, text="View Booking Details", command=lambda: self.view_booking_details(self.guest_id), font=("Arial", 14),
                      bg="#4CAF50", fg="white", width=30).pack(pady=10)

            tk.Button(self.main_frame, text="Pay and Check Out", command=self.pay_and_checkout, font=("Arial", 14),
                      bg="#FF9800", fg="white", width=30).pack(pady=10)

            tk.Button(self.main_frame, text="Calculate Total Amount", command=self.calculate_total_amount, font=("Arial", 14),
                      bg="#9C27B0", fg="white", width=30).pack(pady=10)

        else:
            # No active booking
            tk.Button(self.main_frame, text="Make a Booking", command=self.make_booking_screen, font=("Arial", 14),
                      bg="#4CAF50", fg="white", width=30).pack(pady=10)

            tk.Button(self.main_frame, text="Sort Rooms by Price", command=self.sort_rooms_by_price_screen, font=("Arial", 14),
                      bg="#FFC107", fg="white", width=30).pack(pady=10)

            tk.Button(self.main_frame, text="Check Available Rooms", command=self.check_available_rooms_screen, font=("Arial", 14),
                      bg="#673AB7", fg="white", width=30).pack(pady=10)
            
        tk.Button(self.main_frame, text="Logout", command=self.logout, font=("Arial", 14), bg="#FF5722", fg="white").pack(pady=10)

    def view_booking_details(self, guest_id):
        self.clear_frame()
        tk.Label(self.main_frame, text="Your Booking Details", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=10)

        # Retrieve all bookings for this guest
        bookings = self.booking_model.get_bookings_by_guest(guest_id)

        if bookings:
            columns = ("Booking ID", "User ID", "User Name", "Room ID", "Check-In Date", "Amount Paid", "Status")
            tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=10)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)

            for booking in bookings:
                tree.insert("", "end", values=booking)

            tree.pack(pady=20)
        else:
            tk.Label(self.main_frame, text="No booking records found.", font=("Arial", 16), bg="#f0f8ff").pack(pady=20)

        # Back button to return to the main dashboard
        tk.Button(self.main_frame, text="Back", command=self.back_to_dashboard, font=("Arial", 14), bg="#FF5722", fg="white").pack(pady=10)

   
    def pay_and_checkout(self):
        bill = self.booking_model.calculate_current_bill(self.guest_id)
        receipt_path = generate_receipt(self.guest_id, self.guest_name, bill)
        self.booking_model.check_out(self.guest_id)
        messagebox.showinfo("Payment Successful", f"Your bill of {bill} INR has been paid. You are now checked out.\nReceipt saved at: {receipt_path}")
        self.dashboard_screen()

    def calculate_total_amount(self):
        bill = self.booking_model.calculate_current_bill(self.guest_id)
        messagebox.showinfo("Total Amount", f"Your total amount till now is: {bill} INR")
        self.dashboard_screen()

    def make_booking_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Make a Booking", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=10)

        tk.Label(self.main_frame, text="How many members?", font=("Arial", 14), bg="#f0f8ff").pack(pady=10)
        members_entry = tk.Entry(self.main_frame, font=("Arial", 14))
        members_entry.pack(pady=10)

        tk.Button(self.main_frame, text="Search Rooms", command=lambda: self.search_rooms(int(members_entry.get())), font=("Arial", 14),
                  bg="#4CAF50", fg="white").pack(pady=10)


    def search_rooms(self, members):
        self.clear_frame()
        tk.Label(self.main_frame, text=f"Rooms for {members} or More Members", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=10)

        rooms = self.room_model.get_rooms_by_capacity(members)
        self.display_rooms(rooms)

    def sort_rooms_by_price_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Rooms Sorted by Price", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=10)

        sorted_rooms = self.room_model.sort_by_price()

        if sorted_rooms:
            self.display_rooms(sorted_rooms)
        else:
            tk.Label(self.main_frame, text="No rooms available.", font=("Arial", 16), bg="#f0f8ff").pack(pady=20)
            tk.Button(self.main_frame, text="Back", command=self.back_to_dashboard, font=("Arial", 14), bg="#FF5722", fg="white").pack(pady=10)

    def check_available_rooms_screen(self):
        self.clear_frame()
        tk.Label(self.main_frame, text="Available Rooms", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=10)

        available_rooms = self.booking_model.get_available_rooms()  # Retrieve all available rooms

        if available_rooms:
            self.display_rooms(available_rooms)  # Use the display_rooms function to list available rooms
        else:
            tk.Label(self.main_frame, text="No rooms are available at the moment.", font=("Arial", 16), bg="#f0f8ff").pack(pady=20)
            tk.Button(self.main_frame, text="Back", command=self.back_to_dashboard, font=("Arial", 14), bg="#FF5722", fg="white").pack(pady=10)
   
    def book_room_dialog(self, room):
        dialog = tk.Toplevel(self.window)
        dialog.title("Book Room")
        dialog.geometry("400x300")
        dialog.configure(bg="#f0f8ff")

        tk.Label(dialog, text=f"Book Room {room[0]} ({room[1]} Type)", font=("Arial", 16, "bold"), bg="#f0f8ff").pack(pady=10)
        tk.Label(dialog, text="Enter Check-In Date (YYYY-MM-DD):", font=("Arial", 14), bg="#f0f8ff").pack(pady=10)

        checkin_date_entry = tk.Entry(dialog, font=("Arial", 14))
        checkin_date_entry.pack(pady=10)

        def confirm_booking():
            check_in_date = checkin_date_entry.get()
            try:
                date_obj = datetime.strptime(check_in_date, "%Y-%m-%d")
                
                if date_obj.date() > datetime.now().date():
                    raise ValueError("Enter valid date ")
                
                self.booking_model.create_booking(self.guest_id, self.guest_name, room[0], check_in_date)
                messagebox.showinfo("Booking Successful", f"Room {room[0]} booked successfully!")
                dialog.destroy()
                self.dashboard_screen()

            except ValueError as e:
                messagebox.showerror("Invalid Date", f"{e}")

            except Exception as e:
                messagebox.showerror("Booking Failed", f"An error occurred: {e}")

        tk.Button(dialog, text="Confirm Booking", command=confirm_booking, font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=20)
        tk.Button(dialog, text="Cancel", command=dialog.destroy, font=("Arial", 14), bg="#FF5722", fg="white").pack(pady=10)

    def display_rooms(self, rooms):
        self.clear_frame()
        tk.Label(self.main_frame, text="Available Rooms", font=("Arial", 20, "bold"), bg="#f0f8ff").pack(pady=10)

        if not rooms:
            tk.Label(self.main_frame, text="No rooms available.", font=("Arial", 16), fg="red", bg="#f0f8ff").pack(pady=20)
        else:
            columns = ("Room ID", "Type", "Capacity", "Price", "Meal Included", "Wi-Fi")
            tree = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=15)

            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=120)

            for room in rooms:
                meal_included = "Yes" if room[4] == 1 else "No"
                wifi = "Yes" if room[5] == 1 else "No"
                tree.insert("", "end", values=(room[0], room[1], room[2], room[3], meal_included, wifi))

            tree.pack(pady=20)

            def book_selected_room():
                selected_item = tree.focus()
                if selected_item:
                    room = tree.item(selected_item, "values")
                    self.book_room_dialog(room)
                else:
                    messagebox.showwarning("No Room Selected", "Please select a room before booking.")

            tk.Button(self.main_frame, text="Book Now", command=book_selected_room, font=("Arial", 14), bg="#4CAF50", fg="white").pack(pady=10)

        tk.Button(self.main_frame, text="Back", command=self.back_to_dashboard, font=("Arial", 14), bg="#FF5722", fg="white").pack(pady=10)
