from rpms.dao.base_dao import BaseDAO
from rpms.model.candidate import Candidate
from rpms.util.db_connection import get_connection


class CandidateDAO(BaseDAO):
    def _row_to_candidate(self, row):
        return Candidate(
            candidate_id=row[0],
            name=row[1],
            email=row[2],
            mobile=row[3],
            technology=row[4],
            percentage=float(row[5]),
            passing_year=int(row[6]),
            backlogs=int(row[7]),
            status=row[8],
        )

    def next_id(self):
        return self._generate_next_id("candidates", "candidate_id", "CAN", 1001)

    def add_candidate(self, candidate):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO candidates
                (candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    candidate.candidate_id,
                    candidate.name,
                    candidate.email,
                    candidate.mobile,
                    candidate.technology,
                    candidate.percentage,
                    candidate.passing_year,
                    candidate.backlogs,
                    candidate.status,
                ),
            )
            conn.commit()
            return candidate
        finally:
            cursor.close()
            conn.close()

    def update_candidate(self, candidate):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE candidates
                SET name=%s, email=%s, mobile=%s, technology=%s,
                    percentage=%s, passing_year=%s, backlogs=%s, status=%s
                WHERE candidate_id=%s
                """,
                (
                    candidate.name,
                    candidate.email,
                    candidate.mobile,
                    candidate.technology,
                    candidate.percentage,
                    candidate.passing_year,
                    candidate.backlogs,
                    candidate.status,
                    candidate.candidate_id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, candidate_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs, status "
                "FROM candidates WHERE candidate_id=%s",
                (candidate_id,),
            )
            row = cursor.fetchone()
            return self._row_to_candidate(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_by_email(self, email):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs, status "
                "FROM candidates WHERE email=%s",
                (email,),
            )
            row = cursor.fetchone()
            return self._row_to_candidate(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_by_mobile(self, mobile):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs, status "
                "FROM candidates WHERE mobile=%s",
                (mobile,),
            )
            row = cursor.fetchone()
            return self._row_to_candidate(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def search_candidates(self, keyword) -> list[Candidate]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            like = f"%{keyword}%"
            cursor.execute(
                """
                SELECT candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs, status
                FROM candidates
                WHERE candidate_id LIKE %s OR name LIKE %s OR email LIKE %s OR technology LIKE %s
                ORDER BY candidate_id
                """,
                (like, like, like, like),
            )
            return [self._row_to_candidate(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_all_candidates(self) -> list[Candidate]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT candidate_id, name, email, mobile, technology, percentage, passing_year, backlogs, status "
                "FROM candidates ORDER BY candidate_id"
            )
            return [self._row_to_candidate(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def deactivate_candidate(self, candidate_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE candidates SET status=%s WHERE candidate_id=%s",
                ("INACTIVE", candidate_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()
