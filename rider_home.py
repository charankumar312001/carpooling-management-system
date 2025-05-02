import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import subprocess
import sys
from utils import DBAccess, centre_window
from constants import COLORS, FONTS



# ======================================================================
# Database Operations
# ======================================================================
class RiderOperations:
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
    def get_bookings(user_id):
        return DBAccess.execute_query(
            """SELECT 
                b.id, b.ride_id, b.passenger_id, b.seats, 
                b.created_at, b.status,
                r.start_location, r.destination, r.departure_time, 
                r.arrival_time, r.price, 
                u.first_name, u.last_name, u.phone 
            FROM bookings b
            JOIN rides r ON b.ride_id = r.id
            JOIN users u ON r.driver_id = u.id
            WHERE b.passenger_id = %s
            ORDER BY b.created_at DESC""",
            (user_id,)
        )

# ======================================================================
# GUI Functions
# ======================================================================
def load_rides():
    try:
        clear_content()
        
        # Header with refresh button
        header_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['background'])
        header_frame.pack(fill='x', pady=10)
        
        ctk.CTkLabel(header_frame, 
                    text="Available Rides", 
                    font=FONTS['title']).pack(side='left')
        
        ctk.CTkButton(header_frame,
                     text="Refresh",
                     command=load_rides,
                     width=100).pack(side='right')

        # Rides list
        rides_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        rides_frame.pack(fill='both', expand=True, pady=10)

        rides = DBAccess.execute_query("SELECT * FROM rides WHERE available_seats > 0")
        
        for ride in rides:
            ride_card = ctk.CTkFrame(rides_frame, fg_color=COLORS['secondary'], corner_radius=8)
            ride_card.pack(fill='x', pady=5, padx=10, expand=True)

            # Ride details
            departure = ride['departure_time']
            arrival = ride['arrival_time']
            duration = arrival - departure
            hours, remainder = divmod(duration.seconds, 3600)
            minutes = remainder // 60

            details_frame = ctk.CTkFrame(ride_card, fg_color='transparent')
            details_frame.pack(side='left', fill='x', expand=True, padx=10)
            
            ctk.CTkLabel(details_frame, 
                        text=f"{ride['start_location']} → {ride['destination']}",
                        font=FONTS['label_bold'],
                        text_color="white").pack(anchor='w')
            
            time_details = (
                f"Departure: {departure.strftime('%a, %d %b %Y %I:%M %p')}\n"
                f"Arrival: {arrival.strftime('%a, %d %b %Y %I:%M %p')}\n"
                f"Duration: {hours}h {minutes}m | Seats: {ride['available_seats']}"
            )
            ctk.CTkLabel(details_frame,
                        text=time_details,
                        font=FONTS['label'],
                        text_color="white").pack(anchor='w')

            # Price and booking
            action_frame = ctk.CTkFrame(ride_card, fg_color='transparent')
            action_frame.pack(side='right', padx=10)
            
            ctk.CTkLabel(action_frame,
                        text=f"${ride['price']}/seat",
                        font=FONTS['label_bold'],
                        text_color="white").pack(anchor='e')
            
            ctk.CTkButton(action_frame,
                         text="Book Now",
                         command=lambda r=ride: show_booking_form(r['id']),
                         width=100).pack(pady=5)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load rides: {str(e)}")

def show_booking_form(ride_id):
    try:
        clear_content()
        
        # Back button
        back_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['background'])
        back_frame.pack(fill='x', pady=10)
        ctk.CTkButton(back_frame,
                     text="← Back to Rides",
                     command=load_rides,
                     fg_color="transparent",
                     text_color=COLORS['primary']).pack(anchor='w')

        # Form content
        form_frame = ctk.CTkFrame(content_frame, fg_color=COLORS['background'])
        form_frame.pack(fill='both', expand=True, padx=40, pady=20)

        # Get ride details using existing query method
        ride = DBAccess.execute_query("SELECT * FROM rides WHERE id = %s", (ride_id,))[0]
        
        ctk.CTkLabel(form_frame, 
                    text="Book Your Seats", 
                    font=FONTS['title']).pack(pady=10)

        # Seat selection
        seats_var = ctk.IntVar(value=1)
        ctk.CTkLabel(form_frame, 
                    text="Number of Seats:", 
                    font=FONTS['label_bold']).pack()
        
        seats_spin = ctk.CTkOptionMenu(form_frame,
                                      values=[str(i) for i in range(1, ride['available_seats'] + 1)],
                                      variable=seats_var)
        seats_spin.pack(pady=10)

        def submit_booking():
            try:
                seats = seats_var.get()
                
                # Use context managers for connection and cursor
                with DBAccess.get_connection() as conn:
                    with conn.cursor() as cursor:
                        try:
                            # Atomic seat update
                            cursor.execute(
                                """UPDATE rides 
                                SET available_seats = available_seats - %s 
                                WHERE id = %s AND available_seats >= %s""",
                                (seats, ride_id, seats)
                            )
                            
                            if cursor.rowcount == 0:
                                raise Exception("Not enough seats available")
                            
                            # Create booking
                            cursor.execute(
                                """INSERT INTO bookings (ride_id, passenger_id, seats)
                                VALUES (%s, %s, %s)""",
                                (ride_id, user_id, seats)
                            )
                            
                            conn.commit()
                            messagebox.showinfo("Success", "Booking confirmed!")
                            show_bookings()
                            
                        except Exception as e:
                            conn.rollback()
                            raise e

            except Exception as e:
                messagebox.showerror("Error", f"Booking failed: {str(e)}")

        ctk.CTkButton(form_frame,
                     text="Confirm Booking",
                     command=submit_booking,
                     fg_color=COLORS['primary']).pack(pady=20)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load form: {str(e)}")
        load_rides()

def show_profile(edit_mode=False):
    try:
        clear_content()
        
        profile = RiderOperations.get_profile(user_id)
        
        profile_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        profile_frame.pack(fill='both', expand=True, padx=20, pady=20)

        fields = [
            ('Username:', 'username', profile['username'], False),
            ('Email:', 'email', profile['email'], True),
            ('First Name:', 'first_name', profile['first_name'], True),
            ('Last Name:', 'last_name', profile['last_name'], True),
            ('Phone:', 'phone', profile['phone'], True)
        ]
        
        entries = {}
        for label, field, value, editable in fields:
            field_frame = ctk.CTkFrame(profile_frame, fg_color=COLORS['background'])
            field_frame.pack(fill='x', pady=5)
            
            ctk.CTkLabel(field_frame, 
                        text=label, 
                        font=FONTS['label_bold'],
                        width=150).pack(side='left')
            
            if edit_mode and editable:
                entry = ctk.CTkEntry(field_frame,
                                    fg_color="white",
                                    border_color=COLORS['primary'],
                                    width=300)
                entry.insert(0, value)
                entry.pack(side='left')
                entries[field] = entry
            else:
                ctk.CTkLabel(field_frame, 
                            text=value, 
                            font=FONTS['value']).pack(side='left')

        if edit_mode:
            def update_profile():
                try:
                    update_data = {
                        'email': entries['email'].get(),
                        'first_name': entries['first_name'].get(),
                        'last_name': entries['last_name'].get(),
                        'phone': entries['phone'].get()
                    }
                    if RiderOperations.update_profile(user_id, update_data):
                        messagebox.showinfo("Success", "Profile updated!")
                        show_profile()
                except Exception as e:
                    messagebox.showerror("Error", f"Update failed: {str(e)}")
            
            btn_frame = ctk.CTkFrame(profile_frame, fg_color=COLORS['background'])
            btn_frame.pack(pady=10)
            
            ctk.CTkButton(btn_frame,
                         text="Save Changes",
                         command=update_profile,
                         fg_color=COLORS['primary']).pack(side='left', padx=10)
            
            ctk.CTkButton(btn_frame,
                         text="Cancel",
                         command=lambda: show_profile(),
                         fg_color=COLORS['secondary']).pack(side='left', padx=10)
        else:
            ctk.CTkButton(profile_frame,
                         text="Edit Profile",
                         command=lambda: show_profile(edit_mode=True),
                         fg_color=COLORS['primary']).pack(pady=10)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load profile: {str(e)}")

def show_bookings():
    try:
        clear_content()
        
        bookings = RiderOperations.get_bookings(user_id)
        
        bookings_frame = ctk.CTkScrollableFrame(content_frame, fg_color=COLORS['background'])
        bookings_frame.pack(fill='both', expand=True, padx=20, pady=20)

        if not bookings:
            ctk.CTkLabel(bookings_frame, 
                        text="No bookings found", 
                        font=FONTS['subtitle'],
                        text_color="white").pack()
            return

        for booking in bookings:
            booking_card = ctk.CTkFrame(bookings_frame, fg_color=COLORS['secondary'], corner_radius=8)
            booking_card.pack(fill='x', pady=5, padx=10)

            status = booking.get('status', 'pending')
            status_color = COLORS['success'] if status == 'confirmed' else COLORS['secondary']
            
            status_frame = ctk.CTkFrame(booking_card, fg_color=status_color, width=100)
            status_frame.pack(side='right', padx=10, pady=5)
            ctk.CTkLabel(status_frame,
                        text=status.capitalize(),
                        font=FONTS['label_bold'],
                        text_color="white").pack(pady=5)

            details_frame = ctk.CTkFrame(booking_card, fg_color='transparent')
            details_frame.pack(side='left', fill='x', expand=True, padx=10)

            departure = booking['departure_time'].strftime('%a, %d %b %Y %I:%M %p')
            arrival = booking['arrival_time'].strftime('%a, %d %b %Y %I:%M %p')
            
            ctk.CTkLabel(details_frame,
                        text=f"{booking['start_location']} → {booking['destination']}",
                        font=FONTS['label_bold'],
                        text_color="white").pack(anchor='w')
            
            ctk.CTkLabel(details_frame,
                        text=f"Departure: {departure}\nArrival: {arrival}",
                        font=FONTS['label'],
                        text_color="white").pack(anchor='w')
            
            ctk.CTkLabel(details_frame,
                        text=f"Seats: {booking['seats']} | Status: {status}",
                        font=FONTS['label'],
                        text_color="white").pack(anchor='w')

            if status == 'confirmed':
                driver_info = (
                    f"Driver: {booking['first_name']} {booking['last_name']}\n"
                    f"Contact: {booking['phone']}"
                )
                ctk.CTkLabel(details_frame,
                            text=driver_info,
                            font=FONTS['label'],
                            text_color="white").pack(anchor='w', pady=5)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load bookings: {str(e)}")
        
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def logout():
    window.destroy()
    subprocess.Popen([sys.executable, "login.py"])

# ======================================================================
# Window Setup
# ======================================================================
window = ctk.CTk()
window.title("Rider Dashboard")
window.geometry("1200x800")
window.configure(fg_color=COLORS['background'])
centre_window(window)

user_id = sys.argv[1] if len(sys.argv) > 1 else None

# Navigation Bar
nav_frame = ctk.CTkFrame(window, fg_color=COLORS['primary'], height=50)
nav_frame.pack(fill='x', padx=20, pady=10)

def create_nav_button(text, command):
    return ctk.CTkButton(nav_frame,
                        text=text,
                        command=command,
                        fg_color="transparent",
                        hover_color=COLORS['secondary'],
                        text_color="white",
                        font=FONTS['button'],
                        corner_radius=0)

create_nav_button("Rides", load_rides).pack(side='left', padx=15)
create_nav_button("My Bookings", show_bookings).pack(side='left', padx=15)
create_nav_button("Profile", lambda: show_profile()).pack(side='left', padx=15)
create_nav_button("Logout", logout).pack(side='right', padx=15)

# Content Frame
content_frame = ctk.CTkFrame(window, fg_color=COLORS['background'])
content_frame.pack(fill='both', expand=True, padx=20, pady=20)

# Initial Load
load_rides()
window.mainloop()