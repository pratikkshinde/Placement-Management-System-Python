from rpms.dao.base_dao import BaseDAO
from rpms.model.job import Job
from rpms.util.db_connection import get_connection


class JobDAO(BaseDAO):
    def _row_to_job(self, row):
        return Job(
            job_id=row[0],
            company_id=row[1],
            job_title=row[2],
            technology=row[3],
            openings=int(row[4]),
            location=row[5],
            package=float(row[6]),
            min_percentage=float(row[7]),
            passing_year=int(row[8]),
            max_backlogs=int(row[9]),
            deadline=str(row[10]),
            status=row[11],
        )

    def next_id(self):
        return self._generate_next_id("jobs", "job_id", "JOB", 101)

    def create_job(self, job):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO jobs
                (job_id, company_id, job_title, technology, openings, location, package,
                 min_percentage, passing_year, max_backlogs, deadline, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    job.job_id,
                    job.company_id,
                    job.job_title,
                    job.technology,
                    job.openings,
                    job.location,
                    job.package,
                    job.min_percentage,
                    job.passing_year,
                    job.max_backlogs,
                    job.deadline,
                    job.status,
                ),
            )
            conn.commit()
            return job
        finally:
            cursor.close()
            conn.close()

    def update_job(self, job):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE jobs
                SET company_id=%s, job_title=%s, technology=%s, openings=%s, location=%s,
                    package=%s, min_percentage=%s, passing_year=%s, max_backlogs=%s,
                    deadline=%s, status=%s
                WHERE job_id=%s
                """,
                (
                    job.company_id,
                    job.job_title,
                    job.technology,
                    job.openings,
                    job.location,
                    job.package,
                    job.min_percentage,
                    job.passing_year,
                    job.max_backlogs,
                    job.deadline,
                    job.status,
                    job.job_id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, job_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT job_id, company_id, job_title, technology, openings, location, package,
                       min_percentage, passing_year, max_backlogs, deadline, status
                FROM jobs WHERE job_id=%s
                """,
                (job_id,),
            )
            row = cursor.fetchone()
            return self._row_to_job(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_open_jobs(self) -> list[Job]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT job_id, company_id, job_title, technology, openings, location, package,
                       min_percentage, passing_year, max_backlogs, deadline, status
                FROM jobs WHERE status=%s ORDER BY job_id
                """,
                ("OPEN",),
            )
            return [self._row_to_job(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def close_job(self, job_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE jobs SET status=%s WHERE job_id=%s",
                ("CLOSED", job_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    def search_jobs(self, keyword) -> list[Job]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            like = f"%{keyword}%"
            cursor.execute(
                """
                SELECT job_id, company_id, job_title, technology, openings, location, package,
                       min_percentage, passing_year, max_backlogs, deadline, status
                FROM jobs
                WHERE job_id LIKE %s OR job_title LIKE %s OR technology LIKE %s OR location LIKE %s
                ORDER BY job_id
                """,
                (like, like, like, like),
            )
            return [self._row_to_job(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_all_jobs(self) -> list[Job]:
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT job_id, company_id, job_title, technology, openings, location, package,
                       min_percentage, passing_year, max_backlogs, deadline, status
                FROM jobs ORDER BY job_id
                """
            )
            return [self._row_to_job(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
