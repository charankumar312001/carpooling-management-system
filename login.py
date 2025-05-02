import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import subprocess
from PIL import Image
from utils import DBAccess, resize_image, centre_window
from constants import COLORS, FONTS

def authenticate(username, password):
    result = DBAccess.execute_query(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (username, password)
    )
    return result[0] if result else None

def on_login():
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields")
        return
    
    user = authenticate(username, password)
    if user:
        if user['is_driver']:
            subprocess.Popen(['python', 'driver_home.py', str(user['id'])])
        else:
            subprocess.Popen(['python', 'rider_home.py', str(user['id'])])
        login_window.destroy()
    else:
        messagebox.showerror("Error", "Invalid credentials")

def show_registration():
    subprocess.Popen(['python', 'registration.py'])
    login_window.destroy()

def forgot_password():
    subprocess.Popen(['python', 'forgot_password.py'])  # Make sure this script exists
    login_window.destroy()

def open_module(module_name):
    login_window.destroy()
    subprocess.Popen(['python', f'{module_name}.py'])

# Window setup
login_window = ctk.CTk()
login_window.title("Carpool Login")
login_window.geometry("400x500")
login_window.resizable(True, True)
login_window.configure(fg_color="#C9DEFF")
centre_window(login_window)

# Navigation Bar
nav_frame = ctk.CTkFrame(login_window, fg_color="#2F5B85", height=40)
nav_frame.pack(fill='x', padx=20, pady=10)

button_actions = {
    "Home": "home",
    "About Us": "about_us",
    "Help": "help",
    "Login": "login",
    "Sign-Up": "registration"
}

for text, module in button_actions.items():
    btn = ctk.CTkButton(nav_frame,
                       text=text,
                       fg_color="transparent" if text != "Login" else "#1A3A5B",
                       hover_color="#1A3A5B",
                       text_color="white",
                       font=("Arial", 14),
                       corner_radius=0,
                       command=lambda m=module: open_module(m))
    btn.pack(side='left', padx=15)

# Load logo image
try:
    logo_image = ctk.CTkImage(
        light_image=Image.open("images/logo.png"),
        size=(150, 150)
    )
except Exception as e:
    messagebox.showerror("Error", f"Failed to load logo: {str(e)}")
    logo_image = None

# Load eye icons
try:
    eye_open_icon = ctk.CTkImage(Image.open("images/eye_open.png"), size=(20, 20))
    eye_closed_icon = ctk.CTkImage(Image.open("images/eye_closed.png"), size=(20, 20))
except Exception as e:
    messagebox.showerror("Error", f"Failed to load eye icon: {str(e)}")
    eye_open_icon = None
    eye_closed_icon = None

# Style
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Wrapper to center everything
wrapper_frame = ctk.CTkFrame(login_window, fg_color="#C9DEFF")
wrapper_frame.place(relx=0.5, rely=0.5, anchor='center')

# Main container
main_frame = ctk.CTkFrame(wrapper_frame, fg_color="#C9DEFF")
main_frame.pack()

# Header section
header = ctk.CTkFrame(main_frame, fg_color="#C9DEFF")
header.pack(pady=10)

# Logo and title
ctk.CTkLabel(header, 
            text="Carpool Login", 
            font=FONTS['title'], 
            text_color="#2F5B85").pack(pady=5)

if logo_image:
    ctk.CTkLabel(header, image=logo_image, text="", fg_color="#C9DEFF").pack(pady=10)

# Form frame
form_frame = ctk.CTkFrame(main_frame, fg_color="#C9DEFF")
form_frame.pack(pady=20)

# Username
ctk.CTkLabel(form_frame, 
            text="Username:", 
            text_color="#2F5B85").pack(anchor='w')
username_entry = ctk.CTkEntry(form_frame, 
                             fg_color="white", 
                             border_color="#2F5B85", 
                             width=250)
username_entry.pack(pady=5)

# Password
ctk.CTkLabel(form_frame, 
            text="Password:", 
            text_color="#2F5B85").pack(anchor='w', pady=(10, 0))
password_entry = ctk.CTkEntry(form_frame, 
                             show="*", 
                             fg_color="white", 
                             border_color="#2F5B85", 
                             width=250)
password_entry.pack(pady=5)

# Show/hide password logic
show_password = False

def toggle_password():
    global show_password
    show_password = not show_password
    password_entry.configure(show="" if show_password else "*")
    toggle_btn.configure(image=eye_open_icon if show_password else eye_closed_icon)

# Eye button to toggle password visibility
toggle_btn = ctk.CTkButton(form_frame,
                           text="",
                           image=eye_closed_icon,
                           width=30,
                           height=30,
                           fg_color="#C9DEFF",
                           hover_color="#AECFFF",
                           command=toggle_password)
toggle_btn.place(x=220, y=109)  # Adjust `y` if form layout shifts

# Login button
login_btn = ctk.CTkButton(form_frame,
                         text="Login",
                         command=on_login,
                         fg_color="#2F5B85",
                         text_color="white",
                         hover_color="#1A3A5B",
                         width=250)
login_btn.pack(pady=20)

# Register button
ctk.CTkButton(form_frame,
             text="Register",
             command=show_registration,
             fg_color="transparent",
             text_color="#2F5B85",
             hover_color="#C9DEFF",
             width=250).pack()

# Forgot password button
ctk.CTkButton(form_frame,
             text="Forgot Password?",
             command=forgot_password,
             fg_color="transparent",
             text_color="#1A3A5B",
             hover_color="#C9DEFF",
             width=250).pack(pady=(5, 0))

login_window.mainloop()
