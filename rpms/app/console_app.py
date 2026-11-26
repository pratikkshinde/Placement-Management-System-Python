import mysql.connector
from rpms.exception.custom_exceptions import (
    CandidateNotEligibleError,
    CandidateNotFoundError,
    DuplicateApplicationError,
    JobNotFoundError,
)
from rpms.service.application_service import ApplicationService
from rpms.service.candidate_service import CandidateService
from rpms.service.company_service import CompanyService
from rpms.service.interview_service import InterviewService
from rpms.service.job_service import JobService
from rpms.service.offer_service import OfferService
from rpms.service.placement_service import PlacementService
from rpms.service.report_service import ReportService


class ConsoleApp:
    def __init__(self):
        self.candidate_service = CandidateService()
        self.company_service = CompanyService()
        self.job_service = JobService()
        self.application_service = ApplicationService()
        self.interview_service = InterviewService()
        self.offer_service = OfferService()
        self.placement_service = PlacementService()
        self.report_service = ReportService()

    def show_list(self, items, empty_message):
        if not items:
            print(empty_message)
            return
        for item in items:
            print(item)

    def show_dict_report(self, title, data):
        print(f"\n--- {title} ---")
        if not data:
            print("No records found.")
            return
        for key, count in data.items():
            print(f"{key}: {count}")

    def run(self):
        while True:
            print("\n==================================")
            print("RECRUITMENT & PLACEMENT SYSTEM")
            print("==================================")
            print("\n1. Candidates")
            print("2. Companies")
            print("3. Jobs")
            print("4. Applications")
            print("5. Interviews")
            print("6. Offers")
            print("7. Placements")
            print("8. Reports")
            print("9. Exit")

            choice = input("\nSelect a module (1-9): ").strip()
            if choice == "1":
                self.candidates_menu()
            elif choice == "2":
                self.companies_menu()
            elif choice == "3":
                self.jobs_menu()
            elif choice == "4":
                self.applications_menu()
            elif choice == "5":
                self.interviews_menu()
            elif choice == "6":
                self.offers_menu()
            elif choice == "7":
                self.placements_menu()
            elif choice == "8":
                self.reports_menu()
            elif choice == "9":
                print("Exiting Recruitment & Placement System. Goodbye!")
                break
            else:
                print("Invalid choice. Please select 1 to 9.")

    def candidates_menu(self):
        while True:
            print("\n--- Candidate Management Menu ---")
            print("1. Add Candidate")
            print("2. Update Candidate")
            print("3. Search Candidate")
            print("4. View All Candidates")
            print("5. Deactivate Candidate")
            print("6. Back")
            choice = input("Enter choice: ").strip()

            try:
                if choice == "1":
                    name = input("Name: ").strip()
                    email = input("Email: ").strip()
                    mobile = input("Mobile: ").strip()
                    technology = input("Technology: ").strip()
                    percentage = float(input("Percentage (0-100): ").strip())
                    passing_year = int(input("Passing Year: ").strip())
                    backlogs = int(input("Backlogs: ").strip())
                    candidate = self.candidate_service.add_candidate(
                        name, email, mobile, technology, percentage, passing_year, backlogs
                    )
                    print(f"Candidate Created: {candidate.candidate_id}")

                elif choice == "2":
                    candidate_id = input("Candidate ID: ").strip()
                    name = input("New Name: ").strip()
                    email = input("New Email: ").strip()
                    mobile = input("New Mobile: ").strip()
                    technology = input("New Technology: ").strip()
                    percentage = float(input("New Percentage (0-100): ").strip())
                    passing_year = int(input("New Passing Year: ").strip())
                    backlogs = int(input("New Backlogs: ").strip())
                    candidate = self.candidate_service.update_candidate(
                        candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs
                    )
                    print(f"Candidate Updated: {candidate.candidate_id}")

                elif choice == "3":
                    keyword = input("Search Keyword (ID, Name, Email, or Technology): ").strip()
                    results = self.candidate_service.search_candidates(keyword)
                    self.show_list(results, "No matching candidates found.")

                elif choice == "4":
                    candidates = self.candidate_service.view_all_candidates()
                    self.show_list(candidates, "No candidates found.")

                elif choice == "5":
                    candidate_id = input("Candidate ID to deactivate: ").strip()
                    self.candidate_service.deactivate_candidate(candidate_id)
                    print(f"Candidate Deactivated: {candidate_id}")

                elif choice == "6":
                    break
                else:
                    print("Invalid choice.")

            except (CandidateNotFoundError, ValueError) as err:
                print(f"Error: {err}")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")

    def companies_menu(self):
        while True:
            print("\n--- Company Management ---")
            print("1. Add Company")
            print("2. Update Company")
            print("3. Search Company")
            print("4. View All Companies")
            print("5. Back")
            choice = input("Enter choice: ").strip()

            try:
                if choice == "1":
                    name = input("Company Name (Required): ").strip()
                    location = input("Location: ").strip()
                    contact_email = input("Contact Email: ").strip()
                    hr_name = input("HR Name: ").strip()
                    company = self.company_service.add_company(name, location, contact_email, hr_name)
                    print(f"Company Created: {company.company_id}")

                elif choice == "2":
                    company_id = input("Company ID: ").strip()
                    name = input("New Company Name: ").strip()
                    location = input("New Location: ").strip()
                    contact_email = input("New Contact Email: ").strip()
                    hr_name = input("New HR Name: ").strip()
                    company = self.company_service.update_company(
                        company_id, name, location, contact_email, hr_name
                    )
                    print(f"Company Updated: {company.company_id}")

                elif choice == "3":
                    keyword = input("Enter Company ID / Name / Location: ").strip()
                    results = self.company_service.search_companies(keyword)
                    self.show_list(results, "No matching companies found.")

                elif choice == "4":
                    companies = self.company_service.view_all_companies()
                    self.show_list(companies, "No companies found.")

                elif choice == "5":
                    break
                else:
                    print("Invalid choice.")

            except ValueError as err:
                print(f"Error: {err}")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")

    def jobs_menu(self):
        while True:
            print("\n--- Job Opening Management ---")
            print("1. Create Job")
            print("2. Update Job")
            print("3. View Open Jobs")
            print("4. Close Job")
            print("5. Search Job")
            print("6. Back")
            choice = input("Enter choice: ").strip()

            try:
                if choice == "1":
                    company_id = input("Company ID: ").strip()
                    job_title = input("Job Title: ").strip()
                    technology = input("Technology: ").strip()
                    openings = int(input("Openings: ").strip())
                    location = input("Location: ").strip()
                    package = float(input("Annual Package (LPA): ").strip())
                    min_percentage = float(input("Minimum Percentage: ").strip())
                    passing_year = int(input("Passing Year: ").strip())
                    max_backlogs = int(input("Maximum Backlogs: ").strip())
                    deadline = input("Deadline (YYYY-MM-DD): ").strip()
                    job = self.job_service.create_job(
                        company_id,
                        job_title,
                        technology,
                        openings,
                        location,
                        package,
                        min_percentage,
                        passing_year,
                        max_backlogs,
                        deadline,
                    )
                    print(f"Job Created: {job.job_id}")

                elif choice == "2":
                    job_id = input("Job ID: ").strip()
                    company_id = input("New Company ID: ").strip()
                    job_title = input("New Job Title: ").strip()
                    technology = input("New Technology: ").strip()
                    openings = int(input("New Openings: ").strip())
                    location = input("New Location: ").strip()
                    package = float(input("New Package (LPA): ").strip())
                    min_percentage = float(input("New Minimum Percentage: ").strip())
                    passing_year = int(input("New Passing Year: ").strip())
                    max_backlogs = int(input("New Maximum Backlogs: ").strip())
                    deadline = input("New Deadline (YYYY-MM-DD): ").strip()
                    job = self.job_service.update_job(
                        job_id,
                        company_id,
                        job_title,
                        technology,
                        openings,
                        location,
                        package,
                        min_percentage,
                        passing_year,
                        max_backlogs,
                        deadline,
                    )
                    print(f"Job Updated: {job.job_id}")

                elif choice == "3":
                    open_jobs = self.job_service.view_open_jobs()
                    self.show_list(open_jobs, "No open jobs found.")

                elif choice == "4":
                    job_id = input("Job ID to close: ").strip()
                    self.job_service.close_job(job_id)
                    print(f"Job Closed: {job_id}")

                elif choice == "5":
                    keyword = input("Enter Job ID / Title / Technology / Location: ").strip()
                    results = self.job_service.search_jobs(keyword)
                    self.show_list(results, "No matching jobs found.")

                elif choice == "6":
                    break
                else:
                    print("Invalid choice.")

            except (JobNotFoundError, ValueError) as err:
                print(f"Error: {err}")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")

    def applications_menu(self):
        while True:
            print("\n--- Job Applications & Eligibility Check ---")
            print("1. Check Eligibility")
            print("2. Apply for Job")
            print("3. Update Application Status")
            print("4. View All Applications")
            print("5. Back")
            choice = input("Enter choice: ").strip()

            try:
                if choice == "1":
                    candidate_id = input("Candidate ID: ").strip()
                    job_id = input("Job ID: ").strip()
                    _, message = self.application_service.check_eligibility(candidate_id, job_id)
                    print(message)

                elif choice == "2":
                    candidate_id = input("Candidate ID: ").strip()
                    job_id = input("Job ID: ").strip()
                    application = self.application_service.apply_for_job(candidate_id, job_id)
                    print(f"Application Submitted: {application.application_id} ({application.status})")

                elif choice == "3":
                    application_id = input("Application ID: ").strip()
                    print("Allowed statuses: SHORTLISTED, INTERVIEW, SELECTED, OFFERED, JOINED, REJECTED")
                    new_status = input("New Status: ").strip()
                    application = self.application_service.update_application_status(
                        application_id, new_status
                    )
                    print(f"Application {application.application_id} status updated to {application.status}")

                elif choice == "4":
                    applications = self.application_service.view_all_applications()
                    self.show_list(applications, "No applications found.")

                elif choice == "5":
                    break
                else:
                    print("Invalid choice.")

            except (
                CandidateNotFoundError,
                JobNotFoundError,
                DuplicateApplicationError,
                CandidateNotEligibleError,
                ValueError,
            ) as err:
                print(f"Error: {err}")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")

    def interviews_menu(self):
        while True:
            print("\n--- Interview Scheduling & Feedback ---")
            print("1. Schedule Interview")
            print("2. Record Feedback")
            print("3. View All Interviews")
            print("4. View Interview Feedback")
            print("5. Back")
            choice = input("Enter choice: ").strip()

            try:
                if choice == "1":
                    application_id = input("Application ID: ").strip()
                    round_name = input("Round (e.g. Technical Round 1 / HR): ").strip()
                    interview_date = input("Date (YYYY-MM-DD): ").strip()
                    mode = input("Mode (Online / Offline): ").strip()
                    interviewer = input("Interviewer: ").strip()
                    interview = self.interview_service.schedule_interview(
                        application_id, round_name, interview_date, mode, interviewer
                    )
                    print(f"Interview Scheduled: {interview.interview_id}")

                elif choice == "2":
                    interview_id = input("Interview ID: ").strip()
                    technical_rating = int(input("Technical Rating (1-10): ").strip())
                    communication_rating = int(input("Communication Rating (1-10): ").strip())
                    remarks = input("Remarks: ").strip()
                    result = input("Result (SELECTED / REJECTED / NEXT_ROUND): ").strip()
                    feedback = self.interview_service.record_feedback(
                        interview_id, technical_rating, communication_rating, remarks, result
                    )
                    print(f"Feedback Recorded: {feedback.feedback_id} (Result: {feedback.result})")

                elif choice == "3":
                    interviews = self.interview_service.view_all_interviews()
                    self.show_list(interviews, "No interviews found.")

                elif choice == "4":
                    interview_id = input("Interview ID: ").strip()
                    feedback = self.interview_service.get_feedback(interview_id)
                    if feedback is None:
                        print("No feedback found for this interview.")
                    else:
                        print(feedback)

                elif choice == "5":
                    break
                else:
                    print("Invalid choice.")

            except (JobNotFoundError, ValueError) as err:
                print(f"Error: {err}")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")

    def offers_menu(self):
        while True:
            print("\n--- Offer Management ---")
            print("1. Create Offer")
            print("2. Update Offer Status")
            print("3. View All Offers")
            print("4. Back")
            choice = input("Enter choice: ").strip()

            try:
                if choice == "1":
                    application_id = input("Application ID: ").strip()
                    designation = input("Designation: ").strip()
                    package = float(input("Offered Package (LPA): ").strip())
                    offer_date = input("Offer Date (YYYY-MM-DD): ").strip()
                    joining_date = input("Joining Date (YYYY-MM-DD): ").strip()
                    offer = self.offer_service.create_offer(
                        application_id, designation, package, offer_date, joining_date
                    )
                    print(f"Offer Created: {offer.offer_id}")

                elif choice == "2":
                    offer_id = input("Offer ID: ").strip()
                    offer_status = input("Offer Status (ACCEPTED / DECLINED / PENDING): ").strip()
                    offer = self.offer_service.update_offer_status(offer_id, offer_status)
                    print(f"Offer {offer.offer_id} status updated to {offer.offer_status}")

                elif choice == "3":
                    offers = self.offer_service.view_all_offers()
                    self.show_list(offers, "No offers found.")

                elif choice == "4":
                    break
                else:
                    print("Invalid choice.")

            except (JobNotFoundError, ValueError) as err:
                print(f"Error: {err}")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")

    def placements_menu(self):
        while True:
            print("\n--- Placement Management ---")
            print("1. Record Placement")
            print("2. View All Placements")
            print("3. Back")
            choice = input("Enter choice: ").strip()

            try:
                if choice == "1":
                    offer_id = input("Offer ID: ").strip()
                    final_package = float(input("Final Package (LPA): ").strip())
                    actual_joining_date = input("Actual Joining Date (YYYY-MM-DD): ").strip()
                    joining_status = input("Joining Status (JOINED / NOT_JOINED): ").strip()
                    placement = self.placement_service.record_placement(
                        offer_id, final_package, actual_joining_date, joining_status
                    )
                    print(f"Placement Recorded: {placement.placement_id}")

                elif choice == "2":
                    placements = self.placement_service.view_all_placements()
                    self.show_list(placements, "No placements found.")

                elif choice == "3":
                    break
                else:
                    print("Invalid choice.")

            except ValueError as err:
                print(f"Error: {err}")
            except mysql.connector.Error as err:
                print(f"Database Error: {err}")

    def reports_menu(self):
        while True:
            print("\n--- Placement & Recruitment Reports ---")
            print("1. Candidates by Technology")
            print("2. Open Jobs")
            print("3. Applications by Status")
            print("4. Company-wise Placements")
            print("5. Placed Candidates")
            print("6. Unplaced Candidates")
            print("7. Back")
            choice = input("Enter choice: ").strip()

            try:
                if choice == "1":
                    self.show_dict_report(
                        "Candidates by Technology",
                        self.report_service.candidates_by_technology(),
                    )
                elif choice == "2":
                    self.show_list(self.report_service.open_jobs(), "No open jobs found.")
                elif choice == "3":
                    self.show_dict_report(
                        "Applications by Status",
                        self.report_service.applications_by_status(),
                    )
                elif choice == "4":
                    self.show_dict_report(
                        "Company-wise Placements",
                        self.report_service.company_wise_placements(),
                    )
                elif choice == "5":
                    self.show_list(
                        self.report_service.placed_candidates(),
                        "No placed candidates found.",
                    )
                elif choice == "6":
                    self.show_list(
                        self.report_service.unplaced_candidates(),
                        "No unplaced candidates found.",
                    )
                elif choice == "7":
                    break
                else:
                    print("Invalid choice.")

            except mysql.connector.Error as err:
                print(f"Database Error: {err}")
