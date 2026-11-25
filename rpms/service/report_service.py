from rpms.dao.report_dao import ReportDAO
from rpms.model.candidate import Candidate
from rpms.model.job import Job


class ReportService:
    def __init__(self):
        self.report_dao = ReportDAO()

    def candidates_by_technology(self) -> dict[str, int]:
        return self.report_dao.candidates_by_technology()

    def open_jobs(self) -> list[Job]:
        return self.report_dao.open_jobs()

    def applications_by_status(self) -> dict[str, int]:
        return self.report_dao.applications_by_status()

    def company_wise_placements(self) -> dict[str, int]:
        return self.report_dao.company_wise_placements()

    def placed_candidates(self) -> list[Candidate]:
        return self.report_dao.placed_candidates()

    def unplaced_candidates(self) -> list[Candidate]:
        return self.report_dao.unplaced_candidates()
