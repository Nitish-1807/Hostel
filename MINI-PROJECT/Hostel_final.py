import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

DATA_FILE = "hostel_data.json"
COLLEGE_IDS_FILE = "college_ids.json"  # File to store valid student IDs

# Function to load valid student IDs from file
def load_valid_ids():
    try:
        with open(COLLEGE_IDS_FILE, "r") as file:
            return json.load(file)  # Returns a list of valid IDs
    except FileNotFoundError:
        messagebox.showerror("Error", "The file containing student IDs was not found.")
        return []

class HostelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hostel Management System")
        self.root.geometry("800x600")  # Set default window size

        # Load hostel data and set up the UI
        self.hostels = self.load_data()

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Use a modern theme
        self.style.configure("TButton", font=("Helvetica", 12), padding=6)
        self.style.configure("TLabel", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Create Frames for each Tab
        self.view_rooms_frame = ttk.Frame(self.notebook)
        self.add_hostel_frame = ttk.Frame(self.notebook)

        # Add Frames to Tabs
        self.notebook.add(self.view_rooms_frame, text="View Rooms & Book")
        self.notebook.add(self.add_hostel_frame, text="Add Hostel")

        # View Rooms & Booking Tab
        self.admin_code_label = ttk.Label(self.view_rooms_frame, text="Admin Code:")
        self.admin_code_label.pack(pady=5)
        self.admin_code_entry = ttk.Entry(self.view_rooms_frame, show="*")  # Mask input with '*'
        self.admin_code_entry.pack(pady=5)
        self.admin_code_button = ttk.Button(self.view_rooms_frame, text="Enter Admin Code", command=self.check_admin_code)
        self.admin_code_button.pack(pady=10)

        self.tree = ttk.Treeview(self.view_rooms_frame, columns=("Hostel", "Distance", "Category"), show='headings', height=15)
        self.tree.heading("Hostel", text="Nearby Hostels")
        self.tree.heading("Distance", text="Distance (km)")
        self.tree.heading("Category", text="Category")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.populate_hostel_list()

        self.view_rooms_button = ttk.Button(self.view_rooms_frame, text="View Rooms", command=self.view_rooms)
        self.view_rooms_button.pack(side="left", padx=10, pady=10)

        # Add Hostel Tab
        self.add_hostel_button = ttk.Button(self.add_hostel_frame, text="Add Hostel", command=self.add_hostel)
        self.add_hostel_button.pack(pady=20)
        self.add_hostel_button.config(state="disabled")  # Disable until correct code is entered

        # Add some helpful information
        self.info_label = ttk.Label(self.add_hostel_frame, text="Enter admin code in the 'View Rooms' tab to enable adding hostels.",
                                    foreground="blue")
        self.info_label.pack(pady=10)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        return {}

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.hostels, file, indent=4)

    def populate_hostel_list(self):
        self.tree.delete(*self.tree.get_children())
        for hostel, info in self.hostels.items():
            distance = info.get("distance", "N/A")
            category = info.get("category", "N/A")
            self.tree.insert("", "end", values=(hostel, distance, category))

    def check_admin_code(self):
        entered_code = self.admin_code_entry.get()
        if entered_code == "admin123":
            messagebox.showinfo("Success", "Access granted. You can now add hostels.")
            self.add_hostel_button.config(state="normal")  # Enable Add Hostel button
        else:
            messagebox.showwarning("Invalid Code", "Incorrect admin code. Access denied.")

    def view_rooms(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a hostel!")
            return
        hostel_name = self.tree.item(selected_item, "values")[0]
        RoomWindow(self.root, hostel_name, self.hostels[hostel_name]["floors"], self.save_data)

    def add_hostel(self):
        hostel_name = simpledialog.askstring("Hostel Name", "Enter the name of the new hostel:")
        if not hostel_name:
            messagebox.showwarning("Warning", "Hostel name cannot be empty!")
            return
        
        if hostel_name in self.hostels:
            messagebox.showwarning("Warning", "Hostel already exists!")
            return
        
        num_floors = simpledialog.askinteger("Number of Floors", "Enter the number of floors for this hostel:", minvalue=1)
        if not num_floors:
            messagebox.showwarning("Warning", "Number of floors must be greater than 0!")
            return

        standard_num_rooms = simpledialog.askinteger("Standard Number of Rooms", "Enter the standard number of rooms per floor:", minvalue=1)
        standard_capacity = simpledialog.askinteger("Standard Capacity", "Enter the standard capacity for each room:", minvalue=1)
        veg_price = simpledialog.askfloat("Veg Price", "Enter the price for veg meals:")
        non_veg_price = simpledialog.askfloat("Non-Veg Price", "Enter the price for non-veg meals:")

        floors = {}
        for i in range(num_floors):
            floor_name = f"Floor {i + 1}"
            floors[floor_name] = {
                f"Room {j + 1}": {
                    "status": "available",
                    "capacity": standard_capacity,
                    "occupants": [],
                    "veg_price": veg_price,
                    "non_veg_price": non_veg_price
                } for j in range(standard_num_rooms)
            }

        distance = simpledialog.askfloat("Distance", "Enter the distance from the college (in km):")
        category = simpledialog.askstring("Category", "Enter the category (Boys, Girls, Mixed):")
        if category not in ["Boys", "Girls", "Mixed"]:
            messagebox.showwarning("Warning", "Category must be one of Boys, Girls, Mixed!")
            return
        
        self.hostels[hostel_name] = {
            "distance": distance,
            "category": category,
            "floors": floors
        }
        self.save_data()
        self.populate_hostel_list()

class RoomWindow:
    def __init__(self, root, hostel_name, floors, save_callback):
        self.root = tk.Toplevel(root)
        self.root.title(f"{hostel_name} - Rooms")
        self.floors = floors
        self.save_callback = save_callback

        # Load valid IDs once during initialization
        self.valid_ids = load_valid_ids()

        self.floor_list = tk.Listbox(self.root)
        self.floor_list.pack(side="left", fill="y", padx=10, pady=10)
        for floor in self.floors:
            self.floor_list.insert(tk.END, floor)

        self.room_tree = ttk.Treeview(self.root, columns=("Room", "Status", "Booked", "Remaining", "Capacity"), show='headings')
        self.room_tree.heading("Room", text="Room")
        self.room_tree.heading("Status", text="Status")
        self.room_tree.heading("Booked", text="Booked")
        self.room_tree.heading("Remaining", text="Remaining")
        self.room_tree.heading("Capacity", text="Capacity")
        self.room_tree.pack(fill="both", expand=True)

        self.floor_list.bind("<<ListboxSelect>>", self.populate_room_list)
        self.book_room_button = tk.Button(self.root, text="Book Room", command=self.open_booking_window)
        self.book_room_button.pack(pady=10)

    def populate_room_list(self, event=None):
        try:
            selected_floor = self.floor_list.get(self.floor_list.curselection())
            rooms = self.floors[selected_floor]
            self.room_tree.delete(*self.room_tree.get_children())
            for room, info in rooms.items():
                booked = len(info["occupants"])
                remaining = info["capacity"] - booked
                status = "Fully Booked" if remaining == 0 else "Available"
                self.room_tree.insert("", "end", values=(room, status, booked, remaining, info["capacity"]))
        except tk.TclError:
            pass

    def open_booking_window(self):
        try:
            selected_floor = self.floor_list.get(self.floor_list.curselection())
            selected_room = self.room_tree.item(self.room_tree.selection())["values"][0]
            room_data = self.floors[selected_floor][selected_room]

            if room_data["capacity"] == len(room_data["occupants"]):
                messagebox.showwarning("Warning", "Room is fully booked!")
                return

            student_id = simpledialog.askstring("Student ID", "Enter Student ID:")

            # Check if the student ID is valid
            if student_id not in self.valid_ids:
                messagebox.showwarning("Warning", "Invalid Student ID!")
                return

            if any(occupant["id"] == student_id for occupant in room_data["occupants"]):
                messagebox.showwarning("Warning", "Student already booked this room!")
                return

            meal_choice = simpledialog.askstring("Meal Choice", "Enter meal choice (Veg/Non-Veg):")
            if meal_choice not in ["Veg", "Non-Veg"]:
                messagebox.showwarning("Warning", "Invalid meal choice!")
                return

            room_data["occupants"].append({"id": student_id, "meal": meal_choice})
            self.save_callback()  # Save the updated data
            self.populate_room_list()

        except IndexError:
            messagebox.showwarning("Warning", "No room selected!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HostelManagementSystem(root)
    root.mainloop()
