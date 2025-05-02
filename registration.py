import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import subprocess
from utils import DBAccess, resize_image, centre_window
from constants import COLORS, FONTS

def register_user():
    username = entries['username'].get().strip()
    password = entries['password'].get().strip()
    email = entries['email'].get().strip()
    first_name = entries['first_name'].get().strip()
    last_name = entries['last_name'].get().strip()
    phone = entries['phone'].get().strip()
    is_driver = driver_var.get()

    if not all([username, password, email, first_name, last_name, phone]):
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        result = DBAccess.execute_update(
            """INSERT INTO users (username, password, email, first_name, last_name, phone, is_driver)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (username, password, email, first_name, last_name, phone, is_driver)
        )
        
        if result:
            messagebox.showinfo("Success", "Registration successful!")
            subprocess.Popen(['python.exe', 'login.py'])
            window.destroy()
    except Exception as e:
        messagebox.showerror("Error", f"Registration failed: {str(e)}")

def back_to_login():
    subprocess.Popen(['python.exe', 'login.py'])
    window.destroy()

def open_module(module_name):
    window.destroy()
    subprocess.Popen(['python.exe', f'{module_name}.py'])

# Window setup
window = ctk.CTk()
window.title("Registration")
window.geometry("500x600")
window.resizable(True, True)
window.configure(fg_color="#C9DEFF")
centre_window(window)

# Navigation Bar
nav_frame = ctk.CTkFrame(window, fg_color="#2F5B85", height=40)
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
                       fg_color="transparent" if text != "Sign-Up" else "#1A3A5B",
                       hover_color="#1A3A5B",
                       text_color="white",
                       font=("Arial", 14),
                       corner_radius=0,
                       command=lambda m=module: open_module(m))
    btn.pack(side='left', padx=15)

# Style configuration
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Centering wrapper
wrapper_frame = ctk.CTkFrame(window, fg_color="#C9DEFF")
wrapper_frame.place(relx=0.5, rely=0.5, anchor="center")

# Main container
main_frame = ctk.CTkFrame(wrapper_frame, fg_color="#C9DEFF")
main_frame.pack()

# ---------- Header Bar ----------
header_frame = ctk.CTkFrame(main_frame, fg_color="#305C86", corner_radius=8)
header_frame.pack(fill='x', pady=(0, 20))

ctk.CTkLabel(header_frame, 
             text="Registration", 
             font=FONTS['title'], 
             text_color="white").pack(pady=10)
# -------------------------------

# Fields
fields = [
    ("Username", 'username'),
    ("Password", 'password'),
    ("Email", 'email'),
    ("First Name", 'first_name'),
    ("Last Name", 'last_name'),
    ("Phone", 'phone')
]

entries = {}
for label, name in fields:
    ctk.CTkLabel(main_frame, text=label + ":", text_color="#2F5B85").pack(anchor='w', padx=10, pady=(5, 0))
    entry = ctk.CTkEntry(main_frame, 
                         show='*' if 'password' in name else '', 
                         fg_color="white", 
                         border_color="#2F5B85", 
                         width=300)
    entry.pack(padx=10, pady=5)
    entries[name] = entry

# Driver checkbox
driver_var = ctk.BooleanVar()
ctk.CTkCheckBox(main_frame, 
                text="Register as Driver", 
                variable=driver_var,
                text_color="#2F5B85").pack(pady=10)

# Buttons
ctk.CTkButton(main_frame, 
              text="Register", 
              command=register_user,
              fg_color="#2F5B85", 
              hover_color="#1A3A5B", 
              text_color="white", 
              width=300).pack(pady=10)

ctk.CTkButton(main_frame, 
              text="Back to Login", 
              command=back_to_login, 
              fg_color="transparent", 
              text_color="#2F5B85", 
              hover_color="#C9DEFF", 
              width=300).pack()

window.mainloop()