from rpms.dao.job_dao import JobDAO
from rpms.dao.offer_dao import OfferDAO
from rpms.exception.custom_exceptions import JobNotFoundError
from rpms.model.offer import Offer
from rpms.service.application_service import ApplicationService
from rpms.util.activity_logger import log_activity
from rpms.util.validation import require_non_empty, validate_iso_date


class OfferService:
    def __init__(self):
        self.offer_dao = OfferDAO()
        self.application_service = ApplicationService()
        self.job_dao = JobDAO()

    def create_offer(self, application_id, designation, package, offer_date, joining_date):
        clean_app_id = require_non_empty(application_id, "Application ID")
        clean_designation = require_non_empty(designation, "Designation")

        if package <= 0:
            raise ValueError("Package must be greater than 0.")

        parsed_offer_date = validate_iso_date(offer_date, "Offer date")
        parsed_joining_date = validate_iso_date(joining_date, "Joining date")
        if parsed_joining_date < parsed_offer_date:
            raise ValueError("Joining date cannot be earlier than offer date.")

        application = self.application_service.get_application(clean_app_id)
        if application.status != "SELECTED":
            raise ValueError(
                f"Cannot create offer when application status is {application.status}. "
                "Application must be SELECTED."
            )

        if self.offer_dao.get_by_application(clean_app_id) is not None:
            raise ValueError(f"Offer already exists for application: {clean_app_id}")

        job = self.job_dao.get_by_id(application.job_id)
        if job is None:
            raise JobNotFoundError(f"Job not found: {application.job_id}")

        offer_id = self.offer_dao.next_id()
        offer = Offer(
            offer_id=offer_id,
            application_id=clean_app_id,
            candidate_id=application.candidate_id,
            company_id=job.company_id,
            designation=clean_designation,
            package=package,
            offer_date=str(parsed_offer_date),
            joining_date=str(parsed_joining_date),
            offer_status="PENDING",
        )
        self.offer_dao.create_offer(offer)
        self.application_service.update_application_status(clean_app_id, "OFFERED")
        log_activity("Offer Created", offer_id)
        return offer

    def update_offer_status(self, offer_id, offer_status):
        clean_offer_id = require_non_empty(offer_id, "Offer ID")
        offer = self.offer_dao.get_by_id(clean_offer_id)
        if offer is None:
            raise ValueError(f"Offer not found: {clean_offer_id}")

        clean_status = require_non_empty(offer_status, "Offer status").upper()
        if clean_status not in ("PENDING", "ACCEPTED", "DECLINED"):
            raise ValueError("Offer status must be PENDING, ACCEPTED, or DECLINED.")

        self.offer_dao.update_offer_status(clean_offer_id, clean_status)
        offer.offer_status = clean_status

        if clean_status == "DECLINED":
            self.application_service.update_application_status(offer.application_id, "REJECTED")

        log_activity(f"Offer {clean_status.title()}", clean_offer_id)
        return offer

    def get_offer(self, offer_id):
        clean_offer_id = require_non_empty(offer_id, "Offer ID")
        offer = self.offer_dao.get_by_id(clean_offer_id)
        if offer is None:
            raise ValueError(f"Offer not found: {clean_offer_id}")
        return offer

    def view_all_offers(self):
        return self.offer_dao.get_all_offers()
