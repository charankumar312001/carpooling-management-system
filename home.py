import customtkinter as ctk
from PIL import Image
import tkinter as tk
import subprocess
from utils import centre_window

class HomePage:
    def __init__(self):
        self.home_window = ctk.CTk()
        self.home_window.title("Carpool Home")
        self.home_window.geometry("2000x700")
        self.home_window.configure(fg_color="#C9DEFF")
        centre_window(self.home_window)

        # Load image
        try:
            self.original_image = Image.open("images/home_bg.jpg")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            self.original_image = Image.new('RGB', (800, 600), color='gray')

        self.create_header()
        self.create_navbar()
        self.create_image_section()

    def create_header(self):
        header_frame = ctk.CTkFrame(self.home_window, fg_color="#C9DEFF")
        header_frame.pack(pady=20)
        ctk.CTkLabel(header_frame, 
                    text="CARPOOL CONNECT", 
                    font=("Arial", 28, "bold"), 
                    text_color="#2F5B85").pack()

    def create_navbar(self):
        nav_frame = ctk.CTkFrame(self.home_window, fg_color="#2F5B85", height=40)
        nav_frame.pack(fill='x', padx=20, pady=10)

        # Define navigation targets
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
                               fg_color="transparent",
                               hover_color="#1A3A5B",
                               text_color="white",
                               font=("Arial", 14),
                               corner_radius=0,
                               command=lambda m=module: self.open_module(m))
            btn.pack(side='left', padx=15)

    def open_module(self, module_name):
        """Close current window and open requested module"""
        self.home_window.destroy()
        subprocess.Popen(['python.exe', f'{module_name}.py'])

    #  

    def resize_image(self, event):
        # Dynamic image resizing handler
        new_width = event.width
        new_height = event.height
        
        if new_width <= 0 or new_height <= 0:
            return

        image_ratio = self.original_image.width / self.original_image.height
        frame_ratio = new_width / new_height

        if frame_ratio > image_ratio:
            resized_height = new_height
            resized_width = int(image_ratio * resized_height)
        else:
            resized_width = new_width
            resized_height = int(resized_width / image_ratio)

        resized_image = self.original_image.resize((resized_width, resized_height))
        self.image_tk = ctk.CTkImage(light_image=resized_image, size=(resized_width, resized_height))
        self.image_label.configure(image=self.image_tk)

    def create_image_section(self):
        # Image display area
        image_frame = ctk.CTkFrame(self.home_window, fg_color="#C9DEFF")
        image_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Initial image setup
        self.image_tk = ctk.CTkImage(light_image=self.original_image, 
                                   size=self.original_image.size)
        self.image_label = ctk.CTkLabel(image_frame, 
                                      image=self.image_tk, 
                                      text="")
        self.image_label.pack(expand=True, fill='both')

        # Bind resize event
        image_frame.bind("<Configure>", self.resize_image)

    def run(self):
        self.home_window.mainloop()


if __name__ == "__main__":
    app = HomePage()
    app.run()