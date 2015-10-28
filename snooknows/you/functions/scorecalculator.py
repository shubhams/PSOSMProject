import pandas as pd
import math
import itertools
import json
from pprint import pprint
from collections import Counter

def getFeatureScores():
    dict = {'Your Sex': 'Sex', 'Your Sexual Orientation': 'Sexual Orientation',
            'Your Religious Beliefs': 'Religious Beliefs',
            'Who you\'re in a Relationship with': 'Your Relationships',
            'What you like to Discuss':	'What you like to Discuss',
            'People in your Family': 'Your Family Members',
            'Where you live': 'Where you Live',
            'Places of Interest to you': 'Places of Interest',
            'Pets you Own': 'Your Pets',
            'Your Hobbies/Interests/Fetishes': 'Hobbies/Interest/Fetishes'}

    filepath = 'you/functions/AnonymousDataSensitivity_Responses.tsv'
    df = pd.DataFrame.from_csv(filepath, sep='\t')

    i = 0
    feat_scores = {}
    while i < (len(df.columns) - 2):
        field = df.columns[i]
        # print field
        series = df[field]
        i = i + 1
        j = 0
        count = 0
        total = 0
        while j < len(series):
            if not math.isnan(series[j]):
                count += 1
                total += series[j]
            j += 1
        # print j
        # print field+": %.2f"%((total*1.0)/count)
        score = ((total * 1.0) / count)
        feat_scores[dict[field]] = round(score, 2)
    return feat_scores

def getCombos():
    filepath = 'you/functions/AnonymousDataSensitivity_Responses.tsv'
    df = pd.DataFrame.from_csv(filepath, sep='\t')
    separator = ', '
    series = df[df.columns[10]]
    features = getFeatures(series)
    features.sort()
    # print features
    combo_counter = Counter()

    array = []
    for item in series:
        if type(item) is str:
            item = processText(item, separator)
            array.append(item)

    dict = {}
    for i in range(1, len(features)-1, 1):
        combinations = itertools.combinations(features, i)
        for combination in combinations:
            # print combination
            # print type(combination)
            string = tupleToString(combination)
            for item in array:
                if string in item:
                    # print string + ' ' + item
                    dict[string] = dict.get(string, 0) + 1
    combo_counter.update(dict)
    # print combo_counter
    return combo_counter

def getTopNCombos(combo_counter, n):
    return combo_counter.most_common(n)

def getFeatures(series):
    features = []
    for item in series:
        if type(item) is str:
            array = item.split(', ')
            for string in array:
                if string not in features:
                    features.append(string)
    return features

def processText(text, separator):
    if type(text) is not str:
        return None
    array = text.split(separator)
    array.sort()
    # print array
    string = ''
    for i in range(0, len(array), 1):
        if i >= len(array)-1:
            string += array[i]
        else:
            string += array[i] + ','
    # print string
    return string

def tupleToString(tuple):
    string = ''
    # print tuple
    for i in range(0, len(tuple), 1):
        if i >= len(tuple)-1:
            string += tuple[i]
        else:
            string += tuple[i] + ','
    return string

def getMatchingCombinations(s):
    features=getFeaturesFromJSON(s)
    combo_counter = getCombos()
    features.sort()
    # print features
    dict = {}
    for i in range(1, len(features), 1):
        combinations = itertools.combinations(features, i)
        for combination in combinations:
            # print type(combination)
            string = tupleToString(combination)
            # print string
            count = combo_counter[string]
            if count > 0:
                val = float(count)/58
                val = round(val, 2)
                dict[string] = val
    return dict

def getFeaturesFromJSON(string):
    features = []
    data = json.loads(string)
    # pprint(data)
    for item in data:
        # print item
        fields = data[item]
        if len(fields) > 0:
            # print fields
            # print item
            features.append(item)
    return features

def getUserFeatureScore(string):
    score = {}
    features = getFeaturesFromJSON(string)
    feature_scores = getFeatureScores()
    # print feature_scores
    # print features
    max_score = 0
    for key in feature_scores.keys():
        max_score += float(feature_scores.get(key))
    # print max_score
    user_score = 0
    for feature in features:
        user_score += feature_scores.get(feature, 0)
        # if user_score > 0:
        # print str(s) + ' ' + feature
    # print user_score
    percent_score = round(user_score/max_score, 2)
    # print score
    score['user_score'] = user_score
    score['percent_score'] = percent_score
    return score

if __name__ == '__main__':
    print ""
    # filepath = 'AnonymousDataSensitivity_Responses.tsv'
    # df = pd.DataFrame.from_csv(filepath, sep='\t')
    # pprint(getUserFeatureScore(string))
    # pprint(getMatchingCombinations(getFeaturesFromJSON(string)))