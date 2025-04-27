# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:18:51 2024

@author: Bio İzmir
"""
import nibabel as nib
import VEELA_Test_Metrics.clDice as clDice
from sklearn.metrics import jaccard_score
import surface_distance

"""
GTVolume : Ground-Truth Volume as boolean
MaskVolume : Predicted Volume as boolean
"""

def compute_metrics(GTVolume, MaskVolume):
    cliDiceMetric = clDice.clDice(GTVolume, MaskVolume)
    IoU = jaccard_score(GTVolume.flatten(), MaskVolume.flatten())

    surface_distances = surface_distance.compute_surface_distances(GTVolume, MaskVolume, spacing_mm=(3,2,1))
    NSD = surface_distance.compute_surface_dice_at_tolerance(surface_distances, tolerance_mm=1)

    return cliDiceMetric, IoU, NSD

