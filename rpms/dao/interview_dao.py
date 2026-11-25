from rpms.dao.base_dao import BaseDAO
from rpms.model.interview import Interview, InterviewFeedback
from rpms.util.db_connection import get_connection


class InterviewDAO(BaseDAO):
    def _row_to_interview(self, row):
        return Interview(
            interview_id=row[0],
            application_id=row[1],
            candidate_id=row[2],
            company_id=row[3],
            round_name=row[4],
            interview_date=str(row[5]),
            mode=row[6],
            interviewer=row[7],
            status=row[8],
        )

    def _row_to_feedback(self, row):
        return InterviewFeedback(
            feedback_id=row[0],
            interview_id=row[1],
            technical_rating=int(row[2]),
            communication_rating=int(row[3]),
            remarks=row[4] or "",
            result=row[5],
        )

    def next_interview_id(self):
        return self._generate_next_id("interviews", "interview_id", "INT", 101)

    def next_feedback_id(self):
        return self._generate_next_id("interview_feedback", "feedback_id", "FDB", 101)

    def schedule_interview(self, interview):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO interviews
                (interview_id, application_id, candidate_id, company_id, round_name,
                 interview_date, mode, interviewer, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    interview.interview_id,
                    interview.application_id,
                    interview.candidate_id,
                    interview.company_id,
                    interview.round_name,
                    interview.interview_date,
                    interview.mode,
                    interview.interviewer,
                    interview.status,
                ),
            )
            conn.commit()
            return interview
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, interview_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT interview_id, application_id, candidate_id, company_id, round_name,
                       interview_date, mode, interviewer, status
                FROM interviews WHERE interview_id=%s
                """,
                (interview_id,),
            )
            row = cursor.fetchone()
            return self._row_to_interview(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_all_interviews(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT interview_id, application_id, candidate_id, company_id, round_name,
                       interview_date, mode, interviewer, status
                FROM interviews ORDER BY interview_id
                """
            )
            return [self._row_to_interview(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def update_interview_status(self, interview_id, status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE interviews SET status=%s WHERE interview_id=%s",
                (status, interview_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    def add_feedback(self, feedback):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO interview_feedback
                (feedback_id, interview_id, technical_rating, communication_rating, remarks, result)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    feedback.feedback_id,
                    feedback.interview_id,
                    feedback.technical_rating,
                    feedback.communication_rating,
                    feedback.remarks,
                    feedback.result,
                ),
            )
            conn.commit()
            return feedback
        finally:
            cursor.close()
            conn.close()

    def get_feedback_by_interview(self, interview_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT feedback_id, interview_id, technical_rating, communication_rating, remarks, result
                FROM interview_feedback WHERE interview_id=%s
                """,
                (interview_id,),
            )
            row = cursor.fetchone()
            return self._row_to_feedback(row) if row else None
        finally:
            cursor.close()
            conn.close()
