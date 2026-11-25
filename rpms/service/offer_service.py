from datetime import date
from rpms.dao.job_dao import JobDAO
from rpms.dao.offer_dao import OfferDAO
from rpms.exception.custom_exceptions import JobNotFoundError
from rpms.model.offer import Offer
from rpms.service.application_service import ApplicationService
from rpms.util.activity_logger import log_activity


class OfferService:
    def __init__(self):
        self.offer_dao = OfferDAO()
        self.application_service = ApplicationService()
        self.job_dao = JobDAO()

    def create_offer(self, application_id, designation, package, offer_date, joining_date):
        application = self.application_service.get_application(application_id)
        if application.status != "SELECTED":
            raise ValueError(
                f"Cannot create offer when application status is {application.status}. "
                "Application must be SELECTED."
            )

        if self.offer_dao.get_by_application(application_id) is not None:
            raise ValueError(f"Offer already exists for application: {application_id}")

        if package < 0:
            raise ValueError("Package cannot be negative.")
        try:
            date.fromisoformat(offer_date.strip())
            date.fromisoformat(joining_date.strip())
        except ValueError:
            raise ValueError("Offer and joining dates must be in YYYY-MM-DD format.")

        job = self.job_dao.get_by_id(application.job_id)
        if job is None:
            raise JobNotFoundError(f"Job not found: {application.job_id}")

        offer_id = self.offer_dao.next_id()
        offer = Offer(
            offer_id=offer_id,
            application_id=application_id,
            candidate_id=application.candidate_id,
            company_id=job.company_id,
            designation=designation.strip(),
            package=package,
            offer_date=offer_date.strip(),
            joining_date=joining_date.strip(),
            offer_status="PENDING",
        )
        self.offer_dao.create_offer(offer)
        self.application_service.update_application_status(application_id, "OFFERED")
        log_activity("Offer Created", offer_id)
        return offer

    def update_offer_status(self, offer_id, offer_status):
        offer = self.offer_dao.get_by_id(offer_id)
        if offer is None:
            raise ValueError(f"Offer not found: {offer_id}")

        clean_status = offer_status.strip().upper()
        if clean_status not in ("PENDING", "ACCEPTED", "DECLINED"):
            raise ValueError("Offer status must be PENDING, ACCEPTED, or DECLINED.")

        self.offer_dao.update_offer_status(offer_id, clean_status)
        offer.offer_status = clean_status

        if clean_status == "DECLINED":
            self.application_service.update_application_status(offer.application_id, "REJECTED")

        log_activity(f"Offer {clean_status.title()}", offer_id)
        return offer

    def get_offer(self, offer_id):
        offer = self.offer_dao.get_by_id(offer_id)
        if offer is None:
            raise ValueError(f"Offer not found: {offer_id}")
        return offer

    def view_all_offers(self):
        return self.offer_dao.get_all_offers()
