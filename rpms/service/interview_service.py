from datetime import date
from rpms.dao.interview_dao import InterviewDAO
from rpms.dao.job_dao import JobDAO
from rpms.exception.custom_exceptions import JobNotFoundError
from rpms.model.interview import Interview, InterviewFeedback
from rpms.service.application_service import ApplicationService
from rpms.util.activity_logger import log_activity


class InterviewService:
    def __init__(self):
        self.interview_dao = InterviewDAO()
        self.application_service = ApplicationService()
        self.job_dao = JobDAO()

    def schedule_interview(self, application_id, round_name, interview_date, mode, interviewer):
        application = self.application_service.get_application(application_id)
        if application.status not in ("SHORTLISTED", "INTERVIEW"):
            raise ValueError(
                f"Cannot schedule interview when application status is {application.status}. "
                "Application must be SHORTLISTED or INTERVIEW."
            )

        try:
            date.fromisoformat(interview_date.strip())
        except ValueError:
            raise ValueError("Interview date must be in YYYY-MM-DD format.")

        job = self.job_dao.get_by_id(application.job_id)
        if job is None:
            raise JobNotFoundError(f"Job not found: {application.job_id}")

        interview_id = self.interview_dao.next_interview_id()
        interview = Interview(
            interview_id=interview_id,
            application_id=application.application_id,
            candidate_id=application.candidate_id,
            company_id=job.company_id,
            round_name=round_name.strip(),
            interview_date=interview_date.strip(),
            mode=mode.strip(),
            interviewer=interviewer.strip(),
            status="SCHEDULED",
        )
        self.interview_dao.schedule_interview(interview)

        if application.status == "SHORTLISTED":
            self.application_service.update_application_status(application_id, "INTERVIEW")

        log_activity("Interview Scheduled", interview_id)
        return interview

    def record_feedback(self, interview_id, technical_rating, communication_rating, remarks, result):
        interview = self.interview_dao.get_by_id(interview_id)
        if interview is None:
            raise ValueError(f"Interview not found: {interview_id}")

        if self.interview_dao.get_feedback_by_interview(interview_id) is not None:
            raise ValueError(f"Feedback already recorded for interview: {interview_id}")

        if technical_rating < 1 or technical_rating > 10:
            raise ValueError("Technical rating must be between 1 and 10.")
        if communication_rating < 1 or communication_rating > 10:
            raise ValueError("Communication rating must be between 1 and 10.")

        clean_result = result.strip().upper()
        if clean_result not in ("SELECTED", "REJECTED", "NEXT_ROUND"):
            raise ValueError("Result must be SELECTED, REJECTED, or NEXT_ROUND.")

        feedback_id = self.interview_dao.next_feedback_id()
        feedback = InterviewFeedback(
            feedback_id=feedback_id,
            interview_id=interview_id,
            technical_rating=technical_rating,
            communication_rating=communication_rating,
            remarks=remarks.strip(),
            result=clean_result,
        )
        self.interview_dao.add_feedback(feedback)
        self.interview_dao.update_interview_status(interview_id, "COMPLETED")

        if clean_result in ("SELECTED", "REJECTED"):
            self.application_service.update_application_status(
                interview.application_id, clean_result
            )

        log_activity("Interview Feedback Recorded", feedback_id)
        return feedback

    def view_all_interviews(self):
        return self.interview_dao.get_all_interviews()

    def get_feedback(self, interview_id):
        return self.interview_dao.get_feedback_by_interview(interview_id)
