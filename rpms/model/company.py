class Company:
    def __init__(self, company_id, name, location, contact_email, hr_name):
        self.company_id = company_id
        self.name = name
        self.location = location
        self.contact_email = contact_email
        self.hr_name = hr_name

    def __str__(self):
        return (
            f"{self.company_id} | {self.name} | {self.location} | "
            f"{self.contact_email} | HR: {self.hr_name}"
        )
