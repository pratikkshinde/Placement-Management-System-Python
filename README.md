# Recruitment & Placement Management System (RPMS)

A Python and MySQL console application built using OOP, DAO-Service architecture, exception handling, lists/dictionaries, and file logging.

## Technologies Used
- Python 3
- MySQL (`mysql-connector-python`)
- OOP (Model, DAO, Service, App)
- Lists (`list[Candidate]`, `list[Job]`, `list[Application]`) and Dictionaries (`dict[str, int]`)
- Exception Handling (`CandidateNotFoundError`, `JobNotFoundError`, `DuplicateApplicationError`, `CandidateNotEligibleError`)
- File Handling (`activity_log.txt`)
- Parameterized SQL Queries

## Architecture
```
Main Application (Console Menu)
        |
        v
     Service (Business Logic)
        |
        v
       DAO (Database Operations)
        |
        v
  MySQL Connector
        |
        v
      MySQL
```

## Folder Structure
```
rpms/
  model/
  dao/
  service/
  util/
  exception/
  app/
main.py
requirements.txt
sql/
prototype/
```

## How to Setup and Run

1. Install MySQL connector:
   ```bash
   pip install -r requirements.txt
   ```

2. Run `sql/schema.sql` and `sql/sample_data.sql` in MySQL Workbench to create `rpms_db`, all 8 tables, and sample records.

3. Set your MySQL password in `rpms/util/db_connection.py` (or set `RPMS_DB_PASSWORD` in PowerShell):
   ```powershell
   $env:RPMS_DB_PASSWORD = "your_password"
   ```

4. Start the console application:
   ```bash
   python main.py
   ```
