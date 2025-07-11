from VEELA_Test_Metrics import metrics
import os
import json
import numpy as np
from nibabel import load
from config import NotificationType

class TaskEvaluator:
    def __init__(self, folder_base, task_name, save_to_json=True):
        self.folder_base = folder_base
        self.task_name = task_name
        self.save_to_json = save_to_json
        self.samplewise_scores = []

    def evaluate(self):

        for root, dirs, files in os.walk(self.folder_base):
            dirs[:] = [d for d in dirs if not d.startswith('_')]  # skip dirs starting with "_"
            
            if self.task_name in dirs:
                self.folder_path = os.path.join(root, self.task_name)
                self.folder_base = self.folder_path
                break

        if not os.path.exists(self.folder_base) and not os.path.exists(os.path.join(self.folder_base, "Results", self.task_name)):
            return False, NotificationType.INFO_FAILURE_E1.format(folder_path=os.path.join("Results", self.task_name))

        nii_files = [file for file in os.listdir(self.folder_base) if file.endswith(".nii")]
        if len(nii_files) != 20:
            print(f"The number of test files in the folder is not 20!")
            return False, NotificationType.INFO_FAILURE_E2

        for file in nii_files:
            file_path = os.path.join(self.folder_base, file)
            status, message = self.process_file(file, file_path)
            if not status:
                return False, message

        self.calculate_average_scores()
        results = self.get_results(save_to_json=self.save_to_json)
        return results, ""

    def process_file(self, file, file_path):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def calculate_average_scores(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def get_results(self, save_to_json=True):
        output_path = os.path.join(self.folder_base, "evaluation.json")
        with open(output_path, "w") as f:
            json.dump(self.samplewise_scores, f, indent=4)


class Task1Evaluator(TaskEvaluator):
    def process_file(self, file, file_path):
        try:
            prediction_vol = load(file_path).get_fdata().round().astype(int)
            ground_truth_vol = load(os.path.join("./Test_GT", file_path.split('/')[-1].replace(".", "_gt."))).get_fdata().astype(bool)
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return False, NotificationType.INFO_FAILURE_E3.format(file_path=file_path)
        
        if len(np.unique(prediction_vol)) != 2 or not np.array_equal(np.unique(prediction_vol), [0, 1]):
            print(f"Prediction volume {file_path} does not have 2 labels (0 and 1).")
            return False, NotificationType.INFO_FAILURE_E4.format(file_path=file_path)

        cli_dice, iou, nsd = metrics.compute_metrics(prediction_vol, ground_truth_vol)
        self.samplewise_scores.append({
            "sampleId": file,
            "clDice": cli_dice,
            "IoU": iou,
            "NSD": nsd
        })

        return True, ""

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

    def get_results(self, save_to_json=True):
        super().get_results(save_to_json=save_to_json)

        #get last element of samplewise_scores
        last_score = self.samplewise_scores[-1]
        return {"ID": "",
                "Created By": "",
                "clDice": last_score["clDice"],
                "IoU": last_score["IoU"],
                "NSD": last_score["NSD"]}
    
class Task2Evaluator(TaskEvaluator):
    def process_file(self, file, file_path):
        try:
            prediction_vol = load(file_path).get_fdata().round().astype(int)
            ground_truth_vol = load(os.path.join("./Test_GT", file_path.split('/')[-1].replace(".", "_gt."))).get_fdata()
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return False, NotificationType.INFO_FAILURE_E3.format(file_path=file_path)

        if len(np.unique(prediction_vol)) != 3:
            print(f"Prediction volume {file_path} does not have 3 labels.")
            return False, NotificationType.INFO_FAILURE_E5.format(file_path=file_path)

        prediction_vol_hepatic = np.where(prediction_vol == 1, 1, 0).astype(bool)
        ground_truth_vol_hepatic = np.where(ground_truth_vol == 1, 1, 0).astype(bool)

        prediction_vol_portal = np.where(prediction_vol == 2, 1, 0).astype(bool)
        ground_truth_vol_portal = np.where(ground_truth_vol == 2, 1, 0).astype(bool)

        cli_dice_hepatic, iou_hepatic, nsd_hepatic = metrics.compute_metrics(prediction_vol_hepatic, ground_truth_vol_hepatic)
        cli_dice_portal, iou_portal, nsd_portal = metrics.compute_metrics(prediction_vol_portal, ground_truth_vol_portal)

        self.samplewise_scores.append({
            "sampleId": file,
            "clDice": {"hepatic": cli_dice_hepatic, "portal": cli_dice_portal},
            "IoU": {"hepatic": iou_hepatic, "portal": iou_portal},
            "NSD": {"hepatic": nsd_hepatic, "portal": nsd_portal},
        })

        return True, ""

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

    def get_results(self, save_to_json=True):
        super().get_results(save_to_json=save_to_json)

        last_score = self.samplewise_scores[-1]
        return {
            "ID": "",
            "Created By": "",
            "clDice_hepatic": last_score["clDice"]["hepatic"],
            "clDice_portal": last_score["clDice"]["portal"],
            "IoU_hepatic": last_score["IoU"]["hepatic"],
            "IoU_portal": last_score["IoU"]["portal"],
            "NSD_hepatic": last_score["NSD"]["hepatic"],
            "NSD_portal": last_score["NSD"]["portal"]
        }