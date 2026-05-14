# Name: Caleb Schneringer
# Date: 4/27/2026
# Program: TopTutor.py
# Description: This file creates and manages the Login Page.


# ----------------- UML ------------------
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk


# ------------ Login Page -----------------
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # sets up the controller from GUIMain
        self.controller = controller
         
        # Variables
        self.TopTutorPNG = "D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Assets\TopTutorPNG.png"
        self.LoginInfo = r"D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Data\LoginInfo.json"
        self.__userEntry = ""
        self.__passEntry = ""
        

        # Configures the weight of each row/column
        self.rowconfigure(0, weight = 4)
        self.rowconfigure(1, weight = 4)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 0)
        self.rowconfigure(4, weight = 0)
        self.rowconfigure(5, weight = 0)
        self.rowconfigure(6, weight = 0)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 0)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(4, weight = 0)
        self.columnconfigure(5, weight = 1)
        self.columnconfigure(6, weight = 1)


        # ----------------- Contents (Widgets) ------------------
        # Below is a map of where the widgets are in my grid. U = username Label, P = password label.
        # E = the entrys for each of them.

        # r0 x x x x x x x 
        # r1 x x x x x x x
        # r2 x x U x P x x
        # r3 x x E x E x x
        # r4 x x x x x x x 
        # r5 x x x x x x x
        # r6 x x x x x x x

        
        self.passwordLabel = tk.Label(self, text = "PASSWORD", bg = '#3D3635', fg = 'white')
        self.passwordLabel.grid(column = 4, row = 2)

        self.usernameLabel = tk.Label(self, text = "USERNAME", bg = '#3D3635', fg = 'white')
        self.usernameLabel.grid(column = 2, row = 2)

        self.passwordEntry = tk.Entry(self, show="*")
        self.passwordEntry.grid(column=4, row=3, pady = 10, padx = 10)

        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid(column = 2, row = 3, pady = 10, padx = 10)

        self.verifyButton = tk.Button(self, text = "Enter", command = self.Enter_Button_Clicked)
        self.verifyButton.grid(column = 2, row = 4, sticky= "we", pady = 10, padx = 10, columnspan= 3)

        # Binds the Return key to run Enter_Button_Clicked function
        self.usernameEntry.bind("<Return>", self.Enter_Button_Clicked)
        self.passwordEntry.bind("<Return>", self.Enter_Button_Clicked)

         
        

        # Sets and configure the logo
        self.logoFrame = tk.Frame(self)
        self.logoFrame.place(x=0, y=0, relwidth=1, relheight=1)
        self.logoFrame.lower()

        self.img = Image.open(self.TopTutorPNG)
        self.img = self.img.resize((600, 600))
        self.logo = ImageTk.PhotoImage(self.img)

        self.logoLabel = tk.Label(self.logoFrame, image = self.logo)
        self.logoLabel.place(x= 0, y= 0, relwidth=1, relheight=1)

        # Sets and configures the images for the labels of Username and Password.
        
        


    # ---------------- Methods -----------------
    def Get_Username(self):
        contents = self.usernameEntry.get()
        self.__userEntry = contents

    def Get_Password(self):
        contents = self.passwordEntry.get()
        self.__passEntry = contents

        # I have event equal to None becasue without it, and you dont use the return key, there 
        # is an error.
    def Enter_Button_Clicked(self, event = None): 
        # If username and passsword match in files:
        
        # Pulls the contents from the Entrys
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        with open(self.LoginInfo, "r", encoding="utf-8") as file:
            data = json.load(file)
      
            for user in data:
                
                if username == user["username"]:
                    
                    if password == user["password"]:
                        
                        # User found: Will login as them and delete the contents of the 
                        # Entrys.
                        studentID = user["ID"]
                        self.controller.set_loggedin(studentID)
                        
                        self.controller.refresh_student_info()
                        self.controller.show_frame("SearchScreen")
                        self.usernameEntry.delete(0,'end')
                        self.passwordEntry.delete(0,'end')
                        return

            # Will run if user entered incorrect Username/Password.
            messagebox.showwarning("Invalid Username/Password", "You have entered an invalid Username or Password.")
             



        
        

   




if __name__ == "__main__":
     screen = LoginPage()
     screen.mainloop()