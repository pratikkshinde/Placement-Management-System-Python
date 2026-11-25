from rpms.dao.base_dao import BaseDAO
from rpms.model.placement import Placement
from rpms.util.db_connection import get_connection


class PlacementDAO(BaseDAO):
    def _row_to_placement(self, row):
        return Placement(
            placement_id=row[0],
            offer_id=row[1],
            application_id=row[2],
            candidate_id=row[3],
            company_id=row[4],
            designation=row[5],
            final_package=float(row[6]),
            actual_joining_date=str(row[7]),
            joining_status=row[8],
        )

    def next_id(self):
        return self._generate_next_id("placements", "placement_id", "PLC", 101)

    def record_placement(self, placement):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO placements
                (placement_id, offer_id, application_id, candidate_id, company_id,
                 designation, final_package, actual_joining_date, joining_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    placement.placement_id,
                    placement.offer_id,
                    placement.application_id,
                    placement.candidate_id,
                    placement.company_id,
                    placement.designation,
                    placement.final_package,
                    placement.actual_joining_date,
                    placement.joining_status,
                ),
            )
            conn.commit()
            return placement
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, placement_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT placement_id, offer_id, application_id, candidate_id, company_id,
                       designation, final_package, actual_joining_date, joining_status
                FROM placements WHERE placement_id=%s
                """,
                (placement_id,),
            )
            row = cursor.fetchone()
            return self._row_to_placement(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_by_offer(self, offer_id):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT placement_id, offer_id, application_id, candidate_id, company_id,
                       designation, final_package, actual_joining_date, joining_status
                FROM placements WHERE offer_id=%s
                """,
                (offer_id,),
            )
            row = cursor.fetchone()
            return self._row_to_placement(row) if row else None
        finally:
            cursor.close()
            conn.close()

    def get_all_placements(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT placement_id, offer_id, application_id, candidate_id, company_id,
                       designation, final_package, actual_joining_date, joining_status
                FROM placements ORDER BY placement_id
                """
            )
            return [self._row_to_placement(row) for row in cursor.fetchall()]
        finally:
            cursor.close()
            conn.close()
