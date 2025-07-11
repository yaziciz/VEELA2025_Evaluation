# Configuration file for VEELA
API_KEY = "<your synapse API key>"

CHALLENGE_IDS = {"Segmentation": "9615787", "Classification": "9615788"}

TABLE_ID_TASK1 = "syn68642629"
TABLE_ID_TASK2 = "syn68642631"

CHECK_INTERVAL = 3600  # seconds

class NotificationType:
    INFO_SUCCESS_T1 = (
        "Dear {team_name},\n\n"
        "You can find the average test set evaluation scores for your submission {submission_id} (Task 1 - Segmentation) below:\n\n"
        "{{\"Average\", \"clDice\": {clDice}, \"IoU\": {IoU}, \"NSD\": {NSD}}}\n\n"
        "The score can be seen in the Results table here: https://www.synapse.org/Synapse:syn65471967/wiki/632178 \n\n"
        "Kind regards,\n\n"
        "The VEELA 2025 Organization Team"
    )
    INFO_SUCCESS_T2 = (
        "Dear {team_name},\n\n"
        "You can find the average test set evaluation scores for your submission {submission_id} (Task 1 - Classification) below:\n\n"
        "{{\"clDice\": {{\"hepatic\": {clDice_hepatic}, \"portal\": {clDice_portal}}}, "
        "\"IoU\": {{\"hepatic\": {IoU_hepatic}, \"portal\": {IoU_portal}}}, "
        "\"NSD\": {{\"hepatic\": {NSD_hepatic}, \"portal\": {NSD_portal}}}}}\n\n"    
        "The score can be seen in the Results table here: https://www.synapse.org/Synapse:syn65471967/wiki/632178 \n\n"
        "Kind regards,\n\n"
        "The VEELA 2025 Organization Team"
    )
    INFO_FAILURE_E1 = (
        "The folder {folder_path} does not exist. Please make sure that the folder structure and naming is correct, and the files are placed in the correct directories as shown under the \"Submission Tutorial\" section of the challenge page."
    )
    INFO_FAILURE_E2 = (
        "The number of test files in the folder is not 20. All test cases should be submitted in the same folder, and the files should be named as 'case_1.nii', 'case_2.nii', ..., 'case_{expected_count}.nii'. For more information, please refer to the 'Submission Tutorial' section of the challenge page."
    )
    INFO_FAILURE_E3 = "The file {file_path} could not be loaded. Please ensure that the file is in the correct format, has the correct naming format, and contains valid data. For more information, please refer to the 'Submission Tutorial' section of the challenge page."
    INFO_FAILURE_E4 = "The prediction volume {file_path} does not have 2 labels (0 and 1). Please ensure that the prediction volume is a binary segmentation mask with only two labels: 0 for background and 1 for the object of interest. For more information, please refer to the 'Submission Tutorial' section of the challenge page."
    INFO_FAILURE_E5 = "The prediction volume {file_path} does not have 3 labels. Please ensure that the prediction volume is a multi-class segmentation mask with three labels: 0 for background, 1 for hepatic, and 2 for portal. For more information, please refer to the 'Submission Tutorial' section of the challenge page."

    @staticmethod
    def format(message, **kwargs):
        if isinstance(message, str):
            return message.format(**kwargs)
        return message
    

SUBJECT_TASK1_SCORES = "[VEELA 2025] Submission ID: {submission_id} (Task 1) - Evaluation Scores"
SUBJECT_TASK2_SCORES = "[VEELA 2025] Submission ID: {submission_id} (Task 2) - Evaluation Scores"

SUBJECT_TASK1_FAILED = "[VEELA 2025] Submission ID: {submission_id} (Task 1) - Evaluation Failed"
SUBJECT_TASK2_FAILED = "[VEELA 2025] Submission ID: {submission_id} (Task 2) - Evaluation Failed"
