from synapseclient import Synapse
import os
import json
import numpy as np
from nibabel import load

class SynapseEvaluator:
    def __init__(self, auth_token):
        self.synapse = Synapse()
        self.synapse.login(authToken=auth_token)

    def get_submission(self, submission_id):
        return self.synapse.getSubmission(submission_id)

    def update_submission_status(self, submission):
        submission_status = self.synapse.getSubmissionStatus(submission)
        submission_status.status = "SCORED"
        self.synapse.store(submission_status)


class TaskEvaluator:
    def __init__(self, folder_path, metrics_module):
        self.folder_path = folder_path
        self.metrics = metrics_module
        self.samplewise_scores = []

    def evaluate(self):
        if not os.path.exists(self.folder_path):
            print(f"Folder {self.folder_path} does not exist!")
            return

        nii_files = [file for file in os.listdir(self.folder_path) if file.endswith(".nii")]
        if len(nii_files) != 20:
            print(f"The number of test files in the folder is not 20!")
            return

        for file in nii_files:
            file_path = os.path.join(self.folder_path, file)
            self.process_file(file, file_path)

        self.calculate_average_scores()
        self.save_results()

    def process_file(self, file, file_path):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def calculate_average_scores(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def save_results(self):
        output_path = os.path.join(self.folder_path, "evaluation.json")
        with open(output_path, "w") as f:
            json.dump(self.samplewise_scores, f, indent=4)


class Task1Evaluator(TaskEvaluator):
    def process_file(self, file, file_path):
        try:
            prediction_vol = load(file_path).get_fdata().astype(bool)
            ground_truth_vol = load(file_path).get_fdata().astype(bool)
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return

        cli_dice, iou, nsd = self.metrics.compute_metrics(prediction_vol, ground_truth_vol)
        self.samplewise_scores.append({
            "sampleId": file,
            "clDice": cli_dice,
            "IoU": iou,
            "NSD": nsd
        })

    def calculate_average_scores(self):
        average_scores = {
            "clDice": np.mean([score["clDice"] for score in self.samplewise_scores]),
            "IoU": np.mean([score["IoU"] for score in self.samplewise_scores]),
            "NSD": np.mean([score["NSD"] for score in self.samplewise_scores])
        }
        self.samplewise_scores.append({
            "sampleId": "Average",
            "clDice": average_scores["clDice"],
            "IoU": average_scores["IoU"],
            "NSD": average_scores["NSD"]
        })


class Task2Evaluator(TaskEvaluator):
    def process_file(self, file, file_path):
        try:
            prediction_vol = load(file_path).get_fdata()
            ground_truth_vol = load(file_path).get_fdata()
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return

        if len(np.unique(prediction_vol)) != 3:
            print(f"Prediction volume {file_path} does not have 3 labels.")
            return

        prediction_vol_hepatic = np.where(prediction_vol == 1, 1, 0).astype(bool)
        ground_truth_vol_hepatic = np.where(ground_truth_vol == 1, 1, 0).astype(bool)

        prediction_vol_portal = np.where(prediction_vol == 2, 1, 0).astype(bool)
        ground_truth_vol_portal = np.where(ground_truth_vol == 2, 1, 0).astype(bool)

        cli_dice_hepatic, iou_hepatic, nsd_hepatic = self.metrics.compute_metrics(prediction_vol_hepatic, ground_truth_vol_hepatic)
        cli_dice_portal, iou_portal, nsd_portal = self.metrics.compute_metrics(prediction_vol_portal, ground_truth_vol_portal)

        self.samplewise_scores.append({
            "sampleId": file,
            "clDice": {"hepatic": cli_dice_hepatic, "portal": cli_dice_portal},
            "IoU": {"hepatic": iou_hepatic, "portal": iou_portal},
            "NSD": {"hepatic": nsd_hepatic, "portal": nsd_portal},
        })

    def calculate_average_scores(self):
        average_scores = {
            "clDice": {
                "hepatic": np.mean([score["clDice"]["hepatic"] for score in self.samplewise_scores]),
                "portal": np.mean([score["clDice"]["portal"] for score in self.samplewise_scores])
            },
            "IoU": {
                "hepatic": np.mean([score["IoU"]["hepatic"] for score in self.samplewise_scores]),
                "portal": np.mean([score["IoU"]["portal"] for score in self.samplewise_scores])
            },
            "NSD": {
                "hepatic": np.mean([score["NSD"]["hepatic"] for score in self.samplewise_scores]),
                "portal": np.mean([score["NSD"]["portal"] for score in self.samplewise_scores])
            }
        }
        self.samplewise_scores.append({
            "sampleId": "Average",
            "clDice": average_scores["clDice"],
            "IoU": average_scores["IoU"],
            "NSD": average_scores["NSD"]
        })