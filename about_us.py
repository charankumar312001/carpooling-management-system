import customtkinter as ctk
import tkinter as tk
import subprocess
from PIL import Image
from utils import centre_window

class AboutUsPage:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("About Us - Carpool")
        self.window.geometry("1000x700")
        self.window.configure(fg_color="#C9DEFF")
        centre_window(self.window)

        # Load logo image
        try:
            self.logo_image = ctk.CTkImage(
                light_image=Image.open("images/logo.jpg"),
                size=(100, 100)
            )
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load logo: {str(e)}")
            self.logo_image = None

        self.create_header()
        self.create_navbar()
        self.create_content()
        
    def create_header(self):
        header_frame = ctk.CTkFrame(self.window, fg_color="#C9DEFF")
        header_frame.pack(pady=20)

        if self.logo_image:
            ctk.CTkLabel(header_frame, 
                        image=self.logo_image, 
                        text="").pack(side='left', padx=10)

        ctk.CTkLabel(header_frame, 
                    text="CARPOOL CONNECT", 
                    font=("Arial", 28, "bold"), 
                    text_color="#2F5B85").pack(side='left', padx=10)

    def create_navbar(self):
        nav_frame = ctk.CTkFrame(self.window, fg_color="#2F5B85", height=40)
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
                               fg_color="transparent" if text != "About Us" else "#1A3A5B",
                               hover_color="#1A3A5B",
                               text_color="white",
                               font=("Arial", 14),
                               corner_radius=0,
                               command=lambda m=module: self.open_module(m))
            btn.pack(side='left', padx=15)

    def create_content(self):
        content_frame = ctk.CTkScrollableFrame(self.window, 
                                             fg_color="#C9DEFF")
        content_frame.pack(expand=True, fill='both', padx=40, pady=20)

        # Title
        ctk.CTkLabel(content_frame,
                    text="About Our Carpool Service",
                    font=("Arial", 24, "bold"),
                    text_color="#2F5B85").pack(pady=10)

        # Divider line
        ctk.CTkFrame(content_frame, 
                    height=2, 
                    fg_color="#2F5B85").pack(fill='x', pady=10)

        # Content sections
        about_text = """
        Welcome to Carpool Connect, your reliable solution for shared commuting. 
        We are committed to reducing traffic congestion and carbon emissions 
        while making your daily commute more affordable and social.
        
        Founded in 2023, our platform connects drivers with empty seats to 
        passengers traveling in the same direction. We prioritize safety, 
        convenience, and sustainability in everything we do.
        """
        
        ctk.CTkLabel(content_frame,
                    text=about_text,
                    font=("Arial", 14),
                    text_color="#2F5B85",
                    wraplength=800).pack(pady=10, anchor='w')

        # Features section
        features = [
            ("🚗", "Easy Ride Matching", "Smart algorithm connects you with compatible commuters"),
            ("🔒", "Secure Platform", "Verified users and safety features ensure peace of mind"),
            ("🌱", "Eco-Friendly", "Reduce your carbon footprint by sharing rides"),
            ("💵", "Cost Effective", "Split travel costs with fellow commuters")
        ]

        for icon, title, desc in features:
            feature_frame = ctk.CTkFrame(content_frame, fg_color="#C9DEFF")
            feature_frame.pack(fill='x', pady=10)
            
            ctk.CTkLabel(feature_frame, 
                         text=icon,
                         font=("Arial", 24),
                         width=50).pack(side='left', padx=10)
            
            text_frame = ctk.CTkFrame(feature_frame, fg_color="#C9DEFF")
            text_frame.pack(side='left', fill='x', expand=True)
            
            ctk.CTkLabel(text_frame,
                         text=title,
                         font=("Arial", 16, "bold"),
                         text_color="#2F5B85").pack(anchor='w')
            
            ctk.CTkLabel(text_frame,
                         text=desc,
                         font=("Arial", 14),
                         text_color="#2F5B85",
                         wraplength=700).pack(anchor='w')

    def open_module(self, module_name):
        self.window.destroy()
        subprocess.Popen(['python', f'{module_name}.py'])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AboutUsPage()
    app.run()