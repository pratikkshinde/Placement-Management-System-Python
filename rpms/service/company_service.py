from rpms.dao.company_dao import CompanyDAO
from rpms.model.company import Company
from rpms.util.activity_logger import log_activity


class CompanyService:
    def __init__(self):
        self.company_dao = CompanyDAO()

    def add_company(self, name, location, contact_email, hr_name):
        clean_name = name.strip()
        if self.company_dao.get_by_name(clean_name) is not None:
            raise ValueError(f"Company already exists: {clean_name}")

        company_id = self.company_dao.next_id()
        company = Company(
            company_id=company_id,
            name=clean_name,
            location=location.strip(),
            contact_email=contact_email.strip(),
            hr_name=hr_name.strip(),
        )
        self.company_dao.add_company(company)
        log_activity("Company Created", company_id)
        return company

    def update_company(self, company_id, name, location, contact_email, hr_name):
        existing = self.company_dao.get_by_id(company_id)
        if existing is None:
            raise ValueError(f"Company not found: {company_id}")

        clean_name = name.strip()
        owner = self.company_dao.get_by_name(clean_name)
        if owner is not None and owner.company_id != company_id:
            raise ValueError(f"Company already exists: {clean_name}")

        updated = Company(
            company_id=company_id,
            name=clean_name,
            location=location.strip(),
            contact_email=contact_email.strip(),
            hr_name=hr_name.strip(),
        )
        self.company_dao.update_company(updated)
        log_activity("Company Updated", company_id)
        return updated

    def get_company(self, company_id):
        company = self.company_dao.get_by_id(company_id)
        if company is None:
            raise ValueError(f"Company not found: {company_id}")
        return company

    def search_companies(self, keyword):
        return self.company_dao.search_companies(keyword.strip())

    def view_all_companies(self):
        return self.company_dao.get_all_companies()
