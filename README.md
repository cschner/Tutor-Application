# Tutor Application

A full-featured desktop application built with Python and Tkinter that enables tutors to efficiently manage student information, scheduling, and user accounts. This project demonstrates proficiency in GUI development, data persistence, and user authentication systems.

## Project Overview

The Tutor Application is a complete student management system designed to streamline the administrative tasks of tutoring professionals. Built entirely in Python, this desktop application provides a secure, user-friendly interface for managing student profiles, scheduling sessions, and maintaining account credentials. All data is persisted to JSON files, ensuring information is retained between sessions.

## Key Features

### 1. **Secure Authentication System**
- Username and password-based login system
- Support for admin and regular user accounts
- Encrypted password storage in JSON format
- Form validation to prevent unauthorized access
- Session management with user ID tracking

### 2. **Student Profile Management**
- Create, view, edit, and delete student profiles
- Store comprehensive student information including:
  - Full name (first and last name)
  - Class/course information
  - Current grade level
  - Personal notes and summary documentation
  - Contact and demographic data
- Real-time data validation and error handling

### 3. **Advanced Scheduling System**
- Add, edit, and delete tutoring sessions
- Track session details:
  - Date and time of sessions
  - Assigned tutor name
  - Session notes and duration
- Interactive table-based schedule display with inline editing
- Quick add functionality for new sessions

### 4. **Search and Discovery**
- Fast student name search functionality
- Autocomplete suggestions as you type
- Real-time filtering of student database
- Navigate quickly between student records

### 5. **Admin Control Panel**
- Restricted admin-only access
- Create new student accounts with auto-generated usernames
- Reset and change existing user passwords
- Manage admin privileges
- Secure account creation workflow with confirmation dialogs

### 6. **Data Persistence**
- All information saved to JSON files
- Automatic data serialization
- Encoding support for special characters
- Structured data organization for easy parsing
- Manual save functionality with user confirmation

## Technical Architecture

### Technology Stack
- **Language:** Python 3.7+
- **GUI Framework:** Tkinter (Python's standard GUI library)
- **Data Storage:** JSON files
- **Image Processing:** Pillow (PIL)
- **Project Type:** Desktop Application

### Application Structure

The project follows an object-oriented, modular design pattern:

- **Main.py** - Application entry point; initializes the main GUI window
- **GUIMain.py** - Master controller class that manages all page navigation and inter-frame communication
- **GUILoginPage.py** - Login interface with credential verification against stored credentials
- **GUISearchScreen.py** - Student search and navigation interface
- **GUIStudentPage.py** - Student profile viewing, editing, and schedule management
- **GUIAdminPage.py** - Admin control panel for account creation and password management

### Key Design Patterns Used

1. **Model-View-Controller (MVC)** - Separation of UI (View), data logic, and application flow (Controller)
2. **Frame Stack Navigation** - Multiple Tkinter frames layered and raised based on user navigation
3. **Data Validation** - Input verification at multiple levels to ensure data integrity
4. **File I/O Management** - Robust JSON reading/writing with error handling and encoding support

## Features in Detail

### Login System (GUILoginPage.py)
- Custom-styled login form with company branding
- Background image integration
- Real-time credential validation against LoginInfo.json
- Session ID assignment upon successful authentication
- Clear error messaging for invalid credentials

### Student Management (GUIStudentPage.py)
- Display comprehensive student information with editable fields
- Inline editing for schedule entries with click-to-edit functionality
- Summary text editor for detailed student notes
- Data cleaning function to handle corrupted characters from various sources
- Automatic page refresh upon returning to student view
- Save validation to ensure all changes are persisted

### Admin Interface (GUIAdminPage.py)
- Create student accounts with auto-incremented ID generation
- Username auto-generation from student names
- Admin role assignment during account creation
- Dynamic name suggestions while typing
- Secure password change interface
- Dual-file update system (studentInfo.json and LoginInfo.json)

## How to Run

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cschner/Tutor-Application.git
   cd Tutor-Application
