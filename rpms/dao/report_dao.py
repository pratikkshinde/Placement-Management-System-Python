from rpms.dao.candidate_dao import CandidateDAO
from rpms.dao.job_dao import JobDAO
from rpms.model.candidate import Candidate
from rpms.model.job import Job
from rpms.util.db_connection import get_connection


class ReportDAO:
    def candidates_by_technology(self) -> dict[str, int]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT technology, COUNT(*) FROM candidates GROUP BY technology ORDER BY technology"
            )
            report: dict[str, int] = {}
            for tech, count in cursor.fetchall():
                report[str(tech)] = int(count)
            return report
        finally:
            cursor.close()
            conn.close()

    def open_jobs(self) -> list[Job]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            job_dao = JobDAO()
            cursor.execute(
                """
                SELECT job_id, company_id, job_title, technology, openings, location, package,
                       min_percentage, passing_year, max_backlogs, deadline, status
                FROM jobs WHERE status=%s ORDER BY job_id
                """,
                ("OPEN",),
            )
            return [job_dao._row_to_job(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def applications_by_status(self) -> dict[str, int]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT status, COUNT(*) FROM applications GROUP BY status ORDER BY status"
            )
            report: dict[str, int] = {}
            for status, count in cursor.fetchall():
                report[str(status)] = int(count)
            return report
        finally:
            cursor.close()
            conn.close()

    def company_wise_placements(self) -> dict[str, int]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT c.name, COUNT(p.placement_id)
                FROM companies c
                INNER JOIN placements p ON c.company_id = p.company_id
                WHERE p.joining_status = %s
                GROUP BY c.company_id, c.name
                ORDER BY c.name
                """,
                ("JOINED",),
            )
            report: dict[str, int] = {}
            for company_name, count in cursor.fetchall():
                report[str(company_name)] = int(count)
            return report
        finally:
            cursor.close()
            conn.close()

    def placed_candidates(self) -> list[Candidate]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            candidate_dao = CandidateDAO()
            cursor.execute(
                """
                SELECT DISTINCT c.candidate_id, c.name, c.email, c.mobile, c.technology,
                                c.percentage, c.passing_year, c.backlogs, c.status
                FROM candidates c
                INNER JOIN placements p ON c.candidate_id = p.candidate_id
                WHERE p.joining_status = %s
                ORDER BY c.candidate_id
                """,
                ("JOINED",),
            )
            return [candidate_dao._row_to_candidate(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def unplaced_candidates(self) -> list[Candidate]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            candidate_dao = CandidateDAO()
            cursor.execute(
                """
                SELECT c.candidate_id, c.name, c.email, c.mobile, c.technology,
                       c.percentage, c.passing_year, c.backlogs, c.status
                FROM candidates c
                WHERE c.candidate_id NOT IN (
                    SELECT candidate_id FROM placements WHERE joining_status = %s
                )
                ORDER BY c.candidate_id
                """,
                ("JOINED",),
            )
            return [candidate_dao._row_to_candidate(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
