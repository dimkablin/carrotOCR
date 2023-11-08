import json
import Levenshtein

def get_tags(words: list[str]) -> list[str]:
    """Get tags from words"""

    with open("./models/zero-shot-classification/classes.json", "r", encoding='utf-8') as f:
        data = json.load(f)
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
        for id, value in scores.items():
            if value > 0:
                result.append(keys[id])

        return result