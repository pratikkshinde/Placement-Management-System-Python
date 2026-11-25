class Interview:
    def __init__(
        self,
        interview_id,
        application_id,
        candidate_id,
        company_id,
        round_name,
        interview_date,
        mode,
        interviewer,
        status="SCHEDULED",
    ):
        self.interview_id = interview_id
        self.application_id = application_id
        self.candidate_id = candidate_id
        self.company_id = company_id
        self.round_name = round_name
        self.interview_date = str(interview_date)
        self.mode = mode
        self.interviewer = interviewer
        self.status = status

    def __str__(self):
        return (
            f"{self.interview_id} | App: {self.application_id} | "
            f"Candidate: {self.candidate_id} | Company: {self.company_id} | "
            f"Round: {self.round_name} | Date: {self.interview_date} | "
            f"Mode: {self.mode} | Interviewer: {self.interviewer} | {self.status}"
        )


class InterviewFeedback:
    def __init__(
        self,
        feedback_id,
        interview_id,
        technical_rating,
        communication_rating,
        remarks,
        result,
    ):
        self.feedback_id = feedback_id
        self.interview_id = interview_id
        self.technical_rating = int(technical_rating)
        self.communication_rating = int(communication_rating)
        self.remarks = remarks
        self.result = result

    def __str__(self):
        return (
            f"{self.feedback_id} | Interview: {self.interview_id} | "
            f"Tech: {self.technical_rating}/10 | Comm: {self.communication_rating}/10 | "
            f"Result: {self.result} | Remarks: {self.remarks}"
        )
