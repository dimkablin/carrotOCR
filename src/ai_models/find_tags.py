#pylint: disable=E
""" Find Tags model """
import json
import Levenshtein


class FindTags:
    """ Zero Shot Classification init class"""
    def __init__(self):
        self.path_to_classes = "src/ai_models/weights/zero-shot-classification/backup_classes.json"
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


FIND_TAGS_MODEL = FindTags()
