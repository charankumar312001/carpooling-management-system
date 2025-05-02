import customtkinter as ctk
from tkinter import messagebox
import subprocess
from utils import DBAccess, centre_window
from constants import COLORS, FONTS

# Window setup
forgot_window = ctk.CTk()
forgot_window.title("Forgot Password")
forgot_window.geometry("450x400")
forgot_window.resizable(True, True)
forgot_window.configure(fg_color="#C9DEFF")
centre_window(forgot_window)

# Navigation Bar
nav_frame = ctk.CTkFrame(forgot_window, fg_color="#2F5B85", height=40)
nav_frame.pack(fill='x', padx=20, pady=10)

button_actions = {
    "Home": "home",
    "About Us": "about_us",
    "Help": "help",
    "Login": "login",
    "Sign-Up": "registration"
}

def open_module(module_name):
    forgot_window.destroy()
    subprocess.Popen(['python', f'{module_name}.py'])

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

# State variable to track current step
email_verified = [False]

# Callback Functions
def validate_email():
    email = email_entry.get().strip()
    result = DBAccess.execute_query("SELECT * FROM users WHERE email = %s", (email,))
    
    if result:
        email_verified[0] = True
        email_entry.configure(state="disabled")
        next_button.configure(state="disabled")
        password_section()
    else:
        messagebox.showerror("Error", "Email not found!")

def update_password():
    email = email_entry.get().strip()
    new_pwd = new_pwd_entry.get()
    confirm_pwd = confirm_pwd_entry.get()

    if new_pwd != confirm_pwd:
        messagebox.showerror("Error", "Passwords do not match.")
        return
    if len(new_pwd) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters.")
        return
    if not any(c.isdigit() for c in new_pwd):
        messagebox.showerror("Error", "Password must contain at least one digit.")
        return
    if not any(c.isupper() for c in new_pwd):
        messagebox.showerror("Error", "Password must contain an uppercase letter.")
        return
    if not any(c in "!@#$%^&*()_+-=" for c in new_pwd):
        messagebox.showerror("Error", "Password must contain a special character.")
        return

    try:
        rows_updated = DBAccess.execute_update("UPDATE users SET password = %s WHERE email = %s", (new_pwd, email))
        if rows_updated:
            messagebox.showinfo("Success", "Password changed successfully!")
            forgot_window.destroy()
            subprocess.Popen(['python', 'login.py'])
        else:
            messagebox.showerror("Error", "Failed to update password.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Wrapper
wrapper_frame = ctk.CTkFrame(forgot_window, fg_color="#C9DEFF")
wrapper_frame.place(relx=0.5, rely=0.5, anchor='center')

# Main Frame
main_frame = ctk.CTkFrame(wrapper_frame, fg_color="#C9DEFF")
main_frame.pack()

# Header
ctk.CTkLabel(main_frame, 
             text="Forgot Password", 
             font=FONTS['title'], 
             text_color="#2F5B85").pack(pady=10)

# Email Frame
email_frame = ctk.CTkFrame(main_frame, fg_color="#C9DEFF")
email_frame.pack(pady=10)

ctk.CTkLabel(email_frame, 
             text="Enter Your Email:", 
             text_color="#2F5B85").pack(anchor='w')

email_entry = ctk.CTkEntry(email_frame, 
                            fg_color="white", 
                            border_color="#2F5B85", 
                            width=300)
email_entry.pack(pady=5)

next_button = ctk.CTkButton(email_frame, 
                            text="Next", 
                            command=validate_email,
                            fg_color="#2F5B85", 
                            text_color="white", 
                            hover_color="#1A3A5B", 
                            width=300)
next_button.pack(pady=10)

# Password Frame (initially hidden)
def password_section():
    password_frame = ctk.CTkFrame(main_frame, fg_color="#C9DEFF")
    password_frame.pack(pady=20)

    # New password
    ctk.CTkLabel(password_frame, 
                 text="New Password:", 
                 text_color="#2F5B85").pack(anchor='w')
    global new_pwd_entry
    new_pwd_entry = ctk.CTkEntry(password_frame, 
                                 show="*", 
                                 fg_color="white", 
                                 border_color="#2F5B85", 
                                 width=300)
    new_pwd_entry.pack(pady=5)

    # Confirm password
    ctk.CTkLabel(password_frame, 
                 text="Confirm Password:", 
                 text_color="#2F5B85").pack(anchor='w', pady=(10, 0))
    global confirm_pwd_entry
    confirm_pwd_entry = ctk.CTkEntry(password_frame, 
                                     show="*", 
                                     fg_color="white", 
                                     border_color="#2F5B85", 
                                     width=300)
    confirm_pwd_entry.pack(pady=5)

    # Update button
    ctk.CTkButton(password_frame, 
                  text="Update Password", 
                  command=update_password, 
                  fg_color="#2F5B85", 
                  text_color="white", 
                  hover_color="#1A3A5B", 
                  width=300).pack(pady=15)

forgot_window.mainloop()
