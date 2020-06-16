""" Main pipeline for COVID-19 Climate Impact Predictor.

    Loading pre-trained models, retrain models and classify data.
"""

import sys
import os
import numpy as np


class PredictorPipeline(object):

    def __init__(self):
        """ Initilize session.

            Load model etc.
        """
        print("Hello, COVID-19")

    def readData(self):
        """ Read in data used to classify or train. 

            Preprocess data etc.
        """
        print("Hello, Data")

    def trainClassifier(self):
        """ Train classifier xyz with data xyz. """
        print("Hello, Classifier")

    def classifyData(self):
        """ Predict emission for a specific model and analyse results. """
        print("Hello, Classificaiton")
