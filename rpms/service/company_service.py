from rpms.dao.company_dao import CompanyDAO
from rpms.model.company import Company
from rpms.util.activity_logger import log_activity
from rpms.util.validation import require_non_empty, validate_email


class CompanyService:
    def __init__(self):
        self.company_dao = CompanyDAO()

    def _validate_company_fields(self, name, location, contact_email, hr_name):
        clean_name = require_non_empty(name, "Company name")
        clean_location = require_non_empty(location, "Location")
        clean_email = validate_email(contact_email, "Contact email")
        clean_hr = require_non_empty(hr_name, "HR name")
        return clean_name, clean_location, clean_email, clean_hr

    def add_company(self, name, location, contact_email, hr_name):
        clean_name, clean_location, clean_email, clean_hr = self._validate_company_fields(
            name, location, contact_email, hr_name
        )
        if self.company_dao.get_by_name(clean_name) is not None:
            raise ValueError(f"Company already exists: {clean_name}")

        company_id = self.company_dao.next_id()
        company = Company(
            company_id=company_id,
            name=clean_name,
            location=clean_location,
            contact_email=clean_email,
            hr_name=clean_hr,
        )
        self.company_dao.add_company(company)
        log_activity("Company Created", company_id)
        return company

    def update_company(self, company_id, name, location, contact_email, hr_name):
        clean_id = require_non_empty(company_id, "Company ID")
        existing = self.company_dao.get_by_id(clean_id)
        if existing is None:
            raise ValueError(f"Company not found: {clean_id}")

        clean_name, clean_location, clean_email, clean_hr = self._validate_company_fields(
            name, location, contact_email, hr_name
        )
        owner = self.company_dao.get_by_name(clean_name)
        if owner is not None and owner.company_id != clean_id:
            raise ValueError(f"Company already exists: {clean_name}")

        updated = Company(
            company_id=clean_id,
            name=clean_name,
            location=clean_location,
            contact_email=clean_email,
            hr_name=clean_hr,
        )
        self.company_dao.update_company(updated)
        log_activity("Company Updated", clean_id)
        return updated

    def get_company(self, company_id):
        clean_id = require_non_empty(company_id, "Company ID")
        company = self.company_dao.get_by_id(clean_id)
        if company is None:
            raise ValueError(f"Company not found: {clean_id}")
        return company

    def search_companies(self, keyword):
        return self.company_dao.search_companies(require_non_empty(keyword, "Search keyword"))

    def view_all_companies(self):
        return self.company_dao.get_all_companies()
