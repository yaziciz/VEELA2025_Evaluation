# %%
from evaluator import Task1Evaluator, Task2Evaluator
import os
from config import *

# %%
def run(synapse_interface, challenge_name, submission_id):
    """Run the evaluation process. """

    os.makedirs("Submissions/" + str(submission_id), exist_ok=True)
    
    #Download the submission
    submission = synapse_interface.get_submission(submission_id)

    submission_file_path = submission.filePath    
    os.chdir(os.curdir)
    os.system(f"unzip {submission_file_path} -d Submissions/" + str(submission_id))
    os.remove(submission_file_path)

    if(challenge_name == "Segmentation"):
        print("Evaluating Segmentation (Task 1) Challenge")

        # Task 1 evaluation
        folder_task1 = "./Submissions/"+str(submission_id)+"/Results/Task01"
        task1_evaluator = Task1Evaluator(folder_task1, save_to_json=False)
        results, message = task1_evaluator.evaluate()

        if results:
            #send the results to a table in Synapse
            synapse_interface.send_results_to_table(submission, results, TABLE_ID_TASK1, send_email=True)
            synapse_interface.update_submission_status(submission, status="SCORED")
        else:
            print("Evaluation failed for Task 1.")
            synapse_interface. send_email_notification(submission, subject=SUBJECT_TASK1_FAILED.format(submission_id=submission.id), message=message)
            synapse_interface.update_submission_status(submission, status="INVALID")

        print("Task 1 evaluation has been completed.")

    elif(challenge_name == "Classification"):
        print("Evaluating Classification (Task 2) Challenge")

        # Task 2 evaluation
        folder_task2 = "./Submissions/"+str(submission_id)+"/Results/Task02"
        task2_evaluator = Task2Evaluator(folder_task2, save_to_json=False)
        results = task2_evaluator.evaluate()

        if results:
            #send the results to a table in Synapse
            synapse_interface.send_results_to_table(submission, results, TABLE_ID_TASK2, send_email=True)
            synapse_interface.update_submission_status(submission, status="SCORED")
        else:
            print("Evaluation failed for Task 2.")
            synapse_interface.send_email_notification(submission, subject=SUBJECT_TASK2_FAILED.format(submission_id=submission.id), message=message)
            synapse_interface.update_submission_status(submission, status="INVALID")
