#pylint: disable=E
""" Find Tags model """
import json
from typing import Optional

import Levenshtein
from src.db.permatags_manager import PermatagsManager, PermatagsStructure


class FindTags:
    """ Zero Shot Classification init class"""
    def __init__(self):
        self.path_to_classes = "./models/zero-shot-classification/classes.json"
        self.values = []
        self.keys = []
        self.scores = {}
        self.read_classes(self.path_to_classes)


    def read_classes(self, path) -> None:
        """ Read text classes from file
        :param path: Path to the file with classes that seperated with new line
        :return: None
        """
        with open(path, "r", encoding='utf-8') as file:
            data = json.load(file)
            self.values = list(data.values())
            self.keys = list(data.keys())
            self.scores = {k:0 for k in range(len(self.values))}


    def add_perma_tags(self, tags: list[str]) -> None:
        """ Add tags to the database"""
        for tag in tags:
            data = PermatagsStructure(
                tag=tag
            )
            PermatagsManager.insert_data(data)


    def rem_perma_tag(self, tag: str) -> bool:
        """ Remove tags from the database"""
        return PermatagsManager.delete_data_by_tag(tag)


    def get_perma_tags(self) -> Optional[tuple]:
        """ Get tags from the database"""
        data = PermatagsManager.get_all_data()
        return data


    def __call__(self, n_out: int, texts: list[str]) -> list[str]:
        """Find n: number classes that are closest to the text.

       :param n_out: Number of returning classes.
       :param texts: List of text strings.
       :return: The n classes closest to the text.
       """

        if not texts:
            return []

        for word in texts:
            for index, value in enumerate(self.values):
                score = 0
                for val in value:
                    if Levenshtein.distance(word.lower(), val.lower()) < 2:
                        score += 1
                self.scores[index] += score

        result = []
        for i, value in self.scores.items():
            if value > 0:
                result.append(self.keys[i])

        return result
