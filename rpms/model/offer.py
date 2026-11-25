class Offer:
    def __init__(
        self,
        offer_id,
        application_id,
        candidate_id,
        company_id,
        designation,
        package,
        offer_date,
        joining_date,
        offer_status="PENDING",
    ):
        self.offer_id = offer_id
        self.application_id = application_id
        self.candidate_id = candidate_id
        self.company_id = company_id
        self.designation = designation
        self.package = float(package)
        self.offer_date = str(offer_date)
        self.joining_date = str(joining_date)
        self.offer_status = offer_status

    def __str__(self):
        return (
            f"{self.offer_id} | App: {self.application_id} | "
            f"Candidate: {self.candidate_id} | Company: {self.company_id} | "
            f"{self.designation} | {self.package} LPA | Offer: {self.offer_date} | "
            f"Joining: {self.joining_date} | {self.offer_status}"
        )
