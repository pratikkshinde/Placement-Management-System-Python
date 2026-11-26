from rpms.dao.candidate_dao import CandidateDAO
from rpms.exception.custom_exceptions import CandidateNotFoundError
from rpms.model.candidate import Candidate
from rpms.util.activity_logger import log_activity
from rpms.util.validation import (
    require_non_empty,
    validate_email,
    validate_mobile,
    validate_passing_year,
)


class CandidateService:
    def __init__(self):
        self.candidate_dao = CandidateDAO()

    def _validate_candidate_fields(
        self, name, email, mobile, technology, percentage, passing_year, backlogs
    ):
        clean_name = require_non_empty(name, "Candidate name")
        clean_email = validate_email(email, "Email")
        clean_mobile = validate_mobile(mobile)
        clean_technology = require_non_empty(technology, "Technology")

        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        clean_year = validate_passing_year(passing_year, "Passing year")
        if backlogs < 0:
            raise ValueError("Backlog count cannot be negative.")

        return clean_name, clean_email, clean_mobile, clean_technology, clean_year

    def add_candidate(self, name, email, mobile, technology, percentage, passing_year, backlogs):
        (
            clean_name,
            clean_email,
            clean_mobile,
            clean_technology,
            clean_year,
        ) = self._validate_candidate_fields(
            name, email, mobile, technology, percentage, passing_year, backlogs
        )

        if self.candidate_dao.get_by_email(clean_email) is not None:
            raise ValueError(f"Duplicate email not allowed: {clean_email}")
        if self.candidate_dao.get_by_mobile(clean_mobile) is not None:
            raise ValueError(f"Duplicate mobile not allowed: {clean_mobile}")

        candidate_id = self.candidate_dao.next_id()
        candidate = Candidate(
            candidate_id=candidate_id,
            name=clean_name,
            email=clean_email,
            mobile=clean_mobile,
            technology=clean_technology,
            percentage=percentage,
            passing_year=clean_year,
            backlogs=backlogs,
            status="ACTIVE",
        )
        self.candidate_dao.add_candidate(candidate)
        log_activity("Candidate Created", candidate_id)
        return candidate

    def update_candidate(
        self, candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs
    ):
        clean_id = require_non_empty(candidate_id, "Candidate ID")
        existing = self.candidate_dao.get_by_id(clean_id)
        if existing is None:
            raise CandidateNotFoundError(f"Candidate not found: {clean_id}")

        (
            clean_name,
            clean_email,
            clean_mobile,
            clean_technology,
            clean_year,
        ) = self._validate_candidate_fields(
            name, email, mobile, technology, percentage, passing_year, backlogs
        )

        email_owner = self.candidate_dao.get_by_email(clean_email)
        if email_owner is not None and email_owner.candidate_id != clean_id:
            raise ValueError(f"Duplicate email not allowed: {clean_email}")

        mobile_owner = self.candidate_dao.get_by_mobile(clean_mobile)
        if mobile_owner is not None and mobile_owner.candidate_id != clean_id:
            raise ValueError(f"Duplicate mobile not allowed: {clean_mobile}")

        updated = Candidate(
            candidate_id=clean_id,
            name=clean_name,
            email=clean_email,
            mobile=clean_mobile,
            technology=clean_technology,
            percentage=percentage,
            passing_year=clean_year,
            backlogs=backlogs,
            status=existing.status,
        )
        self.candidate_dao.update_candidate(updated)
        log_activity("Candidate Updated", clean_id)
        return updated

    def get_candidate(self, candidate_id):
        clean_id = require_non_empty(candidate_id, "Candidate ID")
        candidate = self.candidate_dao.get_by_id(clean_id)
        if candidate is None:
            raise CandidateNotFoundError(f"Candidate not found: {clean_id}")
        return candidate

    def search_candidates(self, keyword) -> list[Candidate]:
        return self.candidate_dao.search_candidates(require_non_empty(keyword, "Search keyword"))

    def view_all_candidates(self) -> list[Candidate]:
        return self.candidate_dao.get_all_candidates()

    def deactivate_candidate(self, candidate_id):
        clean_id = require_non_empty(candidate_id, "Candidate ID")
        existing = self.candidate_dao.get_by_id(clean_id)
        if existing is None:
            raise CandidateNotFoundError(f"Candidate not found: {clean_id}")
        self.candidate_dao.deactivate_candidate(clean_id)
        log_activity("Candidate Deactivated", clean_id)
