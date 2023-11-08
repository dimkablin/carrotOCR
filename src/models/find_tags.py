""" Find Tags model """
import Levenshtein
import json

# class FindTags:
#     """ Zero Shot Classification init class"""
#     def __init__(self):
#         self.path_to_classes = "models/zero-shot-classification/classes.txt"
#         self.classes = []
#         self.read_classes(self.path_to_classes)


#     def read_classes(self, path) -> None:
#         """ Read text classes from file
#         :param path: Path to the file with classes that seperated with new line
#         :return: None
#         """
#         with open(path, 'r', encoding='utf-8') as file:
#             classes = file.readlines()

#         self.classes = [cls.rstrip('\n') for cls in classes]


#     def __call__(self, n_out: int, texts: list[str]) -> list[str]:
#         """Find n: number classes that are closest to the text.

#        :param n_out: Number of returning classes.
#        :param texts: List of text strings.
#        :return: The n classes closest to the text.
#        """

#         if not self.classes or not texts:
#             return []

#         class_distances = {}

#         for cls in self.classes:
#             for text in texts:
#                 distance = Levenshtein.distance(cls, text)
#                 if cls not in class_distances or distance < class_distances[cls]:
#                     class_distances[cls] = distance

#         sorted_classes = sorted(self.classes, key=lambda cls: class_distances[cls])
#         return sorted_classes[:min(n_out, len(self.classes))]



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
        with open(path, "r", encoding='utf-8') as f:
            data = json.load(f)
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
        for id, value in self.scores.items():
            if value > 0:
                result.append(self.keys[id])

        return result