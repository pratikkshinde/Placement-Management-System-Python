from datetime import date
from rpms.dao.company_dao import CompanyDAO
from rpms.dao.job_dao import JobDAO
from rpms.exception.custom_exceptions import JobNotFoundError
from rpms.model.job import Job
from rpms.util.activity_logger import log_activity


class JobService:
    def __init__(self):
        self.job_dao = JobDAO()
        self.company_dao = CompanyDAO()

    def _validate_job_fields(self, openings, package, min_percentage, max_backlogs, deadline):
        if openings <= 0:
            raise ValueError("Openings must be greater than 0.")
        if package < 0:
            raise ValueError("Package cannot be negative.")
        if min_percentage < 0 or min_percentage > 100:
            raise ValueError("Minimum percentage must be between 0 and 100.")
        if max_backlogs < 0:
            raise ValueError("Maximum backlogs cannot be negative.")
        try:
            date.fromisoformat(deadline.strip())
        except ValueError:
            raise ValueError("Deadline must be in YYYY-MM-DD format.")

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
        if self.company_dao.get_by_id(company_id) is None:
            raise ValueError(f"Company not found: {company_id}")

        self._validate_job_fields(openings, package, min_percentage, max_backlogs, deadline)

        job_id = self.job_dao.next_id()
        job = Job(
            job_id=job_id,
            company_id=company_id.strip(),
            job_title=job_title.strip(),
            technology=technology.strip(),
            openings=openings,
            location=location.strip(),
            package=package,
            min_percentage=min_percentage,
            passing_year=passing_year,
            max_backlogs=max_backlogs,
            deadline=deadline.strip(),
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
        existing = self.job_dao.get_by_id(job_id)
        if existing is None:
            raise JobNotFoundError(f"Job not found: {job_id}")
        if self.company_dao.get_by_id(company_id) is None:
            raise ValueError(f"Company not found: {company_id}")

        self._validate_job_fields(openings, package, min_percentage, max_backlogs, deadline)

        updated = Job(
            job_id=job_id,
            company_id=company_id.strip(),
            job_title=job_title.strip(),
            technology=technology.strip(),
            openings=openings,
            location=location.strip(),
            package=package,
            min_percentage=min_percentage,
            passing_year=passing_year,
            max_backlogs=max_backlogs,
            deadline=deadline.strip(),
            status=existing.status,
        )
        self.job_dao.update_job(updated)
        log_activity("Job Updated", job_id)
        return updated

    def get_job(self, job_id):
        job = self.job_dao.get_by_id(job_id)
        if job is None:
            raise JobNotFoundError(f"Job not found: {job_id}")
        return job

    def view_open_jobs(self) -> list[Job]:
        return self.job_dao.get_open_jobs()

    def view_all_jobs(self) -> list[Job]:
        return self.job_dao.get_all_jobs()

    def close_job(self, job_id):
        existing = self.job_dao.get_by_id(job_id)
        if existing is None:
            raise JobNotFoundError(f"Job not found: {job_id}")
        self.job_dao.close_job(job_id)
        log_activity("Job Closed", job_id)

    def search_jobs(self, keyword) -> list[Job]:
        return self.job_dao.search_jobs(keyword.strip())
