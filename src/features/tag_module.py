"""SOME DOCUMENTATION for tag_module.py"""

import json
import Levenshtein

def get_tags(words: list[str]) -> list[str]:
    """Get tags from words"""

    with open("./models/zero-shot-classification/classes.json", "r", encoding='utf-8') as file:
        data = json.load(file)
        values = list(data.values())
        keys = list(data.keys())

        scores = {k:0 for k in range(len(values))}

        for word in words:
            for index, value in enumerate(values):
                score = 0
                for val in value:
                    if Levenshtein.distance(word.lower(), val.lower()) < 3:
                        score += 1
                scores[index] += score

        result = []
        for i, value in scores.items():
            if value > 0:
                result.append(keys[i])

        return result
