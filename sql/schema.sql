CREATE DATABASE IF NOT EXISTS rpms_db;
USE rpms_db;

CREATE TABLE IF NOT EXISTS candidates (
    candidate_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    mobile VARCHAR(15) NOT NULL UNIQUE,
    technology VARCHAR(80) NOT NULL,
    percentage DECIMAL(5, 2) NOT NULL,
    passing_year INT NOT NULL,
    backlogs INT NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE'
);

CREATE TABLE IF NOT EXISTS companies (
    company_id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(120) NOT NULL UNIQUE,
    location VARCHAR(100) NOT NULL,
    contact_email VARCHAR(120) NOT NULL,
    hr_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(20) PRIMARY KEY,
    company_id VARCHAR(20) NOT NULL,
    job_title VARCHAR(120) NOT NULL,
    technology VARCHAR(80) NOT NULL,
    openings INT NOT NULL,
    location VARCHAR(100) NOT NULL,
    package DECIMAL(10, 2) NOT NULL,
    min_percentage DECIMAL(5, 2) NOT NULL,
    passing_year INT NOT NULL,
    max_backlogs INT NOT NULL,
    deadline DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'OPEN',
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS applications (
    application_id VARCHAR(20) PRIMARY KEY,
    candidate_id VARCHAR(20) NOT NULL,
    job_id VARCHAR(20) NOT NULL,
    applied_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'APPLIED',
    UNIQUE KEY uq_candidate_job (candidate_id, job_id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE TABLE IF NOT EXISTS interviews (
    interview_id VARCHAR(20) PRIMARY KEY,
    application_id VARCHAR(20) NOT NULL,
    candidate_id VARCHAR(20) NOT NULL,
    company_id VARCHAR(20) NOT NULL,
    round_name VARCHAR(60) NOT NULL,
    interview_date DATE NOT NULL,
    mode VARCHAR(30) NOT NULL,
    interviewer VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'SCHEDULED',
    FOREIGN KEY (application_id) REFERENCES applications(application_id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS interview_feedback (
    feedback_id VARCHAR(20) PRIMARY KEY,
    interview_id VARCHAR(20) NOT NULL UNIQUE,
    technical_rating INT NOT NULL,
    communication_rating INT NOT NULL,
    remarks VARCHAR(255),
    result VARCHAR(20) NOT NULL,
    FOREIGN KEY (interview_id) REFERENCES interviews(interview_id)
);

CREATE TABLE IF NOT EXISTS offers (
    offer_id VARCHAR(20) PRIMARY KEY,
    application_id VARCHAR(20) NOT NULL UNIQUE,
    candidate_id VARCHAR(20) NOT NULL,
    company_id VARCHAR(20) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    package DECIMAL(10, 2) NOT NULL,
    offer_date DATE NOT NULL,
    joining_date DATE NOT NULL,
    offer_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    FOREIGN KEY (application_id) REFERENCES applications(application_id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS placements (
    placement_id VARCHAR(20) PRIMARY KEY,
    offer_id VARCHAR(20) NOT NULL UNIQUE,
    application_id VARCHAR(20) NOT NULL UNIQUE,
    candidate_id VARCHAR(20) NOT NULL,
    company_id VARCHAR(20) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    final_package DECIMAL(10, 2) NOT NULL,
    actual_joining_date DATE NOT NULL,
    joining_status VARCHAR(20) NOT NULL DEFAULT 'JOINED',
    FOREIGN KEY (offer_id) REFERENCES offers(offer_id),
    FOREIGN KEY (application_id) REFERENCES applications(application_id),
    FOREIGN KEY (candidate_id) REFERENCES candidates(candidate_id),
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

