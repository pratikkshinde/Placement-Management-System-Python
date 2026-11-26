from datetime import date
from rpms.dao.company_dao import CompanyDAO
from rpms.dao.job_dao import JobDAO
from rpms.exception.custom_exceptions import JobNotFoundError
from rpms.model.job import Job
from rpms.util.activity_logger import log_activity
from rpms.util.validation import require_non_empty, validate_iso_date, validate_passing_year


class JobService:
    def __init__(self):
        self.job_dao = JobDAO()
        self.company_dao = CompanyDAO()

    def _validate_job_fields(
        self,
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
        check_future_deadline=False,
    ):
        clean_company_id = require_non_empty(company_id, "Company ID")
        clean_title = require_non_empty(job_title, "Job title")
        clean_tech = require_non_empty(technology, "Technology")
        clean_location = require_non_empty(location, "Location")

        if openings <= 0:
            raise ValueError("Openings must be greater than 0.")
        if package <= 0:
            raise ValueError("Package must be greater than 0.")
        if min_percentage < 0 or min_percentage > 100:
            raise ValueError("Minimum percentage must be between 0 and 100.")
        clean_year = validate_passing_year(passing_year, "Passing year")
        if max_backlogs < 0:
            raise ValueError("Maximum backlogs cannot be negative.")

        parsed_deadline = validate_iso_date(deadline, "Deadline")
        if check_future_deadline and parsed_deadline < date.today():
            raise ValueError("Deadline cannot be in the past.")

        return (
            clean_company_id,
            clean_title,
            clean_tech,
            clean_location,
            clean_year,
            str(parsed_deadline),
        )

    def create_job(
        self,
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
    ):
        (
            clean_company_id,
            clean_title,
            clean_tech,
            clean_location,
            clean_year,
            clean_deadline,
        ) = self._validate_job_fields(
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
            check_future_deadline=True,
        )

        if self.company_dao.get_by_id(clean_company_id) is None:
            raise ValueError(f"Company not found: {clean_company_id}")

        job_id = self.job_dao.next_id()
        job = Job(
            job_id=job_id,
            company_id=clean_company_id,
            job_title=clean_title,
            technology=clean_tech,
            openings=openings,
            location=clean_location,
            package=package,
            min_percentage=min_percentage,
            passing_year=clean_year,
            max_backlogs=max_backlogs,
            deadline=clean_deadline,
            status="OPEN",
        )
        self.job_dao.create_job(job)
        log_activity("Job Created", job_id)
        return job

    def update_job(
        self,
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
    ):
        clean_job_id = require_non_empty(job_id, "Job ID")
        existing = self.job_dao.get_by_id(clean_job_id)
        if existing is None:
            raise JobNotFoundError(f"Job not found: {clean_job_id}")

        (
            clean_company_id,
            clean_title,
            clean_tech,
            clean_location,
            clean_year,
            clean_deadline,
        ) = self._validate_job_fields(
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
            check_future_deadline=False,
        )

        if self.company_dao.get_by_id(clean_company_id) is None:
            raise ValueError(f"Company not found: {clean_company_id}")

        updated = Job(
            job_id=clean_job_id,
            company_id=clean_company_id,
            job_title=clean_title,
            technology=clean_tech,
            openings=openings,
            location=clean_location,
            package=package,
            min_percentage=min_percentage,
            passing_year=clean_year,
            max_backlogs=max_backlogs,
            deadline=clean_deadline,
            status=existing.status,
        )
        self.job_dao.update_job(updated)
        log_activity("Job Updated", clean_job_id)
        return updated

    def get_job(self, job_id):
        clean_job_id = require_non_empty(job_id, "Job ID")
        job = self.job_dao.get_by_id(clean_job_id)
        if job is None:
            raise JobNotFoundError(f"Job not found: {clean_job_id}")
        return job

    def view_open_jobs(self) -> list[Job]:
        return self.job_dao.get_open_jobs()

    def view_all_jobs(self) -> list[Job]:
        return self.job_dao.get_all_jobs()

    def close_job(self, job_id):
        clean_job_id = require_non_empty(job_id, "Job ID")
        existing = self.job_dao.get_by_id(clean_job_id)
        if existing is None:
            raise JobNotFoundError(f"Job not found: {clean_job_id}")
        self.job_dao.close_job(clean_job_id)
        log_activity("Job Closed", clean_job_id)

    def search_jobs(self, keyword) -> list[Job]:
        return self.job_dao.search_jobs(require_non_empty(keyword, "Search keyword"))
