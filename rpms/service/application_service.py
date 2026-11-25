from datetime import date
from rpms.dao.application_dao import ApplicationDAO
from rpms.dao.candidate_dao import CandidateDAO
from rpms.dao.job_dao import JobDAO
from rpms.exception.custom_exceptions import (
    CandidateNotEligibleError,
    CandidateNotFoundError,
    DuplicateApplicationError,
    JobNotFoundError,
)
from rpms.model.application import Application
from rpms.util.activity_logger import log_activity


class ApplicationService:
    VALID_TRANSITIONS = {
        "APPLIED": ["SHORTLISTED", "REJECTED"],
        "SHORTLISTED": ["INTERVIEW", "REJECTED"],
        "INTERVIEW": ["SELECTED", "REJECTED"],
        "SELECTED": ["OFFERED", "REJECTED"],
        "OFFERED": ["JOINED", "REJECTED"],
        "JOINED": [],
        "REJECTED": [],
    }

    def __init__(self):
        self.application_dao = ApplicationDAO()
        self.candidate_dao = CandidateDAO()
        self.job_dao = JobDAO()

    def _get_candidate_and_job(self, candidate_id, job_id):
        candidate = self.candidate_dao.get_by_id(candidate_id)
        if candidate is None:
            raise CandidateNotFoundError(f"Candidate not found: {candidate_id}")

        job = self.job_dao.get_by_id(job_id)
        if job is None:
            raise JobNotFoundError(f"Job not found: {job_id}")

        return candidate, job

    def _evaluate_criteria(self, candidate, job, check_duplicate=True):
        if candidate.status != "ACTIVE":
            return False, "NOT ELIGIBLE: Candidate is not active."
        if job.status != "OPEN":
            return False, "NOT ELIGIBLE: Job is not open."
        if date.today() > date.fromisoformat(job.deadline):
            return False, f"NOT ELIGIBLE: Application deadline ({job.deadline}) has passed."
        if check_duplicate and self.application_dao.get_by_candidate_and_job(candidate.candidate_id, job.job_id) is not None:
            return False, "NOT ELIGIBLE: Candidate has already applied for this job."
        if candidate.percentage < job.min_percentage:
            return (
                False,
                f"NOT ELIGIBLE: Percentage {candidate.percentage}% is below required {job.min_percentage}%.",
            )
        if candidate.passing_year != job.passing_year:
            return (
                False,
                f"NOT ELIGIBLE: Passing year {candidate.passing_year} does not match required {job.passing_year}.",
            )
        if candidate.backlogs > job.max_backlogs:
            return (
                False,
                f"NOT ELIGIBLE: Backlogs ({candidate.backlogs}) exceed maximum allowed ({job.max_backlogs}).",
            )
        return True, "ELIGIBLE: All eligibility criteria satisfied."

    def check_eligibility(self, candidate_id, job_id):
        candidate, job = self._get_candidate_and_job(candidate_id, job_id)
        return self._evaluate_criteria(candidate, job, check_duplicate=True)

    def apply_for_job(self, candidate_id, job_id):
        candidate, job = self._get_candidate_and_job(candidate_id, job_id)

        if self.application_dao.get_by_candidate_and_job(candidate_id, job_id) is not None:
            raise DuplicateApplicationError(
                f"Candidate {candidate_id} has already applied for job {job_id}."
            )

        eligible, message = self._evaluate_criteria(candidate, job, check_duplicate=False)
        if not eligible:
            raise CandidateNotEligibleError(message)

        application_id = self.application_dao.next_id()
        application = Application(
            application_id=application_id,
            candidate_id=candidate_id,
            job_id=job_id,
            applied_date=str(date.today()),
            status="APPLIED",
        )
        self.application_dao.create_application(application)
        log_activity("Application Created", application_id)
        return application

    def update_application_status(self, application_id, new_status):
        application = self.application_dao.get_by_id(application_id)
        if application is None:
            raise ValueError(f"Application not found: {application_id}")

        target_status = new_status.strip().upper()
        allowed = self.VALID_TRANSITIONS.get(application.status, [])
        if target_status not in allowed:
            raise ValueError(
                f"Invalid status transition: {application.status} -> {target_status}"
            )

        self.application_dao.update_status(application_id, target_status)
        application.status = target_status

        if target_status == "SHORTLISTED":
            log_activity("Candidate Shortlisted", application_id)
        else:
            log_activity(f"Application {target_status.title()}", application_id)

        return application

    def get_application(self, application_id):
        application = self.application_dao.get_by_id(application_id)
        if application is None:
            raise ValueError(f"Application not found: {application_id}")
        return application

    def view_all_applications(self) -> list[Application]:
        return self.application_dao.get_all_applications()
