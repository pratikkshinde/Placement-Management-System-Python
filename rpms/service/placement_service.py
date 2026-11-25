from datetime import date
from rpms.dao.offer_dao import OfferDAO
from rpms.dao.placement_dao import PlacementDAO
from rpms.model.placement import Placement
from rpms.service.application_service import ApplicationService
from rpms.util.activity_logger import log_activity


class PlacementService:
    def __init__(self):
        self.placement_dao = PlacementDAO()
        self.offer_dao = OfferDAO()
        self.application_service = ApplicationService()

    def record_placement(self, offer_id, final_package, actual_joining_date, joining_status="JOINED"):
        offer = self.offer_dao.get_by_id(offer_id)
        if offer is None:
            raise ValueError(f"Offer not found: {offer_id}")

        if offer.offer_status != "ACCEPTED":
            raise ValueError(
                f"Cannot record placement for offer with status {offer.offer_status}. "
                "Offer must be ACCEPTED."
            )

        if self.placement_dao.get_by_offer(offer_id) is not None:
            raise ValueError(f"Placement already recorded for offer: {offer_id}")

        if final_package < 0:
            raise ValueError("Final package cannot be negative.")
        try:
            date.fromisoformat(actual_joining_date.strip())
        except ValueError:
            raise ValueError("Actual joining date must be in YYYY-MM-DD format.")

        clean_status = joining_status.strip().upper()
        if clean_status not in ("JOINED", "NOT_JOINED"):
            raise ValueError("Joining status must be JOINED or NOT_JOINED.")

        placement_id = self.placement_dao.next_id()
        placement = Placement(
            placement_id=placement_id,
            offer_id=offer_id,
            application_id=offer.application_id,
            candidate_id=offer.candidate_id,
            company_id=offer.company_id,
            designation=offer.designation,
            final_package=final_package,
            actual_joining_date=actual_joining_date.strip(),
            joining_status=clean_status,
        )
        self.placement_dao.record_placement(placement)

        if clean_status == "JOINED":
            self.application_service.update_application_status(offer.application_id, "JOINED")
        else:
            self.application_service.update_application_status(offer.application_id, "REJECTED")

        log_activity("Placement Recorded", placement_id)
        return placement

    def view_all_placements(self):
        return self.placement_dao.get_all_placements()
