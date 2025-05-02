import tkinter as tk
import customtkinter as ctk
from tkinter import ttk, messagebox
import subprocess
from utils import DBAccess, centre_window
from constants import COLORS, FONTS
import sys
from datetime import datetime
from tkcalendar import DateEntry
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

# Database Operations
class DriverOperations:
    @staticmethod
    def get_profile(user_id):
        return DBAccess.execute_query(
            "SELECT * FROM users WHERE id = %s", (user_id,)
        )[0]

    @staticmethod
    def update_profile(user_id, data):
        return DBAccess.execute_update(
            """UPDATE users SET 
            email = %s, first_name = %s, 
            last_name = %s, phone = %s 
            WHERE id = %s""",
            (data['email'], data['first_name'], 
             data['last_name'], data['phone'], user_id)
        )

    @staticmethod
    def create_ride(user_id, data):
        return DBAccess.execute_update(
            """INSERT INTO rides 
            (driver_id, start_location, destination, 
            departure_time, arrival_time, available_seats, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (user_id, data['source'], data['destination'],
             f"{data['departure_date']} {data['departure_time']}",
             f"{data['arrival_date']} {data['arrival_time']}",
             data['seats'], data['price'])
        )

    @staticmethod
    def get_rides(user_id):
        return DBAccess.execute_query(
            """SELECT * FROM rides 
            WHERE driver_id = %s 
            ORDER BY departure_time DESC""",
            (user_id,)
        )

    @staticmethod
    def update_ride(ride_id, data):
        return DBAccess.execute_update(
            """UPDATE rides SET
            start_location = %s,
            destination = %s,
            departure_time = %s,
            arrival_time = %s,
            available_seats = %s,
            price = %s
            WHERE id = %s""",
            (data['source'], data['destination'],
             f"{data['departure_date']} {data['departure_time']}",
             f"{data['arrival_date']} {data['arrival_time']}",
             data['seats'], data['price'], ride_id)
        )

    @staticmethod
    def get_ride_requests(ride_id):
        return DBAccess.execute_query(
            """SELECT 
                b.id, 
                b.ride_id, 
                b.passenger_id, 
                b.seats, 
                b.created_at, 
                b.status,
                u.username, 
                u.email, 
                u.phone 
            FROM bookings b
            JOIN users u ON b.passenger_id = u.id
            WHERE b.ride_id = %s""",
            (ride_id,)
        )

    @staticmethod
    def update_booking_status(booking_id, status):
        return DBAccess.execute_update(
            "UPDATE bookings SET status = %s WHERE id = %s",
            (status, booking_id)
        )

    @staticmethod
    def delete_ride(ride_id):
        return DBAccess.execute_update(
            "DELETE FROM rides WHERE id = %s",
            (ride_id,)
        )

# Window setup
window = ctk.CTk()
window.title("Driver Dashboard")
window.geometry("1200x800")
window.configure(fg_color=COLORS['background'])
centre_window(window)

user_id = sys.argv[1] if len(sys.argv) > 1 else None

# Navigation Bar
nav_frame = ctk.CTkFrame(window, fg_color=COLORS['primary'], height=50)
nav_frame.pack(fill='x', padx=20, pady=10)

def logout():
    window.destroy()
    subprocess.Popen([sys.executable, "login.py"])

def create_logout_button(text, command):
    return ctk.CTkButton(nav_frame,
                         text=text,
                         command=command,
                         fg_color="#cc3333",
                         hover_color="#aa2222",
                         text_color="white",
                         font=FONTS['button'],
                         corner_radius=0)

def create_nav_button(text, command):
    return ctk.CTkButton(nav_frame,
                         text=text,
                         command=command,
                         fg_color="transparent",
                         hover_color=COLORS['secondary'],
                         text_color="white",
                         font=FONTS['button'],
                         corner_radius=0)

# Create buttons
create_nav_button("View Profile", lambda: show_profile()).pack(side='left', padx=15)
create_nav_button("Edit Profile", lambda: show_edit_profile()).pack(side='left', padx=15)
create_nav_button("View Rides", lambda: show_view_rides()).pack(side='left', padx=15)
create_nav_button("Add Ride", lambda: show_add_ride()).pack(side='left', padx=15)
create_nav_button("Drive Report", lambda: show_drive_report()).pack(side='left', padx=15)
create_logout_button("Logout", logout).pack(side='left', padx=15)

# Content Frame
content_frame = ctk.CTkFrame(window, fg_color=COLORS['background'])
content_frame.pack(fill='both', expand=True, padx=20, pady=20)

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

# Profile Section
def show_profile():
    clear_content()
    try:
        user_data = DriverOperations.get_profile(user_id)
        
        profile_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        profile_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        fields = [
            ('Username:', user_data['username']),
            ('Email:', user_data['email']),
            ('First Name:', user_data['first_name']),
            ('Last Name:', user_data['last_name']),
            ('Phone:', user_data['phone']),
            ('Driver Status:', 'Verified Driver' if user_data['is_driver'] else 'Not a Driver')
        ]
        
        for label, value in fields:
            field_frame = ctk.CTkFrame(profile_frame, fg_color=COLORS['background'])
            field_frame.pack(fill='x', pady=5)
            
            ctk.CTkLabel(field_frame, 
                        text=label, 
                        font=FONTS['label'],
                        width=150,
                        anchor='w').pack(side='left')
            ctk.CTkLabel(field_frame, 
                        text=value, 
                        font=FONTS['value'],
                        text_color=COLORS['text']).pack(side='left')
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load profile: {str(e)}")

def show_edit_profile():
    clear_content()
    try:
        user_data = DriverOperations.get_profile(user_id)
        
        edit_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        edit_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        fields = [
            ('Email:', 'email', user_data['email']),
            ('First Name:', 'first_name', user_data['first_name']),
            ('Last Name:', 'last_name', user_data['last_name']),
            ('Phone:', 'phone', user_data['phone'])
        ]
        
        entries = {}
        for label, name, value in fields:
            field_frame = ctk.CTkFrame(edit_frame, fg_color=COLORS['background'])
            field_frame.pack(fill='x', pady=10)
            
            ctk.CTkLabel(field_frame, 
                        text=label, 
                        font=FONTS['label'],
                        width=150).pack(side='left')
            entry = ctk.CTkEntry(field_frame,
                                fg_color="white",
                                border_color=COLORS['primary'],
                                width=300)
            entry.insert(0, value)
            entry.pack(side='left')
            entries[name] = entry
        
        def update_profile():
            try:
                update_data = {name: entries[name].get() for name in entries}
                if DriverOperations.update_profile(user_id, update_data):
                    messagebox.showinfo("Success", "Profile updated successfully!")
                    show_profile()
            except Exception as e:
                messagebox.showerror("Error", f"Update failed: {str(e)}")
        
        ctk.CTkButton(edit_frame,
                     text="Save Changes",
                     command=update_profile,
                     fg_color=COLORS['primary'],
                     hover_color=COLORS['secondary']).pack(pady=20)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load profile: {str(e)}")

# Rides Section
def show_view_rides():
    clear_content()
    try:
        rides = DriverOperations.get_rides(user_id)
        
        rides_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        rides_frame.pack(fill='both', expand=True, padx=20, pady=20)

        if not rides:
            ctk.CTkLabel(rides_frame, text="No rides created yet", font=FONTS['subtitle']).pack()
            return

        for ride in rides:
            ride_card = ctk.CTkFrame(rides_frame, fg_color=COLORS['secondary'], corner_radius=8)
            ride_card.pack(fill='x', pady=5, padx=10)

            departure = ride['departure_time']
            arrival = ride['arrival_time']
            duration = arrival - departure
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60
            
            time_details = (
                f"Departure: {departure.strftime('%a, %d %b %Y %I:%M %p')}\n"
                f"Arrival: {arrival.strftime('%a, %d %b %Y %I:%M %p')}\n"
                f"Duration: {hours}h {minutes}m"
            )

            info_frame = ctk.CTkFrame(ride_card, fg_color='transparent')
            info_frame.pack(side='left', fill='x', expand=True, padx=10)
            
            ctk.CTkLabel(info_frame, 
                        text=f"{ride['start_location']} → {ride['destination']}",
                        font=FONTS['label_bold'],
                        text_color="white").pack(anchor='w')
            
            ctk.CTkLabel(info_frame,
                        text=time_details,
                        font=FONTS['label'],
                        text_color="white").pack(anchor='w')

            stats_frame = ctk.CTkFrame(ride_card, fg_color='transparent')
            stats_frame.pack(side='right', padx=10)

            stats_text = (
                f"Available Seats: {ride['available_seats']}\n"
                f"Price: ₹{ride['price']}/seat\n"
                f"Status: {get_ride_status(departure)}"
            )
            
            ctk.CTkLabel(stats_frame,
                        text=stats_text,
                        font=FONTS['label'],
                        text_color="white").pack(anchor='e')

            btn_frame = ctk.CTkFrame(ride_card, fg_color='transparent')
            btn_frame.pack(side='right', padx=10)
            
            ctk.CTkButton(btn_frame,
                         text="Requests",
                         command=lambda r=ride: show_ride_requests(r['id']),
                         width=80).pack(pady=2)
            
            ctk.CTkButton(btn_frame,
                         text="Edit",
                         command=lambda r=ride: show_edit_ride(r),
                         width=80).pack(pady=2)
            
            ctk.CTkButton(btn_frame,
                         text="Delete",
                         command=lambda r=ride: delete_ride_confirmation(r['id']),
                         fg_color=COLORS['danger'],
                         hover_color="#cc0000",
                         width=80).pack(pady=2)
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load rides: {str(e)}")

def delete_ride_confirmation(ride_id):
    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this ride?\nAll associated bookings will be cancelled!",
        parent=window
    )
    if confirm:
        try:
            if DriverOperations.delete_ride(ride_id):
                messagebox.showinfo("Success", "Ride deleted successfully!")
                show_view_rides()
            else:
                messagebox.showerror("Error", "Failed to delete ride")
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {str(e)}")

def get_ride_status(departure_time):
    now = datetime.now()
    if departure_time < now:
        return "Completed"
    elif (departure_time - now).days <= 1:
        return "Upcoming (within 24h)"
    return "Scheduled"

def show_ride_requests(ride_id):
    clear_content()
    try:
        requests = DriverOperations.get_ride_requests(ride_id)
        
        requests_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        requests_frame.pack(fill='both', expand=True, padx=20, pady=20)

        if not requests:
            ctk.CTkLabel(requests_frame, text="No requests for this ride", font=FONTS['subtitle']).pack()
            return

        for req in requests:
            req_frame = ctk.CTkFrame(requests_frame, fg_color=COLORS['background'])
            req_frame.pack(fill='x', pady=5, padx=10)

            details = f"{req['username']} ({req['email']}) - {req['phone']} | Status: {req['status'].capitalize()}"
            ctk.CTkLabel(req_frame, 
                        text=details,
                        font=FONTS['label']).pack(side='left', padx=10)

            if req['status'] == 'pending':
                ctk.CTkButton(req_frame,
                            text="Accept",
                            command=lambda r=req: update_request(r['id'], 'confirmed'),
                            fg_color=COLORS['primary'],
                            width=80).pack(side='right', padx=2)
                
                ctk.CTkButton(req_frame,
                            text="Reject",
                            command=lambda r=req: update_request(r['id'], 'cancelled'),
                            fg_color="#ff4444",
                            width=80).pack(side='right', padx=2)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load requests: {str(e)}")

def update_request(booking_id, status):
    try:
        if DriverOperations.update_booking_status(booking_id, status):
            messagebox.showinfo("Success", f"Request {status}!")
            show_view_rides()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update request: {str(e)}")

def show_edit_ride(ride):
    clear_content()
    try:
        edit_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        edit_frame.pack(fill='both', expand=True, padx=20, pady=20)

        time_slots = [f"{h:02d}:{m:02d}" for h in range(0, 24) for m in [0, 15, 30, 45]]
        
        fields = [
            ("Source Location", 'source', 'entry', ride['start_location']),
            ("Destination", 'destination', 'entry', ride['destination']),
            ("Departure Date", 'departure_date', 'date', ride['departure_time'].date()),
            ("Departure Time", 'departure_time', 'time', ride['departure_time'].strftime('%H:%M')),
            ("Arrival Date", 'arrival_date', 'date', ride['arrival_time'].date()),
            ("Arrival Time", 'arrival_time', 'time', ride['arrival_time'].strftime('%H:%M')),
            ("Available Seats", 'seats', 'spin', ride['available_seats']),
            ("Price per Seat", 'price', 'entry', ride['price'])
        ]
        
        entries = {}
        for label, name, field_type, default_val in fields:
            field_frame = ctk.CTkFrame(edit_frame, fg_color=COLORS['background'])
            field_frame.pack(fill='x', pady=10)
            
            ctk.CTkLabel(field_frame, 
                        text=label + ":", 
                        font=FONTS['label'],
                        width=150).pack(side='left')
            
            if field_type == 'entry':
                widget = ctk.CTkEntry(field_frame,
                                      fg_color="white",
                                      border_color=COLORS['primary'],
                                      width=300)
                widget.insert(0, default_val)
            elif field_type == 'date':
                widget = DateEntry(field_frame,
                                  date_pattern='yyyy-mm-dd',
                                  background=COLORS['primary'],
                                  foreground='white')
                widget.set_date(default_val)
            elif field_type == 'time':
                widget = ttk.Combobox(field_frame, values=time_slots, width=10)
                widget.set(default_val)
            elif field_type == 'spin':
                widget = ttk.Spinbox(field_frame, from_=1, to=4, width=5)
                widget.set(default_val)
            
            widget.pack(side='left')
            entries[name] = widget

        def update_ride():
            try:
                ride_data = {
                    'source': entries['source'].get(),
                    'destination': entries['destination'].get(),
                    'departure_date': entries['departure_date'].get(),
                    'departure_time': entries['departure_time'].get(),
                    'arrival_date': entries['arrival_date'].get(),
                    'arrival_time': entries['arrival_time'].get(),
                    'seats': entries['seats'].get(),
                    'price': entries['price'].get()
                }
                
                if DriverOperations.update_ride(ride['id'], ride_data):
                    messagebox.showinfo("Success", "Ride updated successfully!")
                    show_view_rides()
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update ride: {str(e)}")

        ctk.CTkButton(edit_frame,
                     text="Update Ride",
                     command=update_ride,
                     fg_color=COLORS['primary'],
                     hover_color=COLORS['secondary']).pack(pady=20)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load ride details: {str(e)}")

# Add Ride Section
def show_add_ride():
    clear_content()
    try:
        add_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        add_frame.pack(fill='both', expand=True, padx=20, pady=20)

        time_slots = [f"{h:02d}:{m:02d}" for h in range(0, 24) for m in [0, 15, 30, 45]]
        
        fields = [
            ("Source Location", 'source', 'entry'),
            ("Destination", 'destination', 'entry'),
            ("Departure Date", 'departure_date', 'date'),
            ("Departure Time", 'departure_time', 'time'),
            ("Arrival Date", 'arrival_date', 'date'),
            ("Arrival Time", 'arrival_time', 'time'),
            ("Available Seats", 'seats', 'spin'),
            ("Price per Seat", 'price', 'entry')
        ]
        
        entries = {}
        for label, name, field_type in fields:
            field_frame = ctk.CTkFrame(add_frame, fg_color=COLORS['background'])
            field_frame.pack(fill='x', pady=10)
            
            ctk.CTkLabel(field_frame, 
                        text=label + ":", 
                        font=FONTS['label'],
                        width=150).pack(side='left')
            
            if field_type == 'entry':
                widget = ctk.CTkEntry(field_frame,
                                      fg_color="white",
                                      border_color=COLORS['primary'],
                                      width=300)
            elif field_type == 'date':
                widget = DateEntry(field_frame,
                                  date_pattern='yyyy-mm-dd',
                                  background=COLORS['primary'],
                                  foreground='white')
            elif field_type == 'time':
                widget = ttk.Combobox(field_frame, values=time_slots, width=10)
                widget.set("00:00")
            elif field_type == 'spin':
                widget = ttk.Spinbox(field_frame, from_=1, to=4, width=5)
            
            widget.pack(side='left')
            entries[name] = widget

        def submit_ride():
            try:
                ride_data = {
                    'source': entries['source'].get(),
                    'destination': entries['destination'].get(),
                    'departure_date': entries['departure_date'].get(),
                    'departure_time': entries['departure_time'].get(),
                    'arrival_date': entries['arrival_date'].get(),
                    'arrival_time': entries['arrival_time'].get(),
                    'seats': entries['seats'].get(),
                    'price': entries['price'].get()
                }
                
                if DriverOperations.create_ride(user_id, ride_data):
                    messagebox.showinfo("Success", "Ride created successfully!")
                    show_view_rides()
            
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create ride: {str(e)}")

        ctk.CTkButton(add_frame,
                     text="Create Ride",
                     command=submit_ride,
                     fg_color=COLORS['primary'],
                     hover_color=COLORS['secondary']).pack(pady=20)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load ride form: {str(e)}")

# Drive Report Section
def show_drive_report():
    clear_content()
    try:
        rides = DriverOperations.get_rides(user_id)
        
        report_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['background'])
        report_frame.pack(fill='both', expand=True, padx=20, pady=20)

        if not rides:
            ctk.CTkLabel(report_frame, text="No rides available for report", font=FONTS['subtitle']).pack()
            return

        # Create table using Treeview
        columns = ('Route', 'Departure', 'Arrival', 'Duration', 'Seats', 'Price', 'Status')
        tree = ttk.Treeview(report_frame, columns=columns, show='headings')
        tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Set column headings
        tree.heading('Route', text='Route')
        tree.heading('Departure', text='Departure')
        tree.heading('Arrival', text='Arrival')
        tree.heading('Duration', text='Duration')
        tree.heading('Seats', text='Seats')
        tree.heading('Price', text='Price')
        tree.heading('Status', text='Status')

        # Set column widths
        tree.column('Route', width=200)
        tree.column('Departure', width=150)
        tree.column('Arrival', width=150)
        tree.column('Duration', width=100)
        tree.column('Seats', width=80)
        tree.column('Price', width=80)
        tree.column('Status', width=120)

        # Populate table
        for ride in rides:
            departure = ride['departure_time']
            arrival = ride['arrival_time']
            duration = arrival - departure
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60
            
            tree.insert('', 'end', values=(
                f"{ride['start_location']} → {ride['destination']}",
                departure.strftime('%a, %d %b %Y %I:%M %p'),
                arrival.strftime('%a, %d %b %Y %I:%M %p'),
                f"{hours}h {minutes}m",
                ride['available_seats'],
                f"₹{ride['price']}",
                get_ride_status(departure)
            ))

        # Download PDF button
        ctk.CTkButton(report_frame,
                     text="Download All Rides PDF",
                     command=lambda: generate_all_rides_pdf(rides),
                     fg_color=COLORS['primary'],
                     hover_color=COLORS['secondary'],
                     width=200).pack(pady=20)
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load report: {str(e)}")

def generate_all_rides_pdf(rides):
    try:
        filename = f"all_rides_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title = Paragraph("All Rides Report", styles['Title'])
        elements.append(title)
        
        # Rides Table
        rides_data = [['Route', 'Departure', 'Arrival', 'Duration', 'Seats', 'Price', 'Status']]
        for ride in rides:
            departure = ride['departure_time']
            arrival = ride['arrival_time']
            duration = arrival - departure
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60
            
            rides_data.append([
                f"{ride['start_location']} → {ride['destination']}",
                departure.strftime('%a, %d %b %Y %I:%M %p'),
                arrival.strftime('%a, %d %b %Y %I:%M %p'),
                f"{hours}h {minutes}m",
                str(ride['available_seats']),
                f"₹{ride['price']}",
                get_ride_status(departure)
            ])
        
        if len(rides_data) == 1:
            rides_data.append(['No rides', '', '', '', '', '', ''])
        
        rides_table = Table(rides_data)
        rides_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(rides_table)
        
        doc.build(elements)
        messagebox.showinfo("Success", f"PDF report saved as {filename}")
        
        # Open the PDF file
        if os.name == 'nt':  # Windows
            os.startfile(filename)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.call(['open', filename])
            
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate PDF: {str(e)}")

show_profile()
window.mainloop()