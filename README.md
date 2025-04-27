# VEELA 2025 Evaluation
This repository contains the evaluation scripts of the VEELA 2025 Challenge.

### VEELA 2025 - Vessel Extraction and Extrication for Liver
Accurate analysis of liver vasculature in three dimensions (3D) is essential for a variety of medical procedures including computer-aided diagnosis, treatment planning, or pre-operative planning of hepatic diseases. Pre-surgical planning for living donated liver transplantation requires precise knowledge of the liver vascular morphology. Likewise, the localization of liver lesions is based on the lesion’s relative position to the surrounding hepatic vessels. Moreover, it is also used for medical education, which significantly benefits from advanced models and realistic simulations. A complete analysis of the liver vasculature implies the analysis of three-vessel types:

* Hepatic vessels that transport deoxygenated blood from the liver to the heart,
* Portal vessels that transport nutrient-rich blood from intestines to the liver,
* The hepatic artery that carries oxygenated blood from the heart to the liver.

The VEELA challenge has two sub-branches:

* Segmentation of liver vasculature.
* Classification of hepatic and portal vessels.

For more information: [Synapse Page of VEELA 2025](https://www.synapse.org/Synapse:syn65471967/wiki/631203)


**Evaluation Metrics ✅**

Three evaluation metrics based on literature research and the “Metrics Reloaded" website will be used for the ranking of the submissions:

- Localization Criterion:  
Mask Intersection over Union (Mask IoU)
https://metrics-reloaded.dkfz.de/metric?id=mask_iou

- Overlap-based Metric - Centerline Dice:
clDice is calculated on the intersection of the segmentation masks and their (morphological) skeleta.
https://metrics-reloaded.dkfz.de/metric?id=cl_dice

- Boundary-based Metric: Normalized Surface Distance (NSD)
https://metrics-reloaded.dkfz.de/metric?id=normalized_surface_distance
