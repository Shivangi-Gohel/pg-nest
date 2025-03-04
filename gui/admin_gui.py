import tkinter as tk
from tkinter import ttk, messagebox
from models.room_model import RoomModel
from models.user_model import UserModel
from models.booking_model import BookingModel
import matplotlib.pyplot as plt
from matplotlib import gridspec
import datetime
from collections import defaultdict

class AdminGUI:
    def __init__(self, login_screen):
        self.login_screen = login_screen
        self.window = tk.Tk()
        self.window.title("Admin Dashboard  |  PG-Nest")
        self.window.geometry("700x500")
        self.window.configure(bg="#f0f0f0")

        self.room_model = RoomModel()
        self.user_model = UserModel()
        self.booking_model = BookingModel()

    def run(self):
        self.dashboard_screen()
        self.window.mainloop()

    def dashboard_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        header = tk.Frame(self.window, bg="#4CAF50", height=80)
        header.pack(fill="x")
        tk.Label(header, text="Admin Dashboard", font=("Arial", 24, "bold"), bg="#4CAF50", fg="white").pack(pady=20)

        main_frame = tk.Frame(self.window, bg="#f0f0f0")
        main_frame.pack(expand=True)

        button_frame = tk.Frame(main_frame, bg="#ffffff", relief=tk.GROOVE, bd=2, padx=40, pady=20)
        button_frame.pack(pady=40)
        
        buttons = [
            ("List All Guests", self.list_all_guests),
            ("List All Rooms", self.list_all_rooms),
            ("Add New Room", self.add_room_screen),
            ("Pending Bookings", self.list_pending_bookings),
            ("All Bookings", self.list_all_bookings),
            ("Generate Report", self.generate_report),
            ("Activate Room", self.activate_room_screen),
            ("Disband Room", self.disband_room_screen),
        ]

        for i, (text, command) in enumerate(buttons):
            row, col = divmod(i, 2)  # Divide buttons into 2 columns
            tk.Button(
                button_frame, 
                text=text, 
                command=command, 
                font=("Arial", 14), 
                bg="#4CAF50", 
                fg="white", 
                width=25, 
                height=2
            ).grid(row=row, column=col, padx=10, pady=10)

        tk.Button(
            main_frame, 
            text="Logout", 
            command=self.logout, 
            font=("Arial", 14), 
            bg="#FF5722", 
            fg="white", 
            width=30, 
            height=2
        ).pack(pady=20)

        
    def logout(self):
        self.window.destroy()
        self.login_screen.deiconify() # show login screen
   
    def list_all_guests(self):
        guests = self.user_model.get_all_guests()
        guest_window = tk.Toplevel(self.window)
        guest_window.title("All Guests")
        guest_window.geometry("800x500")

        frame = tk.Frame(guest_window)
        frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=("ID", "Name", "Email", "Phone", "Address"), show='headings')
        
        # Set column headings and auto-size columns
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        # Add scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        tree.pack(fill=tk.BOTH, expand=True)

        for guest in guests:
            tree.insert('', tk.END, values=guest)

    def list_all_rooms(self):
        rooms = self.room_model.get_all_rooms()
        room_window = tk.Toplevel(self.window)
        room_window.title("All Rooms")
        room_window.geometry("800x500")

        frame = tk.Frame(room_window)
        frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=("ID", "Type", "Capacity", "Price", "Meal", "Wi-Fi", "Usable"), show='headings')
        
        # Set column headings and auto-size columns
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Add scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        tree.pack(fill=tk.BOTH, expand=True)

        # Insert room data into the table
        for room in rooms:
            room_id, room_type, capacity, price, meal, wifi, usable = room
            
            # Convert 0/1 to "No"/"Yes"
            meal_status = "Yes" if meal == 1 else "No"
            wifi_status = "Yes" if wifi == 1 else "No"
            usable_status = "Yes" if usable == 1 else "No"
            
            tree.insert('', tk.END, values=(room_id, room_type, capacity, price, meal_status, wifi_status, usable_status))
 
    def add_room_screen(self):
        room_window = tk.Toplevel(self.window)
        room_window.title("Add New Room")
        room_window.geometry("400x400")
        room_window.configure(bg="#f0f0f0")

        tk.Label(room_window, text="Add New Room", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=10)

        frame = tk.Frame(room_window, bg="#ffffff", padx=20, pady=20, relief=tk.GROOVE, bd=2)
        frame.pack(pady=10)

        tk.Label(frame, text="Room Type:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        room_type_dropdown = ttk.Combobox(frame, font=("Arial", 12), state="readonly" , values=["AC", "Non-AC", "Deluxe", "Local"])
        room_type_dropdown.set("AC")
        room_type_dropdown.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Capacity:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        capacity_entry = tk.Entry(frame, font=("Arial", 12))
        capacity_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Price per Day:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        price_entry = tk.Entry(frame, font=("Arial", 12))
        price_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Meal Included:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
        meal_dropdown = ttk.Combobox(frame, font=("Arial", 12), state="readonly" ,values=["Yes", "No"])
        meal_dropdown.set("No")
        meal_dropdown.grid(row=3, column=1, pady=5)

        # Wi-Fi Dropdown
        tk.Label(frame, text="Wi-Fi:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=5)
        wifi_dropdown = ttk.Combobox(frame, font=("Arial", 12), state="readonly", values=["Yes", "No"])
        wifi_dropdown.set("Yes")
        wifi_dropdown.grid(row=4, column=1, pady=5)

        def add_room():
            room_type = room_type_dropdown.get()
            capacity = capacity_entry.get().strip()
            price = price_entry.get().strip()
            meal = meal_dropdown.get()
            wifi = wifi_dropdown.get()

            if not (room_type and capacity and price and meal and wifi):
                messagebox.showerror("Input Error", "All fields must be filled.")
                return
            if not capacity.isdigit():
                messagebox.showerror("Input Error", "Capacity must be a valid integer.")
                return
            if not price.replace('.', '', 1).isdigit():
                messagebox.showerror("Input Error", "Price must be a valid number.")
                return

            # Convert Yes/No to 1/0
            meal_value = 1 if meal == "Yes" else 0
            wifi_value = 1 if wifi == "Yes" else 0

            try:
                capacity = int(capacity)
                price = float(price)
                self.room_model.add_room(room_type, capacity, price, meal_value, wifi_value)
                messagebox.showinfo("Success", "Room added successfully!")
                room_window.destroy()
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

        tk.Button(room_window, text="Add Room", command=add_room, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

    def list_pending_bookings(self):
        bookings = self.booking_model.get_all_pending_bookings()
        self.display_pending_data(bookings, "Pending Bookings")

    def list_all_bookings(self):
        bookings = self.booking_model.get_all_bookings()
        self.display_booking_data(bookings, "All Bookings")

    def display_pending_data(self, bookings, title):
        if not bookings:
            messagebox.showinfo("No Data", f"No {title.lower()} available.")
            return

        booking_window = tk.Toplevel(self.window)
        booking_window.title(title)
        booking_window.geometry("800x500")

        frame = tk.Frame(booking_window)
        frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=("Booking ID", "Name", "Room ID", "Check-In Date"), show='headings')

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        tree.pack(fill=tk.BOTH, expand=True)

        for booking in bookings:
            tree.insert('', tk.END, values=booking)

    def display_booking_data(self, bookings, title):
        if not bookings:
            messagebox.showinfo("No Data", f"No {title.lower()} available.")
            return

        booking_window = tk.Toplevel(self.window)
        booking_window.title(title)
        booking_window.geometry("800x500")

        frame = tk.Frame(booking_window)
        frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=("Booking ID", "User ID", "Name", "Room ID", "Check-In Date", "Check-out-Date", "Payment Status"), show='headings')

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        tree.pack(fill=tk.BOTH, expand=True)

        for booking in bookings:
            tree.insert('', tk.END, values=booking)
  
    def activate_room_screen(self):
        activate_window = tk.Toplevel(self.window)
        activate_window.title("Activate Room")
        activate_window.geometry("300x200")
        activate_window.configure(bg="#f0f0f0")

        tk.Label(activate_window, text="Enter Room Number to Activate", font=("Arial", 14), bg="#f0f0f0").pack(pady=20)
        room_number_entry = tk.Entry(activate_window, font=("Arial", 12))
        room_number_entry.pack(pady=10)

        def activate_room():
            room_number = room_number_entry.get().strip()
            if not room_number.isdigit():
                messagebox.showerror("Input Error", "Please enter a valid room number.")
                return

            success = self.room_model.activate_room(int(room_number))
            if success:
                messagebox.showinfo("Success", f"Room {room_number} has been activated.")
                activate_window.destroy()
            else:
                messagebox.showerror("Error", f"Room {room_number} not found or already active.")

        tk.Button(activate_window, text="Activate Room", command=activate_room, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=20)

    def disband_room_screen(self):
        disband_window = tk.Toplevel(self.window)
        disband_window.title("Disband Room")
        disband_window.geometry("300x200")
        disband_window.configure(bg="#f0f0f0")

        tk.Label(disband_window, text="Enter Room Number to Disband", font=("Arial", 14), bg="#f0f0f0").pack(pady=20)
        room_number_entry = tk.Entry(disband_window, font=("Arial", 12))
        room_number_entry.pack(pady=10)

        def disband_room():
            room_number = room_number_entry.get().strip()
            if not room_number.isdigit():
                messagebox.showerror("Input Error", "Please enter a valid room number.")
                return

            success = self.room_model.disband_room(int(room_number))
            if success:
                messagebox.showinfo("Success", f"Room {room_number} has been disbanded.")
                disband_window.destroy()
            else:
                messagebox.showerror("Error", f"Room {room_number} not found or already disbanded or in use.")

        tk.Button(disband_window, text="Disband Room", command=disband_room, font=("Arial", 12), bg="#FF5722", fg="white").pack(pady=20)
        
    def generate_report(self):
        bookings = self.booking_model.get_all_bookings()
        room_usage = defaultdict(int)
        revenue_by_room_type = defaultdict(float)
        payment_status = {"clear": 0, "pending": 0}
        bookings_over_time = defaultdict(int)

        for booking in bookings:
            _, user_id, user_name, room_id, check_in_date, check_out_date, status = booking
            room = self.room_model.get_room_by_id(room_id)
            
            # 1. Room Usage by Room Type
            room_type = room[1] 
            room_usage[room_type] += 1

            # 2. Revenue by Room Type
            price_per_day = room[3]
            check_in_date = datetime.datetime.strptime(check_in_date, "%Y-%m-%d")
            check_out_date = datetime.datetime.strptime(check_out_date, "%Y-%m-%d") if check_out_date else datetime.datetime.now()
            days_stayed = (check_out_date - check_in_date).days
            revenue_by_room_type[room_type] += price_per_day * max(days_stayed, 1)

            # 3. Total Bookings Over Time
            bookings_over_time[check_in_date] += 1

            # 4. Payment Status Distribution
            if status in payment_status:
                payment_status[status] += 1
        
        print(room_usage)
        print(revenue_by_room_type)
        print(payment_status)
        print(bookings_over_time)

        # Create a figure with multiple subplots
        fig = plt.figure(figsize=(12, 8))
        spec = gridspec.GridSpec(2, 2, figure=fig)

        # Plot 1: Total Bookings Over Time (Line Chart)
        ax1 = fig.add_subplot(spec[0, 0])
        sorted_dates = sorted(bookings_over_time.keys())
        ax1.plot(sorted_dates, [bookings_over_time[date] for date in sorted_dates], marker='o', linestyle='-', color='b')
        ax1.set_title("Total Bookings Over Time")
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Number of Bookings")
        ax1.grid(True)

        # Plot 2: Room Usage by Room Type (Bar Chart)
        ax2 = fig.add_subplot(spec[0, 1])
        ax2.bar(room_usage.keys(), room_usage.values(), color=['#4CAF50', '#2196F3', '#FF5722', '#FFC107'])
        ax2.set_title("Room Usage by Room Type")
        ax2.set_xlabel("Room Type")
        ax2.set_ylabel("Number of Bookings")

        # Plot 3: Revenue by Room Type (Bar Chart)
        ax3 = fig.add_subplot(spec[1, 0])
        ax3.bar(revenue_by_room_type.keys(), revenue_by_room_type.values(), color=['#8E44AD', '#3498DB', '#E74C3C', '#1ABC9C'])
        ax3.set_title("Revenue by Room Type")
        ax3.set_xlabel("Room Type")
        ax3.set_ylabel("Revenue (INR)")

        # Plot 4: Payment Status Distribution (Pie Chart)
        ax4 = fig.add_subplot(spec[1, 1])
        ax4.pie(payment_status.values(), labels=payment_status.keys(), autopct='%1.1f%%', startangle=140, colors=['#2ECC71', '#F1C40F', '#E74C3C'])
        ax4.set_title("Payment Status Distribution")

        # Adjust layout and show the plot
        plt.tight_layout()
        plt.show()
        