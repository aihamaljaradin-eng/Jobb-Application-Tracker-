# Job Application Tracker

A terminal-based job application tracker built with Python and MySQL that helps users manage applications, track statuses, and monitor interview progress.

## Project Overview
The Job Application Tracker is designed for job seekers who apply to multiple positions at the same time and need a structured way to organize their applications. The system stores important information such as company details, deadlines, interview dates, and application status, making it easier to manage the job search process.

## Features
- Add new job applications
- View stored applications
- Update the status of an application
- Remove applications that are no longer relevant
- Track interview dates and deadlines
- Manage company and user-related application data

## Tech Stack
- Python
- MySQL
- SQL

## Database Design
The system is based on a relational database with the following main entities:
- User
- Company
- Status
- JobApplication

Relationships:
- One user can have many job applications
- One company can be linked to many job applications
- One status can be linked to many job applications

## How to Run
1. Clone the repository
2. Install dependencies
3. Create the database in MySQL
4. Run the SQL schema file
5. Insert sample data
6. Configure the `.env` file with your database credentials
7. Run the Python application

## Future Improvements
- Add a graphical user interface
- Add search and filter options
- Add email reminders for deadlines and interviews
- Add data visualization for application progress

## Developers
- Aiham Aljaradin
- Suheyb Hashi
