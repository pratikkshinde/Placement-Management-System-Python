from rpms.dao.candidate_dao import CandidateDAO
from rpms.exception.custom_exceptions import CandidateNotFoundError
from rpms.model.candidate import Candidate
from rpms.util.activity_logger import log_activity


class CandidateService:
    def __init__(self):
        self.candidate_dao = CandidateDAO()

    def _validate_candidate_fields(self, percentage, backlogs):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        if backlogs < 0:
            raise ValueError("Backlog count cannot be negative.")

    def add_candidate(self, name, email, mobile, technology, percentage, passing_year, backlogs):
        self._validate_candidate_fields(percentage, backlogs)

        if self.candidate_dao.get_by_email(email) is not None:
            raise ValueError(f"Duplicate email not allowed: {email}")
        if self.candidate_dao.get_by_mobile(mobile) is not None:
            raise ValueError(f"Duplicate mobile not allowed: {mobile}")

        candidate_id = self.candidate_dao.next_id()
        candidate = Candidate(
            candidate_id=candidate_id,
            name=name.strip(),
            email=email.strip(),
            mobile=mobile.strip(),
            technology=technology.strip(),
            percentage=percentage,
            passing_year=passing_year,
            backlogs=backlogs,
            status="ACTIVE",
        )
        self.candidate_dao.add_candidate(candidate)
        log_activity("Candidate Created", candidate_id)
        return candidate

    def update_candidate(
        self, candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs
    ):
        existing = self.candidate_dao.get_by_id(candidate_id)
        if existing is None:
            raise CandidateNotFoundError(f"Candidate not found: {candidate_id}")

        self._validate_candidate_fields(percentage, backlogs)

        email_owner = self.candidate_dao.get_by_email(email)
        if email_owner is not None and email_owner.candidate_id != candidate_id:
            raise ValueError(f"Duplicate email not allowed: {email}")

        mobile_owner = self.candidate_dao.get_by_mobile(mobile)
        if mobile_owner is not None and mobile_owner.candidate_id != candidate_id:
            raise ValueError(f"Duplicate mobile not allowed: {mobile}")

        updated = Candidate(
            candidate_id=candidate_id,
            name=name.strip(),
            email=email.strip(),
            mobile=mobile.strip(),
            technology=technology.strip(),
            percentage=percentage,
            passing_year=passing_year,
            backlogs=backlogs,
            status=existing.status,
        )
        self.candidate_dao.update_candidate(updated)
        log_activity("Candidate Updated", candidate_id)
        return updated

    def get_candidate(self, candidate_id):
        candidate = self.candidate_dao.get_by_id(candidate_id)
        if candidate is None:
            raise CandidateNotFoundError(f"Candidate not found: {candidate_id}")
        return candidate

    def search_candidates(self, keyword) -> list[Candidate]:
        return self.candidate_dao.search_candidates(keyword.strip())

    def view_all_candidates(self) -> list[Candidate]:
        return self.candidate_dao.get_all_candidates()

    def deactivate_candidate(self, candidate_id):
        existing = self.candidate_dao.get_by_id(candidate_id)
        if existing is None:
            raise CandidateNotFoundError(f"Candidate not found: {candidate_id}")
        self.candidate_dao.deactivate_candidate(candidate_id)
        log_activity("Candidate Deactivated", candidate_id)
