from rpms.dao.base_dao import BaseDAO
from rpms.model.application import Application
from rpms.util.db_connection import get_connection


class ApplicationDAO(BaseDAO):
    def _row_to_application(self, row):
        return Application(
            application_id=row[0],
            candidate_id=row[1],
            job_id=row[2],
            applied_date=str(row[3]),
            status=row[4],
        )

    def next_id(self):
        return self._generate_next_id("applications", "application_id", "APP", 501)

    def create_application(self, application):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO applications (application_id, candidate_id, job_id, applied_date, status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    application.application_id,
                    application.candidate_id,
                    application.job_id,
                    application.applied_date,
                    application.status,
                ),
            )
            conn.commit()
            return application
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, application_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT application_id, candidate_id, job_id, applied_date, status "
                "FROM applications WHERE application_id=%s",
                (application_id,),
            )
            row = cursor.fetchone()
            return self._row_to_application(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_by_candidate_and_job(self, candidate_id, job_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT application_id, candidate_id, job_id, applied_date, status "
                "FROM applications WHERE candidate_id=%s AND job_id=%s",
                (candidate_id, job_id),
            )
            row = cursor.fetchone()
            return self._row_to_application(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_all_applications(self) -> list[Application]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT application_id, candidate_id, job_id, applied_date, status "
                "FROM applications ORDER BY application_id"
            )
            return [self._row_to_application(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_by_candidate(self, candidate_id) -> list[Application]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT application_id, candidate_id, job_id, applied_date, status "
                "FROM applications WHERE candidate_id=%s ORDER BY application_id",
                (candidate_id,),
            )
            return [self._row_to_application(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def update_status(self, application_id, new_status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE applications SET status=%s WHERE application_id=%s",
                (new_status, application_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()
