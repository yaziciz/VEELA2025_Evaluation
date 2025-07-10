from synapseclient import Synapse

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
        team = self.synapse.getTeam(submission.teamId)
        return team.name

    def update_submission_status(self, submission, status="SCORED"):
        submission_status = self.synapse.getSubmissionStatus(submission)
        submission_status.status = status
        self.synapse.store(submission_status)

    def send_results_to_table(self, submission, results):
        # This method can be implemented to send results to a Synapse table
        # For now, it is a placeholder
        print(f"Results for submission {submission.id} from team {self.get_team_name(submission)}: {results}")
        # You can implement the logic to store results in a Synapse table here