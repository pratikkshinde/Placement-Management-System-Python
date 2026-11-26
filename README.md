# Recruitment & Placement Management System (RPMS)

## Project Overview
The Recruitment & Placement Management System (RPMS) is a Python and MySQL console-based application built for managing candidate profiles, hiring companies, job openings, eligibility checks, job applications, interviews, job offers, final placements, and summary reports.

## Technology Stack
- Python 3
- MySQL (`mysql-connector-python`)
- Object-Oriented Programming (Model, DAO, Service, ConsoleApp)
- Lists (`list[Candidate]`, `list[Job]`, `list[Application]`) and Dictionaries (`dict[str, int]`)
- Custom Exception Handling (`CandidateNotFoundError`, `JobNotFoundError`, `DuplicateApplicationError`, `CandidateNotEligibleError`)
- File Handling (`activity_log.txt`)
- Parameterized SQL Queries (`%s` placeholders)

## Project Architecture
```
Main Application (main.py -> ConsoleApp)
        |
        v
     Service (Business Rules & Validation)
        |
        v
       DAO (Database Operations)
        |
        v
  MySQL Connector (mysql-connector-python)
        |
        v
      MySQL (rpms_db)
```

## Folder Structure
```
rpms/
  model/       -> Data classes (Candidate, Company, Job, Application, Interview, InterviewFeedback, Offer, Placement)
  dao/         -> MySQL data access classes
  service/     -> Business logic and input validation
  util/        -> DB connection, activity logger, shared validation helpers
  exception/   -> Custom exception classes
  app/         -> Console menu interface
sql/
  schema.sql
  sample_data.sql
prototype/
  index.html
  styles.css
main.py
requirements.txt
```

## Project Modules
1. **Candidate Management:** Add, update, search, view all, and deactivate candidates.
2. **Company Management:** Add, update, search, and view all companies.
3. **Job Management:** Create, update, view open jobs, close jobs, and search jobs.
4. **Job Applications & Eligibility Check:** Evaluate candidate eligibility and apply without duplicates.
5. **Interview Management:** Schedule interviews and record technical/communication feedback.
6. **Offer Management:** Create job offers for selected applications and update offer status.
7. **Placement Management:** Record final joining details and mark applications as `JOINED`.
8. **Reports:** Candidates by Technology, Open Jobs, Applications by Status, Company-wise Placements, Placed Candidates, and Unplaced Candidates.

## Database Setup
1. Open MySQL Workbench (or MySQL CLI) and run `sql/schema.sql` to create the `rpms_db` database and its 8 tables (`candidates`, `companies`, `jobs`, `applications`, `interviews`, `interview_feedback`, `offers`, `placements`).
2. Optionally run `sql/sample_data.sql` to load sample records.

## Installation Instructions
1. Ensure Python 3 and MySQL Server 8.0 are installed.
2. Install the MySQL connector dependency:
   ```bash
   pip install -r requirements.txt
   ```

## Execution Instructions
1. Set your MySQL password in `rpms/util/db_connection.py` or via environment variable in PowerShell:
   ```powershell
   $env:RPMS_DB_PASSWORD = "your_mysql_password"
   ```
2. Run the console application:
   ```bash
   python main.py
   ```
