# Name: Caleb Schneringer
# Date: 4/27/2026
# Program: TopTutor.py
# Description: Admin page for creating accounts + changing passwords

import tkinter as tk
import json
from tkinter import messagebox


class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(bg="grey")
        self.place(width=600, height=600)

        # File paths
        self.studentFile = r"D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Data\studentInfo.json"
        self.loginFile   = r"D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Data\LoginInfo.json"

        self.selectedID = None  # ID of selected student for password change

        # ------------------ Title ------------------
        tk.Label(self, text="Admin Panel", font=("Ariel", 28), bg="grey").place(x=180, y=20)

        # ------------------ Create Account Section ------------------
        tk.Label(self, text="Create Student Account", font=("Ariel", 20), bg="grey").place(x=160, y=80)

        tk.Label(self, text="First Name:", font=("Ariel", 16), bg="grey").place(x=50, y=130)
        self.firstEntry = tk.Entry(self, font=("Ariel", 14), width=20)
        self.firstEntry.place(x=200, y=130)

        tk.Label(self, text="Last Name:", font=("Ariel", 16), bg="grey").place(x=50, y=170)
        self.lastEntry = tk.Entry(self, font=("Ariel", 14), width=20)
        self.lastEntry.place(x=200, y=170)

        tk.Label(self, text="Class:", font=("Ariel", 16), bg="grey").place(x=50, y=210)
        self.classEntry = tk.Entry(self, font=("Ariel", 14), width=20)
        self.classEntry.place(x=200, y=210)

        tk.Label(self, text="Grade:", font=("Ariel", 16), bg="grey").place(x=50, y=250)
        self.gradeEntry = tk.Entry(self, font=("Ariel", 14), width=20)
        self.gradeEntry.place(x=200, y=250)

        tk.Label(self, text="Password:", font=("Ariel", 16), bg="grey").place(x=50, y=290)
        self.newPassEntry = tk.Entry(self, font=("Ariel", 14), width=20, show="*")
        self.newPassEntry.place(x=200, y=290)

        tk.Button(self, text="Create Student Account", font=("Ariel", 16),
                  bg="green", command=self.createStudent).place(x=190, y=330)

        # ------------------ Change Password Section ------------------
        tk.Label(self, text="Change Existing Password", font=("Ariel", 20), bg="grey").place(x=150, y=380)

        tk.Label(self, text="Lookup Name:", font=("Ariel", 16), bg="grey").place(x=50, y=430)
        self.lookupEntry = tk.Entry(self, font=("Ariel", 14), width=25)
        self.lookupEntry.place(x=200, y=430)
        self.lookupEntry.bind("<KeyRelease>", self.updateSuggestions)

        # Listbox for name suggestions
        self.suggestionBox = tk.Listbox(self, width=25, height=4)
        self.suggestionBox.place(x=200, y=460)
        self.suggestionBox.bind("<<ListboxSelect>>", self.selectSuggestion)

        tk.Label(self, text="New Password:", font=("Ariel", 16), bg="grey").place(x=50, y=510)
        self.changePassEntry = tk.Entry(self, font=("Ariel", 14), width=25, show="*")
        self.changePassEntry.place(x=200, y=510)

        tk.Button(self, text="Apply Password", font=("Ariel", 16),
                  bg="green", command=self.applyPassword).place(x=200, y=540)

        # Back button
        tk.Button(self, text="Back", font=("Ariel", 16), bg="red",
                  command=self.backClicked).place(x=10, y=10)

    # ------------------ Create Student ------------------
    def createStudent(self):
        # Get input values
        first = self.firstEntry.get().strip()
        last  = self.lastEntry.get().strip()
        cls   = self.classEntry.get().strip()
        grade = self.gradeEntry.get().strip()
        pwd   = self.newPassEntry.get().strip()

        # Basic validation
        if not first or not last or not pwd:
            messagebox.showerror("Error", "Missing required fields")
            return

        # Ask if admin
        is_admin = messagebox.askyesno("Admin?", "Should this student be an admin?")

        # Load JSON files
        with open(self.studentFile, "r") as f:
            students = json.load(f)
        with open(self.loginFile, "r") as f:
            logins = json.load(f)

        # Generate new ID
        if len(students) == 0:
            new_id = "001"
        else:
            new_id = str(max(int(s["ID"]) for s in students) + 1).zfill(3)

        # Create username
        username = first[0].lower() + last.lower()

        # Add student record
        students.append({
            "ID": new_id,
            "firstName": first,
            "lastName": last,
            "isAdmin": is_admin,
            "class": cls,
            "grade": grade,
            "summary": "",
            "schedule": []
        })

        # Add login record
        logins.append({
            "ID": new_id,
            "username": username,
            "password": pwd
        })

        # Save files
        with open(self.studentFile, "w") as f:
            json.dump(students, f, indent=4)
        with open(self.loginFile, "w") as f:
            json.dump(logins, f, indent=4)

        messagebox.showinfo("Success", "Student account created")

    # ------------------ Suggestions ------------------
    def updateSuggestions(self, event):
        # Update name suggestions as user types
        text = self.lookupEntry.get().lower()
        self.suggestionBox.delete(0, tk.END)

        if not text:
            return

        with open(self.studentFile, "r") as f:
            data = json.load(f)

        # Add matching names
        for s in data:
            full = s["firstName"] + " " + s["lastName"]
            if text in full.lower():
                self.suggestionBox.insert(tk.END, full)

    def selectSuggestion(self, event):
        # When user clicks a suggestion
        if not self.suggestionBox.curselection():
            return

        name = self.suggestionBox.get(self.suggestionBox.curselection())
        self.lookupEntry.delete(0, tk.END)
        self.lookupEntry.insert(0, name)

        # Find selected student's ID
        with open(self.studentFile, "r") as f:
            data = json.load(f)

        for s in data:
            if s["firstName"] + " " + s["lastName"] == name:
                self.selectedID = s["ID"]
                break

    # ------------------ Apply Password ------------------
    def applyPassword(self):
        # Ensure a student is selected
        if not self.selectedID:
            messagebox.showerror("Error", "No student selected")
            return

        new_pass = self.changePassEntry.get().strip()
        if not new_pass:
            messagebox.showerror("Error", "Password cannot be empty")
            return

        # Load files
        with open(self.studentFile, "r") as f:
            students = json.load(f)
        with open(self.loginFile, "r") as f:
            logins = json.load(f)

        # Update student password (if stored here)
        for s in students:
            if s["ID"] == self.selectedID:
                s["password"] = new_pass
                break

        # Update login password
        for l in logins:
            if l["ID"] == self.selectedID:
                l["password"] = new_pass
                break

        # Save files
        with open(self.studentFile, "w") as f:
            json.dump(students, f, indent=4)
        with open(self.loginFile, "w") as f:
            json.dump(logins, f, indent=4)

        messagebox.showinfo("Success", "Password updated")

    # ------------------ Clear All Entry Boxes ------------------
    def clearEntrys(self):
        # Clear all input fields
        self.firstEntry.delete(0, 'end')
        self.lastEntry.delete(0, 'end')
        self.classEntry.delete(0, 'end')
        self.gradeEntry.delete(0, 'end')
        self.newPassEntry.delete(0, 'end')
        self.lookupEntry.delete(0, 'end')
        self.changePassEntry.delete(0, 'end')

    # ------------------ Back Button ------------------
    def backClicked(self):
        # Return to search screen + clear fields
        self.controller.show_frame("SearchScreen")
        self.clearEntrys()
