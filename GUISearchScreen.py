# Name: Caleb Schneringer
# Date: 4/27/2026
# Program: TopTutor.py
# Description: Creates and manages the GUI for the main search screen. 
#              Also can sign people out, jump to the signed in persons profile,
#              or attempt to gain admin permission.

# ----------------- UML ------------------

import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image
from PIL import ImageTk
import json

# AI was used to help me with tough bug fixing.
# Used python librarys for methods and info of tkinter.

# ------------- Main Screen ---------------
class SearchScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(bg="black") # Configures the windows background color

        # ------------- Paths ---------------- 
        self.StudentInfo = r"D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Data\studentInfo.json"
        self.LogoutPic = r"D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Assets\LogoutPNG.png"
        self.ProfilePic = r"D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Assets\ProfilePNG.png"
        self.AdminPic = r"D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Assets\AdminPNG.png"

        # Creates a list with all the names of accounts.
        # This is used for looking up individual accounts.
        with open(self.StudentInfo, "r") as file:
            self.studentData = json.load(file)

        self.nameList = [f"{item['lastName']}, {item["firstName"]}" for item in self.studentData]

        # Layout of this tkinter window
        # x x x x x x x
        # x x x E x x x
        # x x x x x x x
        # x x x x x x x
        # x x x x x x x
        # x A x P x L x
        # x x x x x x x
        
        # Sets the Row and Column Weights
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 0)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 0)
        self.rowconfigure(6, weight = 1)

        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 0)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 0)
        self.columnconfigure(4, weight = 1)
        self.columnconfigure(5, weight = 0)
        self.columnconfigure(6, weight = 1)

        # Configures the button images
        self.logoutIMG = Image.open(self.LogoutPic)
        self.logoutIMG = self.logoutIMG.resize((100, 100))
        self.logoutLogo = ImageTk.PhotoImage(self.logoutIMG)

        self.profileIMG = Image.open(self.ProfilePic)
        self.profileIMG = self.profileIMG.resize((100, 100))
        self.profileLogo = ImageTk.PhotoImage(self.profileIMG)

        self.adminIMG = Image.open(self.AdminPic)
        self.adminIMG = self.adminIMG.resize((100, 100))
        self.adminLogo = ImageTk.PhotoImage(self.adminIMG)

        # ------------- Contents (Widgets) --------------
        self.titleLabel = tk.Label(self, text= "Top Tutor", font=("Ariel", 46, "bold"), fg="white", bg = "black")
        self.titleLabel.place(x=155,y=75)
        # Search Bar
        self.searchBar = tk.Entry(self,
                                  width= 20,
                                  font= ('Arial', 16))
        self.searchBar.grid(row=2, column=2, columnspan=3)

        self.searchBar.insert(0, 'Last, First') # Inserts the Placeholder text

        # Binds events to the Search Bar
        self.searchBar.bind("<FocusIn>", self.on_click) # Removes the Placeholder text
        self.searchBar.bind("<Return>", self.searchPerson) # Searches for the person entered
        self.searchBar.bind("<KeyRelease>", self.updateRecommendations) # every time you edit the text it updates the recommendation

        # SearchRecommendation
        self.searchrecommendation = tk.Listbox(self, 
                                               height=6,
                                               font=("Arial", 16))
        self.searchrecommendation.place(x=177,y=225)
        
        self.searchrecommendation.bind("<<ListboxSelect>>", self.selectRecommendation) # sets the event if the user clicks on a reconmmendation
        
        # Logout Button
        self.logoutButton = tk.Button(self,
                                     image = self.logoutLogo,
                                     bg='black',
                                     bd=0,
                                     activebackground='black',
                                     command= self.logout)
        self.logoutButton.grid(row=5, column= 5)


        # Profile Button
        self.profileButton = tk.Button(self, 
                                      image = self.profileLogo,
                                      bg='black',bd=0,
                                      activebackground='black',
                                      command= self.profile_clicked)
        self.profileButton.grid(row=5, column=3)


        # Admin Button
        self.adminButton = tk.Button(self, 
                                     image= self.adminLogo, 
                                     bg='black',bd=0, 
                                     activebackground='black', 
                                     command=self.askAdminPassword)
        self.adminButton.grid(row=5, column=1)




    # ----------------- Methods -------------------
    def askAdminPassword(self):
        # Name is a little missleading.
        # This function does not ask the user for a admin password, but
        # Checks the logged in accounts data to see if their isAdmin is 
        # True or False.
        with open(self.StudentInfo, "r") as file:
            data = json.load(file)

        for item in data:
            if item["ID"] == self.controller.loggedin:
                # item is the logged in account
                if item["isAdmin"] == True:
                    self.controller.show_frame("AdminPage")
                    self.ClearEntrys()
                    return
        print(self.controller.loggedin)
        messagebox.showwarning("Invalid Status","You do not have the credentials to access this.")


        # Removes the placeholder text in the entry
    def on_click(self, event):
        if self.searchBar.get() == 'Last, First':
            self.searchBar.delete(0, 'end') # deletes the placeholder text in the entry
        else: 
            return
    
        # Searches for the person entered in the searchBar
    def searchPerson(self, l, f):
         with open(self.StudentInfo, "r") as file:
            data = json.load(file)

            for item in data:
                if item['lastName'] == l:
                    if item['firstName'] == f:
                        id = item["ID"]
                        return id

            

    def logout(self):
        self.controller.show_frame("LoginPage") # Changes the page back to the login page
        self.ClearEntrys()

        # Resets who is logged in
        self.controller.set_loggedin('', '')

    def profile_clicked(self): # Sends user to logged in account's profile
        
        
        self.controller.originalUser = self.controller.loggedin
        self.controller.refresh_student_info() # Sets up the info on StudentPage

        self.controller.show_frame("StudentPage") # Changes the page to the signed in user
        self.ClearEntrys()
        

    def selectRecommendation(self, event):
        selection = self.searchrecommendation.curselection() # Checks to see if you clicked on a recommendation
        if selection:
            chosen = self.searchrecommendation.get(selection[0]) # Gets the info of your selected name

            last, first = chosen.split(',')
            last = last.strip()
            first = first.strip()
            chosenID = self.searchPerson(last, first)

            self.controller.set_loggedin(chosenID, self.controller.loggedin) # (account you are going to, account you signed in as)

            self.controller.refresh_student_info()
            self.controller.show_frame("StudentPage")
            self.ClearEntrys
             
    def updateRecommendations(self, event):
        typed = self.searchBar.get().strip().lower() # gets the contents of searchBar

        self.searchrecommendation.delete(0, tk.END) # Removes the recommendations allready in the Listbox

        if typed == "": # makes sure that searchBar isnt empty
            return

        for name in self.nameList: # Checks to see if searchBars contents is in my list of names
            if typed in name.lower():
                self.searchrecommendation.insert(tk.END, name)
    
    def ClearEntrys(self):
        self.searchBar.delete(0,"end")
        self.searchrecommendation.delete(0, tk.END)
        self.searchBar.insert(0,"Last, First")


        
        






if __name__ == "__main__":
     screen = SearchScreen()
     screen.mainloop()