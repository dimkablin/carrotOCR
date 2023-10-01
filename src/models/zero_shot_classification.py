""" Zero Shot Classification model """
from typing import List
from transformers import pipeline


class ZeroShotClassificationModel:
    """ Zero Shot Classification init class"""
    def __init__(self):
        self.task = "zero-shot-classification"
        self.model = "cointegrated/rubert-base-cased-nli-threeway"

        self.path_to_classes = "models/zero-shot-classification/classes.txt"
        self.classes = []
        self.read_classes(self.path_to_classes)

        self.pipe = pipeline(self.task, self.model)

    def read_classes(self, path) -> None:
        """ Read text classes from file
        :param path: Path to the file with classes that seperated with new line
        :return: None
        """
        with open(path, 'r', encoding='utf-8') as file:
            classes = file.readlines()

        self.classes = [cls.rstrip('\n') for cls in classes]

    def __call__(self, inputs: List[str], n_out: int = 5):
        """ Perform zero-shot classification on a list of input texts.

        :param inputs: List of input texts to classify.
        :param n_out: Number of top classification results to return (default is 5).
        :return: List of dictionaries containing classification results.
                 Each dictionary includes "labels" and "scores".
        """

        outputs = self.pipe(inputs, candidate_labels=self.classes)

        results = []
        for output in outputs:
            results.append({
                "labels": output["labels"][:n_out],
                "scores": output["scores"][:n_out]
            })

        return results

    def __str__(self):
        return f"Task {self.task}, Model {self.model}"
