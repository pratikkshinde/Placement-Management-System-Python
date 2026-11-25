from rpms.dao.base_dao import BaseDAO
from rpms.model.company import Company
from rpms.util.db_connection import get_connection


class CompanyDAO(BaseDAO):
    def _row_to_company(self, row):
        return Company(
            company_id=row[0],
            name=row[1],
            location=row[2],
            contact_email=row[3],
            hr_name=row[4],
        )

    def next_id(self):
        return self._generate_next_id("companies", "company_id", "CMP", 101)

    def add_company(self, company):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO companies (company_id, name, location, contact_email, hr_name)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    company.company_id,
                    company.name,
                    company.location,
                    company.contact_email,
                    company.hr_name,
                ),
            )
            conn.commit()
            return company
        finally:
            cursor.close()
            conn.close()

    def update_company(self, company):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                UPDATE companies
                SET name=%s, location=%s, contact_email=%s, hr_name=%s
                WHERE company_id=%s
                """,
                (
                    company.name,
                    company.location,
                    company.contact_email,
                    company.hr_name,
                    company.company_id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, company_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT company_id, name, location, contact_email, hr_name FROM companies WHERE company_id=%s",
                (company_id,),
            )
            row = cursor.fetchone()
            return self._row_to_company(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_by_name(self, name):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT company_id, name, location, contact_email, hr_name FROM companies WHERE name=%s",
                (name,),
            )
            row = cursor.fetchone()
            return self._row_to_company(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def search_companies(self, keyword):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            like = f"%{keyword}%"
            cursor.execute(
                """
                SELECT company_id, name, location, contact_email, hr_name
                FROM companies
                WHERE company_id LIKE %s OR name LIKE %s OR location LIKE %s
                ORDER BY company_id
                """,
                (like, like, like),
            )
            return [self._row_to_company(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def get_all_companies(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT company_id, name, location, contact_email, hr_name FROM companies ORDER BY company_id"
            )
            return [self._row_to_company(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
