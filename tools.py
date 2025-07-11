import synapseclient
from synapseclient import Synapse
import pandas as pd
from config import *

class SynapseInterface:
    def __init__(self, auth_token):
        self.synapse = Synapse()
        self.synapse.login(authToken=auth_token)

    def get_submission_IDs(self, challenge_id):
        submissions = self.synapse.getSubmissions(challenge_id, status="RECEIVED")
        return [sub.id for sub in submissions]

    def get_submission(self, submission_id):
        return self.synapse.getSubmission(submission_id)
    
    def get_team_name(self, submission):
        if not hasattr(submission, 'teamId'):
            #get user name if no team is associated
            user = self.synapse.getUserProfile(submission.userId)
            return user.userName
        else:
            team = self.synapse.getTeam(submission.teamId)
            return team.name

    def update_submission_status(self, submission, status="SCORED"):
        submission_status = self.synapse.getSubmissionStatus(submission)
        submission_status.status = status
        self.synapse.store(submission_status)

    def send_results_to_table(self, submission, results, table_ID, send_email=False):
        #Add team name to results
        results['Created By'] = "@" + self.get_team_name(submission)
        results['ID'] = submission.id

        results_df = pd.DataFrame([results])
        row = synapseclient.Table(table_ID, results_df)
        self.synapse.store(row)
        print(f"Results for submission {submission.id} have been sent to the table {table_ID}.")

        if send_email:
            subject = SUBJECT_TASK1_SCORES.format(submission_id=submission.id) if table_ID == TABLE_ID_TASK1 else SUBJECT_TASK2_SCORES.format(submission_id=submission.id)
            message = NotificationType.format(
                NotificationType.INFO_SUCCESS_T1 if table_ID == TABLE_ID_TASK1 else NotificationType.INFO_SUCCESS_T2,
                team_name=self.get_team_name(submission),
                submission_id=submission.id,
                **results
            )
            self.send_email_notification(submission, subject, message)

    def send_email_notification(self, submission, subject, message):
        if not hasattr(submission, 'teamId'):
            recipient = submission.userId
        else:
            recipient = submission.teamId

        #self.synapse.sendMessage(userIds=[recipient], messageSubject=subject, messageBody=message)
        print(f"Email sent to {recipient} for submission {submission.id}.")