class Application:
    def __init__(self, application_id, candidate_id, job_id, applied_date, status="APPLIED"):
        self.application_id = application_id
        self.candidate_id = candidate_id
        self.job_id = job_id
        self.applied_date = str(applied_date)
        self.status = status

    def __str__(self):
        return (
            f"{self.application_id} | Candidate: {self.candidate_id} | "
            f"Job: {self.job_id} | Date: {self.applied_date} | Status: {self.status}"
        )
