# Name: Caleb Schneringer
# Date: 4/27/2026
# Program: Tutor_Application.py
# Description: This file creates all the frames and ties them together for all the GUI.
#              Main.py runs this parent class to start the program.
from logging import root
import tkinter as tk

# Imports All Frame Classes
from GUIStudentPage import StudentPage
from GUIAdminPage import AdminPage
from GUISearchScreen import SearchScreen
from GUILoginPage import LoginPage


class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Set-Up
        self.title("Top Tutor")
        self.geometry("600x600")

        
        self.loggedin = "" # Once logged in it will change to that persons name
        self.originalUser = "" 

        # Create a container frame that will hold all page frames        
        container = tk.Frame(self)
        container.grid(row = 0, column = 0, sticky = 'nsew')

        # Set the weight of each row and column
        self.rowconfigure(0, weight = 1)
        self.columnconfigure(0, weight = 1)

        container.rowconfigure(0, weight = 1)
        container.columnconfigure(0, weight = 1)
        
        # Creates all the frames and makes them findable through string.
        # When changing pages you would send "PageName" into show_frame
        self.frames = {
            "LoginPage": LoginPage(container, self),
            "SearchScreen": SearchScreen(container, self),
            "AdminPage": AdminPage(container, self),
            "StudentPage": StudentPage(container, self)
            }

        # Places the frames
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
        
       
        # Show the initial page when the app starts
        self.show_frame("LoginPage")

    # Method used to swap pages
    def show_frame(self, name):
        self.frames[name].tkraise()

    def refresh_student_info(self):
        self.frames["StudentPage"].set_Student_Info()

    def set_loggedin(self, id, og = ''):
        self.loggedin = id

        self.originalUser = og
        
        
 
















