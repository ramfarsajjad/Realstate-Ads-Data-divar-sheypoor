import json
import os

def check_unique(lst):
    return len(lst) == len(set(lst))

dir_main = os.path.dirname(os.path.abspath(__name__))
TokDir = os.path.join(dir_main, 'scraper')
# Example usage:
TokFile = os.path.join(TokDir,'syp_tokbase.json')
with open(TokFile, 'r') as file:
    tokcell = json.load(file)
print(check_unique(tokcell))  # Output: True (unique)


