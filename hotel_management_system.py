import tkinter as tk
from tkinter import ttk, messagebox
import ctypes  # For getting screen size

# Global variable to store data
rooms = []
reservations = []
checkouts = []

class HotelManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")

        # Calculate window size as 60% of screen size
        screen_width, screen_height = self.get_screen_size()
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.6)
        window_position_x = (screen_width - window_width) // 2
        window_position_y = (screen_height - window_height) // 2

        # Set window size and position
        self.root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

        # Function to load and resize images
        self.image_dict = {}
        self.load_images()

        # Welcome message
        self.welcome_label = ttk.Label(self.root, text="Welcome to the Hotel Management System", font=('Helvetica', 16, 'bold'))
        self.welcome_label.grid(row=0, column=0, columnspan=len(self.options)+1, padx=10, pady=10)

        # Options frame
        self.options_frame = ttk.Frame(self.root)
        self.options_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

        # Canvas for rooms frame
        self.canvas = tk.Canvas(self.root)
        self.canvas.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        # Create a frame inside the canvas for the rooms
        self.rooms_frame = ttk.Frame(self.canvas)
        self.rooms_frame.grid(row=0, column=0, sticky='nsew')

        # Add a scrollbar for the canvas
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=2, column=5, sticky='ns')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Configure canvas scrolling
        self.canvas.create_window((0, 0), window=self.rooms_frame, anchor='nw')
        
        # Bind canvas resizing to the scrollbar
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Reservation frame
        self.reservation_frame = ttk.Frame(self.root)
        self.create_reservation_form()
        
        # Contact frame
        self.contacts_frame = ttk.Frame(self.root)
        
        # Reservation Status frame
        self.status_frame = ttk.Frame(self.root)
        # Initialize rooms and options
        self.initialize_rooms()
        self.initialize_options()

    def create_status_frame(self):
        # Create frame for hotel status display
        self.status_frame = ttk.Frame(self.root, borderwidth=2, relief=tk.SUNKEN)
        self.status_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        # Hotel Status Labels
        ttk.Label(self.status_frame, text="Hotel Status", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.total_guests_label = ttk.Label(self.status_frame, text="Total Guests (Reservations): -")
        self.total_guests_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.occupied_rooms_label = ttk.Label(self.status_frame, text="Occupied Rooms: -")
        self.occupied_rooms_label.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        self.available_rooms_label = ttk.Label(self.status_frame, text="Available Rooms: -")
        self.available_rooms_label.grid(row=3, column=0, padx=10, pady=5, sticky='w')

    def initialize_rooms(self):
        # Display rooms frame initially
        self.hide_frames()
        #self.show_rooms_list()

    def initialize_options(self):
        # Create buttons for each option
        for idx, (option, image_path, color, command) in enumerate(self.options, start=1):
            try:
                button = ttk.Button(self.options_frame, text=option, image=self.image_dict[option], compound=tk.TOP,
                                    style=f'TButton{idx}.Custom.TButton', command=command)
                button.grid(row=0, column=idx, padx=5, pady=10)
            except tk.TclError as e:
                print(f"Error loading image {image_path}: {e}")

    def load_images(self):
        # Function to load and resize images
        image_path = 'C:/Users/MASTER/Downloads/hotelmanagement/images/'
        self.options = [
            ("Hotel Status", image_path + "hotel_status.png", "#ffcc99", self.hotel_status),
            ("Rooms", image_path + "rooms.png", "#99ff99", self.show_rooms_list),
            ("Reserve", image_path + "reserve.png", "#99ccff", self.show_reservation_form),
            ("Checkout", image_path + "payment_info.png", "#ff99cc", self.payment_info),
            ("Contacts", image_path + "contacts.png", "#ffff99", self.contacts),
            ("Exit", image_path + "exit.png", "#cccccc", self.exit_app)
        ]
        for option, image_file, color, command in self.options:
            image = tk.PhotoImage(file=image_file)
            image = image.subsample(5, 5)  # Resize image
            self.image_dict[option] = image

    def hotel_status(self):
    
        self.hide_frames()
        # Reservation Status frame
        self.create_status_frame()
        
        # Count total guests
        total_guests = len(reservations)
        
        # Count occupied rooms
        occupied_rooms = len(checkouts)
        
        # Count available rooms
        available_rooms = len(rooms) - occupied_rooms

        # Update labels in status frame
        self.total_guests_label.config(text=f"Total Guests (Reservations): {total_guests}")
        self.occupied_rooms_label.config(text=f"Occupied Rooms: {occupied_rooms}")
        self.available_rooms_label.config(text=f"Available Rooms: {available_rooms}")


    def show_rooms_list(self):
        self.hide_frames()
        self.canvas.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.show_rooms()


    def show_reservation_form(self):
        self.hide_frames()
        self.reservation_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')
        self.create_reservation_form()

    def payment_info(self):
    
        self.hide_frames()
        self.reservation_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')
        #self.create_reservation_form()
        
        for widget in self.reservation_frame.winfo_children():
            widget.destroy()
        self.hide_frames()
        self.reservation_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        ttk.Label(self.reservation_frame, text="Select Room:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        available_rooms = [room["room_number"] for room in rooms]
        self.selected_room_var = tk.StringVar(self.reservation_frame)
        self.selected_room_dropdown = ttk.Combobox(self.reservation_frame, textvariable=self.selected_room_var, values=available_rooms, state="readonly")
        self.selected_room_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        self.selected_room_dropdown.bind("<<ComboboxSelected>>", self.display_payment_options)

        self.payment_label = ttk.Label(self.reservation_frame, text="Amount to be Paid: ")
        self.payment_label.grid(row=1, column=0, padx=10, pady=5, sticky='e')

        self.payment_detail_label = ttk.Label(self.reservation_frame, text="")
        self.payment_detail_label.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.payment_method_label = ttk.Label(self.reservation_frame, text="Payment Method: ")
        self.payment_method_label.grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.payment_method_var = tk.StringVar(self.reservation_frame)
        self.payment_method_dropdown = ttk.Combobox(self.reservation_frame, textvariable=self.payment_method_var, values=["Cash", "Card"], state="readonly")
        self.payment_method_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        self.payment_method_dropdown.bind("<<ComboboxSelected>>", self.display_payment_details)

        self.card_frame = ttk.Frame(self.reservation_frame)
        self.cash_frame = ttk.Frame(self.reservation_frame)

        self.card_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        self.cash_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.card_label = ttk.Label(self.card_frame, text="Enter Credit Card Details:")
        self.card_label.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.card_entry = ttk.Entry(self.card_frame)
        self.card_entry.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.cash_label1 = ttk.Label(self.cash_frame, text="Enter User Name:")
        self.cash_label1.grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.cash_entry1 = ttk.Entry(self.cash_frame)
        self.cash_entry1.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.cash_label2 = ttk.Label(self.cash_frame, text="Enter Contact Number:")
        self.cash_label2.grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.cash_entry2 = ttk.Entry(self.cash_frame)
        self.cash_entry2.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.card_frame.grid_remove()
        self.cash_frame.grid_remove()
        
        self.checkout_button = ttk.Button(self.reservation_frame, text="Checkout", command=self.checkout)
        self.checkout_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        

    def display_payment_options(self, event):
        room_number = int(self.selected_room_var.get())
        selected_room = next((room for room in rooms if room["room_number"] == room_number), None)
    
        if selected_room:
            price = selected_room['price'].get()  # Retrieve the value from the StringVar
            self.payment_detail_label.config(text=f"${price} for Room {selected_room['room_number']}")
        else:
            self.payment_detail_label.config(text="")

    def display_payment_details(self, event):
        payment_method = self.payment_method_var.get()
        if payment_method == "Card":
            self.card_frame.grid()
            self.cash_frame.grid_remove()
        elif payment_method == "Cash":
            self.card_frame.grid_remove()
            self.cash_frame.grid()

    def checkout(self):
        room_number = int(self.selected_room_var.get())
        guest_name = self.cash_entry1.get()
        contact_number = self.cash_entry2.get()
        card = self.card_entry.get()

        checkout_details = {
            "room_number": room_number,
            "guest_name": guest_name,
            "contact_number": contact_number,
            "card": card
        }
        checkouts.append(checkout_details)
        messagebox.showinfo("Checkout", f"Checkout successful for Room {room_number}")
        self.clear_payment_info()

    def clear_payment_info(self):
        self.selected_room_var.set("")
    
        # Clear payment details labels
        self.payment_detail_label.config(text="")
        
        # Reset payment method dropdown
        self.payment_method_var.set("")
        
        # Clear credit card entry
        self.card_entry.delete(0, tk.END)
        
        # Clear cash entry fields
        self.cash_entry1.delete(0, tk.END)
        self.cash_entry2.delete(0, tk.END)

        # Reset StringVars
        self.user_name_var.set("")
        self.contact_number_var.set("")

        # Reset Combobox
        self.payment_method_combobox.current(-1)

        # Hide payment_info frame
        self.payment_info_frame.grid_forget()

    def contacts(self):
        self.hide_frames()

        # Create contacts frame
        self.contacts_frame = ttk.Frame(self.root)
        self.contacts_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='nsew')

        # Create table headers with borders
        headers = ["Guest Name", "Contact Info", "Card Details", "Stayed in Room"]
        for col, header in enumerate(headers):
            ttk.Label(self.contacts_frame, text=header, font=('Helvetica', 12, 'bold'), relief=tk.RIDGE).grid(row=0, column=col, padx=10, pady=5, sticky='nsew')

        # Display checkout details if available, otherwise show "No Data"
        if not checkouts:
            ttk.Label(self.contacts_frame, text="No Data", font=('Helvetica', 12)).grid(row=1, column=0, columnspan=4, padx=10, pady=5)
        else:
            for idx, checkout in enumerate(checkouts, start=1):
                ttk.Label(self.contacts_frame, text=checkout['guest_name'], relief=tk.RIDGE).grid(row=idx, column=0, padx=10, pady=5, sticky='nsew')
                ttk.Label(self.contacts_frame, text=checkout['contact_number'], relief=tk.RIDGE).grid(row=idx, column=1, padx=10, pady=5, sticky='nsew')
                ttk.Label(self.contacts_frame, text=checkout['card'], relief=tk.RIDGE).grid(row=idx, column=2, padx=10, pady=5, sticky='nsew')
                ttk.Label(self.contacts_frame, text=checkout['room_number'], relief=tk.RIDGE).grid(row=idx, column=3, padx=10, pady=5, sticky='nsew')


    def exit_app(self):
        self.root.destroy()

    def get_screen_size(self):
        user32 = ctypes.windll.user32
        return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    def add_room(self):
        # Generate room_number (auto-generated from array index + 1)
        room_number = len(rooms) + 1

        # Create a new room with default values
        room = {
            "room_number": room_number,
            "room_type": tk.StringVar(),
            "price": tk.DoubleVar(),
            "wifi": tk.BooleanVar(),
            "tv": tk.BooleanVar()
        }
        rooms.append(room)

        # Update the rooms display
        self.show_rooms()

    def remove_room(self, room):
        rooms.remove(room)
        # Update the rooms display after removing the room
        self.show_rooms()

    def show_rooms(self):
        # Clear current rooms display if any
        for widget in self.rooms_frame.winfo_children():
            widget.destroy()

        # Display each room in the rooms list
        for idx, room in enumerate(rooms, start=1):
            room_frame = ttk.Frame(self.rooms_frame, padding=10, relief=tk.RIDGE, borderwidth=2)
            room_frame.grid(row=idx, column=0, columnspan=5, padx=10, pady=5, sticky='ew')

            # Room number label
            ttk.Label(room_frame, text=f"Room Number: {room['room_number']}").grid(row=0, column=0, padx=5, pady=5)

            # Room type dropdown
            ttk.Label(room_frame, text="Room Type:").grid(row=0, column=1, padx=5, pady=5)
            room_type_dropdown = ttk.Combobox(room_frame, textvariable=room['room_type'],
                                              values=["Single", "Double", "Suite"], state="readonly")
            room_type_dropdown.grid(row=0, column=2, padx=5, pady=5)

            # Price entry
            ttk.Label(room_frame, text="Price:").grid(row=0, column=3, padx=5, pady=5)
            price_entry = ttk.Entry(room_frame, textvariable=room['price'])
            price_entry.grid(row=0, column=4, padx=5, pady=5)

            # Wifi checkbox
            wifi_check = ttk.Checkbutton(room_frame, text="Wifi", variable=room['wifi'])
            wifi_check.grid(row=1, column=0, padx=5, pady=5)

            # TV checkbox
            tv_check = ttk.Checkbutton(room_frame, text="TV", variable=room['tv'])
            tv_check.grid(row=1, column=1, padx=5, pady=5)

            # Remove room button
            remove_button = ttk.Button(room_frame, text="Remove Room", command=lambda r=room: self.remove_room(r))
            remove_button.grid(row=1, column=2, columnspan=3, padx=5, pady=5)

        # Show Add Room button after showing rooms list
        self.add_room_button = ttk.Button(self.rooms_frame, text="Add Room", command=self.add_room)
        self.add_room_button.grid(row=len(rooms) + 1, column=0, padx=5, pady=10, sticky='ew')
        
        # Update canvas scroll region
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def hide_frames(self):
        # Hide all frames except the welcome label
        for frame in (self.canvas, self.reservation_frame,self.contacts_frame,self.status_frame):
            frame.grid_forget()

    def create_reservation_form(self):
        for widget in self.reservation_frame.winfo_children():
            widget.destroy()
        # Reservation form fields
        ttk.Label(self.reservation_frame, text="Guest Information", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        # Second row: First Name
        ttk.Label(self.reservation_frame, text="First Name:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.first_name_entry = ttk.Entry(self.reservation_frame)
        self.first_name_entry.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        # Second row: Last Name
        ttk.Label(self.reservation_frame, text="Last Name:").grid(row=2, column=2, padx=10, pady=5, sticky='e')
        self.last_name_entry = ttk.Entry(self.reservation_frame)
        self.last_name_entry.grid(row=2, column=3, padx=10, pady=5, sticky='w')

        # Third row: Email
        ttk.Label(self.reservation_frame, text="Email:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.email_entry = ttk.Entry(self.reservation_frame)
        self.email_entry.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        # Third row: Address
        ttk.Label(self.reservation_frame, text="Address:").grid(row=3, column=2, padx=10, pady=5, sticky='e')
        self.address_entry = ttk.Entry(self.reservation_frame)
        self.address_entry.grid(row=3, column=3, padx=10, pady=5, sticky='w')

        # Fourth row: Number of Adults
        ttk.Label(self.reservation_frame, text="Number of Adults:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
        self.num_adults_entry = ttk.Entry(self.reservation_frame)
        self.num_adults_entry.grid(row=4, column=1, padx=10, pady=5, sticky='w')

        # Fourth row: Number of Children
        ttk.Label(self.reservation_frame, text="Number of Children:").grid(row=4, column=2, padx=10, pady=5, sticky='e')
        self.num_children_entry = ttk.Entry(self.reservation_frame)
        self.num_children_entry.grid(row=4, column=3, padx=10, pady=5, sticky='w')

        # Fifth row: Room Type
        ttk.Label(self.reservation_frame, text="Room Type:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
        self.room_type_var = tk.StringVar(self.reservation_frame)
        room_type_dropdown = ttk.Combobox(self.reservation_frame, textvariable=self.room_type_var,
                                          values=["Single", "Double", "Suite"], state="readonly")
        room_type_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky='w')
        room_type_dropdown.bind("<<ComboboxSelected>>", lambda event: self.update_available_rooms())

        # Fifth row: Wifi, TV
        self.wifi_var = tk.BooleanVar(self.reservation_frame)
        wifi_checkbutton = ttk.Checkbutton(self.reservation_frame, text="Wifi", variable=self.wifi_var)
        wifi_checkbutton.grid(row=5, column=2, padx=10, pady=5, sticky='w')
        wifi_checkbutton.bind("<ButtonRelease-1>", lambda event: self.update_available_rooms())

        self.tv_var = tk.BooleanVar(self.reservation_frame)
        tv_checkbutton = ttk.Checkbutton(self.reservation_frame, text="TV", variable=self.tv_var)
        tv_checkbutton.grid(row=5, column=3, padx=10, pady=5, sticky='w')
        tv_checkbutton.bind("<ButtonRelease-1>", lambda event: self.update_available_rooms())
        
        # Sixth row: Available Rooms
        ttk.Label(self.reservation_frame, text="Available Rooms:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
        self.available_rooms_var = tk.StringVar(self.reservation_frame)
        self.available_rooms_dropdown = ttk.Combobox(self.reservation_frame, textvariable=self.available_rooms_var, state="readonly")
        self.available_rooms_dropdown.grid(row=6, column=1, padx=10, pady=5, sticky='w')

        # Sixth row: No rooms available label
        self.no_rooms_label = ttk.Label(self.reservation_frame, text="No rooms available", foreground="red")
        self.no_rooms_label.grid(row=6, column=1, padx=10, pady=5, sticky='w')
        self.no_rooms_label.grid_remove()  # Initially hide it

        # Submit reservation button (spanning four columns)
        ttk.Button(self.reservation_frame, text="Submit Reservation", command=self.save_reservation).grid(row=7, column=0, columnspan=4, padx=10, pady=10)

    def update_available_rooms(self):
        room_type = self.room_type_var.get()
        wifi = self.wifi_var.get()
        tv = self.tv_var.get()

        matching_rooms = [room["room_number"] for room in rooms if room["room_type"].get() == room_type and room["wifi"].get() == wifi and room["tv"].get() == tv]

        if matching_rooms:
            self.available_rooms_dropdown["values"] = matching_rooms
            self.available_rooms_dropdown.set('')
            self.available_rooms_dropdown.grid()
            self.no_rooms_label.grid_remove()
        else:
            self.available_rooms_dropdown.grid_remove()
            self.no_rooms_label.grid()
            
    def save_reservation(self):
        # Capture reservation details
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        address = self.address_entry.get()
        num_adults = self.num_adults_entry.get()
        num_children = self.num_children_entry.get()
        room_type = self.room_type_var.get()
        wifi = self.wifi_var.get()
        tv = self.tv_var.get()
        room_number = self.available_rooms_var.get()

        # Validate input fields
        if not first_name or not last_name or not num_adults or not num_children or not room_type:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        # Convert number of adults and children to integers
        try:
            num_adults = int(num_adults)
            num_children = int(num_children)
        except ValueError:
            messagebox.showerror("Error", "Number of adults and children must be integers.")
            return

        # Create reservation details dictionary
        reservation_details = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "address": address,
            "num_adults": num_adults,
            "num_children": num_children,
            "room_type": room_type,
            "wifi": wifi,
            "tv": tv,
            "room_number": room_number
        }

        # Save reservation details 
        reservations.append(reservation_details)
        
        # Show success message
        messagebox.showinfo("Reservation Saved", "Reservation has been successfully saved!")

        # Optionally, clear form fields after successful reservation
        self.clear_reservation_form()

    def clear_reservation_form(self):
        # Clear all form fields
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.num_adults_entry.delete(0, tk.END)
        self.num_children_entry.delete(0, tk.END)
        self.room_type_var.set('')
        self.available_rooms_var.set('')
        self.wifi_var.set(False)
        self.tv_var.set(False)

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelManagementApp(root)
    app.run()
