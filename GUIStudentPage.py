# Name: Caleb Schneringer
# Date: 4/27/2026
# Program: TopTutor.py
# Description: Student info GUI + schedule editing. 
#              This file deals with everything involving the student
#              page, and resets for it.

import tkinter as tk
from tkinter import ttk, simpledialog
import json


class StudentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.configure(bg="grey")
        self.StudentInfo = r"D:\Projects\Python\SFCC\Tutor_Application\Tutor_Application\Data\studentInfo.json"
        # Vars for student info
        self.name_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.grade_var = tk.StringVar()
        self.summary_var = tk.StringVar()

        # Load student data
        self.set_Student_Info()

        # Grid weights for layout
        for r in range(7):
            self.rowconfigure(r, weight=1)
        for c in range(7):
            self.columnconfigure(c, weight=1 if c < 2 else 0)

        # Top buttons
        tk.Button(self, text="Back", font=("Ariel", 16), bg='red',
                  command=self.backClicked).place(x=520, y=20)

        tk.Button(self, text="Save", font=("Ariel", 16), bg='green',
                  command=self.saveClicked).place(x=440, y=20)

        tk.Button(self, text="Edit", font=("Ariel", 16),
                  command=self.editClicked).place(x=380, y=20)

        tk.Button(self, text='Add', font=("Ariel", 16),
                  command=self.add_to_Schedule).place(x=10, y=430)

        # Displayed labels
        tk.Label(self, textvariable=self.name_var, bg="grey",
                 font=("Ariel", 32)).place(x=10, y=10)

        tk.Label(self, textvariable=self.class_var, bg="grey",
                 font=("Ariel", 16)).place(x=10, y=300)

        tk.Label(self, textvariable=self.grade_var, bg="grey",
                 font=("Ariel", 16)).place(x=10, y=340)

        # Summary text box
        self.summaryText = tk.Text(self, width=42, height=9, font=("Ariel", 8))
        self.summaryText.place(x=300, y=340)

        tk.Label(self, text="Summary", bg="grey",
                 font=("Ariel", 16)).place(x=300, y=300)

    # ---------------- CLEAN FUNCTION ----------------
    def clean(self, s):
        # Fix corrupted dash characters
        if not isinstance(s, str):
            return s
        return (
            s.replace("â€“", "-")
             .replace("–", "-")
             .replace("—", "-")
             .replace("−", "-")
             .replace("‑", "-")
        )

    # ---------------- Schedule Table ----------------
    def ShowSchedule(self):
        # Build schedule table frame
        self.tableFrame = tk.Frame(self, bg="grey")
        self.tableFrame.grid(row=6, column=0, padx=10, pady=10,
                             sticky="sew", columnspan=4)
        self.tableFrame.grid_propagate(False)

        # Scrollbar
        scroll = tk.Scrollbar(self.tableFrame)
        scroll.pack(side="right", fill="y")

        # Treeview setup
        self.scheduleTable = ttk.Treeview(
            self.tableFrame,
            columns=("date", "time", "tutor", "delete"),
            show="headings",
            height=4,
            yscrollcommand=scroll.set
        )

        # Column headers
        self.scheduleTable.heading("date", text="Date")
        self.scheduleTable.heading("time", text="Time")
        self.scheduleTable.heading("tutor", text="Tutor")
        self.scheduleTable.heading("delete", text="Delete")

        # Column widths
        self.scheduleTable.column("date", width=100)
        self.scheduleTable.column("time", width=150)
        self.scheduleTable.column("tutor", width=200)
        self.scheduleTable.column("delete", width=80, anchor="center")

        self.scheduleTable.pack(fill="both", expand=True)
        scroll.config(command=self.scheduleTable.yview)

        # Insert schedule rows
        for row in self.schedule:
            clean_row = (
                self.clean(row[0]),
                self.clean(row[1]),
                self.clean(row[2]),
                row[3]
            )
            self.scheduleTable.insert("", "end", values=clean_row)

        # Enable clicking to edit
        self.scheduleTable.bind("<Button-1>", self.start_edit)

    def start_edit(self, event):
        # Detect clicked row/column
        row_id = self.scheduleTable.identify_row(event.y)
        col = self.scheduleTable.identify_column(event.x)

        if not row_id or col == "#0":
            return

        # Delete column clicked
        if col == "#4":
            self.scheduleTable.delete(row_id)
            return

        # Get cell position + value
        x, y, width, height = self.scheduleTable.bbox(row_id, col)
        column_id = self.scheduleTable["columns"][int(col[1:]) - 1]
        current_value = self.scheduleTable.set(row_id, column_id)

        # Create entry box over cell
        self.editBox = tk.Entry(self.tableFrame)
        self.editBox.place(x=x, y=y, width=width, height=height)
        self.editBox.insert(0, current_value)
        self.editBox.focus()

        # Save on Enter or losing focus
        self.editBox.bind("<Return>", lambda e: self.save_edit(row_id, column_id))
        self.editBox.bind("<FocusOut>", lambda e: self.save_edit(row_id, column_id))

    def save_edit(self, row_id, column_id):
        # Save edited value back into table
        try:
            new_value = self.clean(self.editBox.get())
            self.scheduleTable.set(row_id, column_id, new_value)
            self.editBox.destroy()
        except:
            print("edit failed")

    def add_to_Schedule(self):
        # Ask user for new schedule row
        date = simpledialog.askstring("Date", "Enter the Date (m/d/y)")
        time = simpledialog.askstring("Time", "Enter the Time (#:##AM-#:##AM)")
        tutor = simpledialog.askstring("Tutor", "Enter the Tutor's Name")

        # Clean inputs
        
        date = self.clean(date)
        time = self.clean(time)
        tutor = self.clean(tutor)

        # Insert into table
        dateStatus = False
        timeStatus = False
        tutorStatus = False

        if date and time and tutor:
            self.scheduleTable.insert("", "end", values=(date, time, tutor, "X"))
            return
        if date:
            dateStatus = True
        if time:
            timeStatus = True
        if tutor:
            tutorStatus = True

        values = (
            date if dateStatus else "Error",
            time if timeStatus else "Error",
            tutor if tutorStatus else "Error",
            "X"
        )

        self.scheduleTable.insert("", "end", values=(values))


    # ---------------- Navigation ----------------
    def backClicked(self):
        # Return to search screen
        self.controller.set_loggedin(self.controller.originalUser)
        self.controller.show_frame('SearchScreen')
        self.summaryText.delete("1.0",tk.END)

    # ---------------- Save Logic ----------------
    def saveClicked(self):
        # Save all student info + schedule to JSON

        # Load JSON file
        try:
            with open(self.StudentInfo,
                      "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            print("Error loading JSON:", e)
            return

        student_found = False

        # Find matching student
        for student in data:
            if str(student.get("ID")) == str(self.user):
                student_found = True

                # Save name
                full_name = self.studentName.get().strip()
                parts = full_name.split(" ", 1)
                first_name = parts[0]
                last_name = parts[1] if len(parts) == 2 else ""

                student["firstName"] = first_name
                student["lastName"] = last_name

                # Save class + grade
                student["class"] = self.studentClass.get()
                student["grade"] = self.studentGrade.get()

                # Save summary text
                student["summary"] = self.summaryText.get("1.0", "end-1c")

                # Save schedule rows
                new_schedule = []
                for row_id in self.scheduleTable.get_children():
                    row = self.scheduleTable.item(row_id)["values"]
                    new_schedule.append([
                        self.clean(row[0]),
                        self.clean(row[1]),
                        self.clean(row[2]),
                        row[3]
                    ])

                student["schedule"] = new_schedule
                print("<Save Complete>")
                break

        if not student_found:
            print("No matching student ID")
            return

        # Write JSON file
        try:
            with open(self.StudentInfo,
                      "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print("Error writing JSON:", e)
            return

        # Reload page
        self.set_Student_Info()
        

    # ---------------- Edit Logic ----------------
    def editClicked(self):
        # Quick edit popup for name/class/grade
        Name = simpledialog.askstring("Name", "Enter Student Name.")
        Class = simpledialog.askstring("Class", "Enter Student Class.")
        Grade = simpledialog.askstring("Grade", "Enter Student Grade.")

        # Makes sure that the askstrings are set to a string not None or empty
        if Name:
            self.name_var.set(Name)
        if Class:
            self.class_var.set(Class)
        if Grade:
            self.grade_var.set(Grade)

    # ---------------- Load Student Info ----------------
    def set_Student_Info(self):
        # Load student info from JSON
        
        self.user = self.controller.loggedin

        with open(self.StudentInfo,
                  "r", encoding="utf-8") as file:
            self.studentData = json.load(file)

        for item in self.studentData:
            if str(item["ID"]) == str(self.user):

                self.info = dict(item)

                # Set displayed vars
                full_name = f"{self.info['firstName']} {self.info['lastName']}"
                self.name_var.set(full_name)
                self.class_var.set(self.info["class"])
                self.grade_var.set(self.info["grade"])
                self.summary_var.set(self.info["summary"])

                

                # Clean schedule rows
                cleaned = []
                for row in self.info["schedule"]:
                    cleaned.append((
                        self.clean(row[0]),
                        self.clean(row[1]),
                        self.clean(row[2]),
                        row[3]
                    ))
                self.schedule = cleaned

                # Store references
                self.studentName = self.name_var
                self.studentClass = self.class_var
                self.studentGrade = self.grade_var
                self.studentSummary = self.summary_var

                # Build schedule table
                self.ShowSchedule()

                # Load summary text if empty
                if self.summaryText.get("1.0", "end-1c") == "":
                    self.summaryText.insert("1.0", self.summary_var.get())

                break
