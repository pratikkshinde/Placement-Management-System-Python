from rpms.dao.base_dao import BaseDAO
from rpms.model.offer import Offer
from rpms.util.db_connection import get_connection


class OfferDAO(BaseDAO):
    def _row_to_offer(self, row):
        return Offer(
            offer_id=row[0],
            application_id=row[1],
            candidate_id=row[2],
            company_id=row[3],
            designation=row[4],
            package=float(row[5]),
            offer_date=str(row[6]),
            joining_date=str(row[7]),
            offer_status=row[8],
        )

    def next_id(self):
        return self._generate_next_id("offers", "offer_id", "OFF", 101)

    def create_offer(self, offer):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO offers
                (offer_id, application_id, candidate_id, company_id, designation,
                 package, offer_date, joining_date, offer_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    offer.offer_id,
                    offer.application_id,
                    offer.candidate_id,
                    offer.company_id,
                    offer.designation,
                    offer.package,
                    offer.offer_date,
                    offer.joining_date,
                    offer.offer_status,
                ),
            )
            conn.commit()
            return offer
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, offer_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT offer_id, application_id, candidate_id, company_id, designation,
                       package, offer_date, joining_date, offer_status
                FROM offers WHERE offer_id=%s
                """,
                (offer_id,),
            )
            row = cursor.fetchone()
            return self._row_to_offer(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_by_application(self, application_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT offer_id, application_id, candidate_id, company_id, designation,
                       package, offer_date, joining_date, offer_status
                FROM offers WHERE application_id=%s
                """,
                (application_id,),
            )
            row = cursor.fetchone()
            return self._row_to_offer(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_all_offers(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT offer_id, application_id, candidate_id, company_id, designation,
                       package, offer_date, joining_date, offer_status
                FROM offers ORDER BY offer_id
                """
            )
            return [self._row_to_offer(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()

    def update_offer_status(self, offer_id, offer_status):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE offers SET offer_status=%s WHERE offer_id=%s",
                (offer_status, offer_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
            conn.close()
