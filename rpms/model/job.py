class Job:
    def __init__(
        self,
        job_id,
        company_id,
        job_title,
        technology,
        openings,
        location,
        package,
        min_percentage,
        passing_year,
        max_backlogs,
        deadline,
        status="OPEN",
    ):
        self.job_id = job_id
        self.company_id = company_id
        self.job_title = job_title
        self.technology = technology
        self.openings = int(openings)
        self.location = location
        self.package = float(package)
        self.min_percentage = float(min_percentage)
        self.passing_year = int(passing_year)
        self.max_backlogs = int(max_backlogs)
        self.deadline = str(deadline)
        self.status = status

    def __str__(self):
        return (
            f"{self.job_id} | Company: {self.company_id} | {self.job_title} | "
            f"{self.technology} | Openings: {self.openings} | {self.location} | "
            f"Pkg: {self.package} LPA | Min %: {self.min_percentage} | "
            f"Year: {self.passing_year} | Max Backlogs: {self.max_backlogs} | "
            f"Deadline: {self.deadline} | {self.status}"
        )
