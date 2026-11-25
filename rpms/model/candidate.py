class Candidate:
    def __init__(
        self,
        candidate_id,
        name,
        email,
        mobile,
        technology,
        percentage,
        passing_year,
        backlogs,
        status="ACTIVE",
    ):
        self.candidate_id = candidate_id
        self.name = name
        self.email = email
        self.mobile = mobile
        self.technology = technology
        self.percentage = float(percentage)
        self.passing_year = int(passing_year)
        self.backlogs = int(backlogs)
        self.status = status

    def __str__(self):
        return (
            f"{self.candidate_id} | {self.name} | {self.email} | {self.mobile} | "
            f"{self.technology} | {self.percentage}% | Year: {self.passing_year} | "
            f"Backlogs: {self.backlogs} | {self.status}"
        )
