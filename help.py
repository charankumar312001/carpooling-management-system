import customtkinter as ctk
import tkinter as tk
import subprocess
from PIL import Image
from utils import centre_window

class HelpPage:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Help Center - Carpool")
        self.window.geometry("1000x700")
        self.window.configure(fg_color="#C9DEFF")
        centre_window(self.window)

        # Load logo
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
        self.create_help_content()
        
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
                               fg_color="transparent" if text != "Help" else "#1A3A5B",
                               hover_color="#1A3A5B",
                               text_color="white",
                               font=("Arial", 14),
                               corner_radius=0,
                               command=lambda m=module: self.open_module(m))
            btn.pack(side='left', padx=15)

    def create_help_content(self):
        main_frame = ctk.CTkScrollableFrame(self.window, fg_color="#C9DEFF")
        main_frame.pack(expand=True, fill='both', padx=40, pady=20)

        # Help title
        ctk.CTkLabel(main_frame,
                    text="Help Center",
                    font=("Arial", 24, "bold"),
                    text_color="#2F5B85").pack(pady=10, anchor='w')

        # FAQ Section
        faqs = [
            {
                "question": "How do I create an account?",
                "answer": "Click the 'Sign-Up' button in the top navigation and fill in the required information to create your account."
            },
            {
                "question": "How do I schedule a ride?",
                "answer": "After logging in, go to the 'Schedule Ride' section and enter your travel details."
            },
            {
                "question": "What safety measures are in place?",
                "answer": "We verify all users, offer ride tracking, and provide in-app emergency support."
            },
            {
                "question": "How are payments handled?",
                "answer": "Payments are processed securely through our integrated payment gateway. We never store your card details."
            }
        ]

        for faq in faqs:
            faq_frame = ctk.CTkFrame(main_frame, fg_color="#C9DEFF")
            faq_frame.pack(fill='x', pady=5)
            
            # Question button
            question_btn = ctk.CTkButton(faq_frame,
                                        text=faq["question"],
                                        font=("Arial", 14, "bold"),
                                        text_color="#2F5B85",
                                        fg_color="transparent",
                                        hover_color="#B0D0FF",
                                        anchor='w',
                                        command=lambda a=faq["answer"]: self.toggle_answer(a))
            question_btn.pack(fill='x')
            
            # Answer label (hidden initially)
            answer_label = ctk.CTkLabel(faq_frame,
                                       text=faq["answer"],
                                       font=("Arial", 13),
                                       text_color="#2F5B85",
                                       wraplength=800,
                                       justify='left')
            answer_label.pack(fill='x', padx=20)
            answer_label.pack_forget()  # Hide initially

        # Contact Section
        contact_frame = ctk.CTkFrame(main_frame, fg_color="#C9DEFF")
        contact_frame.pack(fill='x', pady=20)

        ctk.CTkLabel(contact_frame,
                    text="Need More Help?",
                    font=("Arial", 18, "bold"),
                    text_color="#2F5B85").pack(anchor='w')

        ctk.CTkLabel(contact_frame,
                    text="Contact our support team:\nEmail: support@carpoolconnect.com\nPhone: +1 (800) 123-4567",
                    font=("Arial", 14),
                    text_color="#2F5B85",
                    justify='left').pack(anchor='w', pady=10)

    def toggle_answer(self, answer_text):
        # Toggle answer visibility
        for widget in self.window.winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        for subchild in child.winfo_children():
                            if isinstance(subchild, ctk.CTkLabel) and subchild.cget("text") == answer_text:
                                if subchild.winfo_ismapped():
                                    subchild.pack_forget()
                                else:
                                    subchild.pack(fill='x', padx=20)
                                break

    def open_module(self, module_name):
        self.window.destroy()
        subprocess.Popen(['python3', f'{module_name}.py'])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = HelpPage()
    app.run()