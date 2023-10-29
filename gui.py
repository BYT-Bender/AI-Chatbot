# Copyright © 2023 BYT-Bender

# Import necessary modules
import json
import tkinter as tk
import customtkinter

# Import classes and functions from custom modules
from assets.utilities import Utility
from chatbot import Chatbot
from assets.admin_commands import AdminCommands
from assets.analize import Graph

# Set the appearance mode and default color theme
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


# Create the main application class
class App(customtkinter.CTk):
    def __init__(self, config):
        super().__init__()

        # Create an instance of the Chatbot class
        self.config = config
        self.chatbot = Chatbot(self.config)
        self.admin_commands = AdminCommands(self.config)
        self.graph = Graph(self.config)

        # Configure the main application window
        self.title("Chatbot")
        self.geometry(f"{1100}x{580}")

        # Configure the grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # Create the sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Chatbot", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,text="Reload",command= lambda: self.admin_commands.reload_chatbot(all=True))
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Analize", command=self.graph.main)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # Create the main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Send a message")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, text="Send", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.send_message)
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # Create the textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250, font=("Arial", 14))
        self.textbox.grid(row=0, column=1, rowspan=3, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # Set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.configure(state="disabled")
        self.entry.bind("<Return>", self.send_message)

    # Event handler to change the appearance mode
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    # Event handler to change UI scaling
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    # Event handler to send a user message
    def send_message(self, event=None):
        user_message = self.entry.get()
        if user_message:
            self.display_message("You: " + user_message)
            bot_response = self.chatbot.generate_response(user_message)
            self.display_message("Chatbot: " + bot_response + "\n")
            self.entry.delete(0, tk.END)

    # Display a message in the chatbox
    def display_message(self, message):
        self.textbox.configure(state="normal")
        self.textbox.insert(tk.END, message + "\n")
        self.textbox.configure(state="disabled")
        self.textbox.see(tk.END)


# Function to load the configuration from a JSON file
def load_config(config_file):
    try:
        with open(config_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"Config file '{config_file}' not found.")
    except Exception as error:
        raise Exception(f"Error loading configuration: {error}")


if __name__ == "__main__":
    try:
        config_file = "config.json"
        config = load_config(config_file)
        config["log_file"] = config["log_files"]["app"]

        utility = Utility(config)
        utility.log_action("Status change detected: running")
        utility.log_action(f"Loaded Chatbot with configuration: {config}")

        app = App(config)
        app.mainloop()

        utility.exit()

    except FileNotFoundError:
        utility.handle_file_not_found_error("Config", config_file)
    except Exception as error:
        utility.handle_error("booting", error)
