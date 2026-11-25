class Placement:
    def __init__(
        self,
        placement_id,
        offer_id,
        application_id,
        candidate_id,
        company_id,
        designation,
        final_package,
        actual_joining_date,
        joining_status="JOINED",
    ):
        self.placement_id = placement_id
        self.offer_id = offer_id
        self.application_id = application_id
        self.candidate_id = candidate_id
        self.company_id = company_id
        self.designation = designation
        self.final_package = float(final_package)
        self.actual_joining_date = str(actual_joining_date)
        self.joining_status = joining_status

    def __str__(self):
        return (
            f"{self.placement_id} | Offer: {self.offer_id} | "
            f"Candidate: {self.candidate_id} | Company: {self.company_id} | "
            f"{self.designation} | {self.final_package} LPA | "
            f"Joined: {self.actual_joining_date} | {self.joining_status}"
        )
