USE rpms_db;

INSERT IGNORE INTO companies (company_id, name, location, contact_email, hr_name) VALUES
('CMP101', 'TCS', 'Pune', 'hr.pune@tcs.com', 'Sneha Kulkarni'),
('CMP102', 'Infosys', 'Bengaluru', 'careers@infosys.com', 'Rohan Mehta'),
('CMP103', 'Wipro', 'Hyderabad', 'talent@wipro.com', 'Ananya Rao'),
('CMP104', 'Persistent Systems', 'Pune', 'jobs@persistent.com', 'Kunal Deshmukh'),
('CMP105', 'Tech Mahindra', 'Mumbai', 'hr@techmahindra.com', 'Divya Iyer');

INSERT IGNORE INTO candidates (candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs, status) VALUES
('CAN1001', 'Rohan Sharma', 'rohan.sharma@gmail.com', '9876543210', 'Python', 78.50, 2026, 0, 'ACTIVE'),
('CAN1002', 'Priya Nair', 'priya.nair@gmail.com', '9876543211', 'Java', 82.00, 2026, 0, 'ACTIVE'),
('CAN1003', 'Vikram Joshi', 'vikram.joshi@gmail.com', '9876543212', 'Python', 58.00, 2026, 2, 'ACTIVE'),
('CAN1004', 'Sneha Patil', 'sneha.patil@gmail.com', '9876543213', 'Python', 85.40, 2026, 0, 'ACTIVE'),
('CAN1005', 'Rahul Verma', 'rahul.verma@gmail.com', '9876543214', 'Data Science', 79.20, 2026, 0, 'ACTIVE'),
('CAN1006', 'Neha Kulkarni', 'neha.kulkarni@gmail.com', '9876543215', 'Java', 74.80, 2026, 0, 'ACTIVE'),
('CAN1007', 'Sanket Deshmukh', 'sanket.deshmukh@gmail.com', '9876543216', 'React', 71.50, 2026, 1, 'ACTIVE'),
('CAN1008', 'Pooja More', 'pooja.more@gmail.com', '9876543217', 'Python', 76.00, 2026, 0, 'ACTIVE'),
('CAN1009', 'Aditya Kale', 'aditya.kale@gmail.com', '9876543218', 'Java', 80.10, 2026, 0, 'ACTIVE'),
('CAN1010', 'Komal Shinde', 'komal.shinde@gmail.com', '9876543219', 'Data Science', 88.30, 2026, 0, 'ACTIVE'),
('CAN1011', 'Siddharth Sawant', 'siddharth.sawant@gmail.com', '9876543220', 'Java', 73.40, 2026, 1, 'ACTIVE'),
('CAN1012', 'Tanvi Gokhale', 'tanvi.gokhale@gmail.com', '9876543221', 'React', 77.90, 2026, 0, 'ACTIVE'),
('CAN1013', 'Omkar Chavan', 'omkar.chavan@gmail.com', '9876543222', 'Python', 69.50, 2026, 0, 'ACTIVE'),
('CAN1014', 'Meera Jadhav', 'meera.jadhav@gmail.com', '9876543223', 'SQL', 72.00, 2026, 0, 'ACTIVE'),
('CAN1015', 'Nikhil Pawar', 'nikhil.pawar@gmail.com', '9876543224', 'Python', 64.00, 2025, 1, 'ACTIVE'),
('CAN1016', 'Anjali Bhosale', 'anjali.bhosale@gmail.com', '9876543225', 'Java', 84.60, 2026, 0, 'ACTIVE'),
('CAN1017', 'Pranav Mane', 'pranav.mane@gmail.com', '9876543226', 'Data Science', 61.50, 2026, 3, 'ACTIVE'),
('CAN1018', 'Shruti Gaikwad', 'shruti.gaikwad@gmail.com', '9876543227', 'React', 81.20, 2026, 0, 'ACTIVE'),
('CAN1019', 'Yashwant Suryavanshi', 'yashwant.s@gmail.com', '9876543228', 'SQL', 67.40, 2025, 0, 'INACTIVE'),
('CAN1020', 'Gauri Phadke', 'gauri.phadke@gmail.com', '9876543229', 'Python', 90.00, 2026, 0, 'INACTIVE');

INSERT IGNORE INTO jobs (job_id, company_id, job_title, technology, openings, location, package, min_percentage, passing_year, max_backlogs, deadline, status) VALUES
('JOB101', 'CMP101', 'Junior Python Developer', 'Python', 5, 'Pune', 5.50, 65.00, 2026, 0, '2026-12-31', 'OPEN'),
('JOB102', 'CMP102', 'Java Backend Trainee', 'Java', 3, 'Bengaluru', 6.00, 70.00, 2026, 1, '2026-12-31', 'OPEN'),
('JOB103', 'CMP103', 'Associate Data Analyst', 'Data Science', 4, 'Hyderabad', 6.50, 75.00, 2026, 0, '2026-12-31', 'OPEN'),
('JOB104', 'CMP104', 'Java Full Stack Engineer', 'Java', 2, 'Pune', 7.00, 70.00, 2026, 1, '2026-12-31', 'OPEN'),
('JOB105', 'CMP105', 'Frontend React Developer', 'React', 3, 'Mumbai', 5.20, 68.00, 2026, 1, '2026-12-31', 'OPEN'),
('JOB106', 'CMP101', 'SQL Support Engineer', 'SQL', 2, 'Pune', 4.20, 60.00, 2025, 1, '2026-10-15', 'CLOSED');

INSERT IGNORE INTO applications (application_id, candidate_id, job_id, applied_date, status) VALUES
('APP501', 'CAN1001', 'JOB101', '2026-11-01', 'JOINED'),
('APP502', 'CAN1002', 'JOB102', '2026-11-02', 'JOINED'),
('APP503', 'CAN1004', 'JOB101', '2026-11-03', 'JOINED'),
('APP504', 'CAN1005', 'JOB103', '2026-11-04', 'OFFERED'),
('APP505', 'CAN1006', 'JOB104', '2026-11-05', 'SELECTED'),
('APP506', 'CAN1007', 'JOB105', '2026-11-06', 'INTERVIEW'),
('APP507', 'CAN1008', 'JOB101', '2026-11-07', 'INTERVIEW'),
('APP508', 'CAN1009', 'JOB102', '2026-11-08', 'SHORTLISTED'),
('APP509', 'CAN1010', 'JOB103', '2026-11-09', 'SHORTLISTED'),
('APP510', 'CAN1011', 'JOB104', '2026-11-10', 'APPLIED'),
('APP511', 'CAN1012', 'JOB105', '2026-11-11', 'APPLIED'),
('APP512', 'CAN1013', 'JOB101', '2026-11-12', 'REJECTED');

INSERT IGNORE INTO interviews (interview_id, application_id, candidate_id, company_id, round_name, interview_date, mode, interviewer, status) VALUES
('INT101', 'APP501', 'CAN1001', 'CMP101', 'Technical Round 1', '2026-11-05', 'Online', 'Anil Deshpande', 'COMPLETED'),
('INT102', 'APP502', 'CAN1002', 'CMP102', 'Technical Round 1', '2026-11-06', 'Offline', 'Suresh Nair', 'COMPLETED'),
('INT103', 'APP503', 'CAN1004', 'CMP101', 'Technical Round 1', '2026-11-07', 'Online', 'Anil Deshpande', 'COMPLETED'),
('INT104', 'APP504', 'CAN1005', 'CMP103', 'Technical & HR', '2026-11-08', 'Online', 'Deepak Menon', 'COMPLETED'),
('INT105', 'APP505', 'CAN1006', 'CMP104', 'Technical Round 1', '2026-11-09', 'Offline', 'Ritu Malhotra', 'COMPLETED'),
('INT106', 'APP512', 'CAN1013', 'CMP101', 'Technical Round 1', '2026-11-14', 'Online', 'Anil Deshpande', 'COMPLETED'),
('INT107', 'APP506', 'CAN1007', 'CMP105', 'Technical Round 1', '2026-11-28', 'Online', 'Karthik Subramanian', 'SCHEDULED'),
('INT108', 'APP507', 'CAN1008', 'CMP101', 'Technical Round 1', '2026-11-29', 'Online', 'Anil Deshpande', 'SCHEDULED');

INSERT IGNORE INTO interview_feedback (feedback_id, interview_id, technical_rating, communication_rating, remarks, result) VALUES
('FDB101', 'INT101', 9, 8, 'Strong Python and SQL basics', 'SELECTED'),
('FDB102', 'INT102', 9, 9, 'Excellent Core Java and OOP concepts', 'SELECTED'),
('FDB103', 'INT103', 8, 9, 'Very good problem solving skills', 'SELECTED'),
('FDB104', 'INT104', 8, 8, 'Good data analysis fundamentals', 'SELECTED'),
('FDB105', 'INT105', 8, 7, 'Solid Spring and Java knowledge', 'SELECTED'),
('FDB106', 'INT106', 4, 6, 'Needs improvement in SQL queries', 'REJECTED');

INSERT IGNORE INTO offers (offer_id, application_id, candidate_id, company_id, designation, package, offer_date, joining_date, offer_status) VALUES
('OFF101', 'APP501', 'CAN1001', 'CMP101', 'Junior Python Developer', 5.50, '2026-11-10', '2026-11-20', 'ACCEPTED'),
('OFF102', 'APP502', 'CAN1002', 'CMP102', 'Java Backend Trainee', 6.00, '2026-11-11', '2026-11-21', 'ACCEPTED'),
('OFF103', 'APP503', 'CAN1004', 'CMP101', 'Junior Python Developer', 5.80, '2026-11-12', '2026-11-22', 'ACCEPTED'),
('OFF104', 'APP504', 'CAN1005', 'CMP103', 'Associate Data Analyst', 6.50, '2026-11-18', '2026-12-15', 'PENDING');

INSERT IGNORE INTO placements (placement_id, offer_id, application_id, candidate_id, company_id, designation, final_package, actual_joining_date, joining_status) VALUES
('PLC101', 'OFF101', 'APP501', 'CAN1001', 'CMP101', 'Junior Python Developer', 5.50, '2026-11-20', 'JOINED'),
('PLC102', 'OFF102', 'APP502', 'CAN1002', 'CMP102', 'Java Backend Trainee', 6.00, '2026-11-21', 'JOINED'),
('PLC103', 'OFF103', 'APP503', 'CAN1004', 'CMP101', 'Junior Python Developer', 5.80, '2026-11-22', 'JOINED');
