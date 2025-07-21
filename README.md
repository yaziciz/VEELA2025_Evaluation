### VEELA 2025 - Vessel Extraction and Extrication for Liver
Accurate analysis of liver vasculature in three dimensions (3D) is essential for a variety of medical procedures including computer-aided diagnosis, treatment planning, or pre-operative planning of hepatic diseases. Pre-surgical planning for living donated liver transplantation requires precise knowledge of the liver vascular morphology. Likewise, the localization of liver lesions is based on the lesion’s relative position to the surrounding hepatic vessels. Moreover, it is also used for medical education, which significantly benefits from advanced models and realistic simulations. A complete analysis of the liver vasculature implies the analysis of three-vessel types:

1- Hepatic vessels that transport deoxygenated blood from the liver to the heart,
2- Portal vessels that transport nutrient-rich blood from intestines to the liver,
3- The hepatic artery that carries oxygenated blood from the heart to the liver.

During routine clinical workflow, vessel segmentation is mostly carried out by radiologists, who manually annotate all vessels on abdominal multi-slice computed tomography angiography (CTA) images in DICOM format. This process is tedious, time-consuming work that is prone to high intra- and inter-expert variability. This creates the need for an accurate, fully automated vessel segmentation method. In this context, the VEELA challenge has two goals:

1- Segmentation of liver vasculature,
2- Classification of hepatic and portal vessels.
(Note: hepatic arteries were not included in the scope of this challenge)

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

This repository includes the evaluation scripts utilized in the challenge.
