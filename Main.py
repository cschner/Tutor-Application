# Name: Caleb Schneringer
# Date: 4/17/2026
# Program: TopTutor.py
# Description: Program to help Tutors keep track of scheduling and student information.
#              It has securtiy of passcodes and a searchbar to help find students.
#              Admins can create new student accounts, and change existing passwords.
#              All information is saved in a json file, and is saved with a button.

from GUIMain import MainGUI


if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()

        