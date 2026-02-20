# Fake-docters
MedFlow – Patient Management System
A simple hospital patient management system built with Flask, SQLAlchemy, and JavaScript.

This system allows hospital staff to:
-Register and manage users
-Add new patients
-Edit patient records
-Update patient treatment status
-View dashboard statistics
-Track patient triage color levels

🚀 Features
🔐 Authentication

Admin and Staff roles
Secure password hashing
Session-based login system

👤 Patient Management

Add new patients
Edit patient information
Search by:
-Patient ID (HN)
-First Name
-Surname

Store:

-General info
-Medical info 
-status & triage

📊 Dashboard
Top stats;
 Total Patients
 Waiting Patients
 Completed Patients

Triage color statistics:
 White
 Green
 Yellow
 Red 
 Black

🔄 Status Tracking

Patients can be updated to:
-Waiting
-Completed

Dashboard updates automatically after status change.

>> Default Admin Account
Username: admin
Password: admin123

🗄 Database

SQLite database file: patients.db
Automatically created on first run
