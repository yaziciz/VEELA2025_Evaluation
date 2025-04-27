from VEELA_Test_Metrics import metrics
from evaluator import SynapseEvaluator, Task1Evaluator, Task2Evaluator
import os
from config import *

if __name__ == "__main__":
    # Synapse authentication
    synapse_evaluator = SynapseEvaluator(API_KEY)
    # Create a folder for submissions
    os.makedirs("Submissions/" + str(SUBMISSION_ID), exist_ok=True)

    #Download the submission
    submission = synapse_evaluator.get_submission(SUBMISSION_ID)

    submission_file_path = submission.filePath    
    os.chdir(os.curdir)
    os.system(f"unzip {submission_file_path} -d Submissions/" + str(SUBMISSION_ID))

    # Task 1 evaluation
    folder_task1 = "./Submissions/"+str(SUBMISSION_ID)+"/Results/Task01"
    task1_evaluator = Task1Evaluator(folder_task1, metrics)
    task1_evaluator.evaluate()

    # Task 2 evaluation
    folder_task2 = "./Submissions/"+str(SUBMISSION_ID)+"/Results/Task02"
    task2_evaluator = Task2Evaluator(folder_task2, metrics)
    task2_evaluator.evaluate()

    # Update submission status
    synapse_evaluator.update_submission_status(submission)
