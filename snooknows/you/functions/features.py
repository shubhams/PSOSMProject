import textrazor
from array import array
import re
from nltk.corpus import stopwords
import codecs
from pprint import pprint
import json
import getcomments as gt

##client.set_cleanup_mode("cleanHTML")
##response=client.analyze_url("http://www.bbc.co.uk/news/uk-politics-18640916")
# from Simmoo_Script import userReligionDict

userPlacesDict = {}
userReligionDict = {}
userSexDict = {}
userHobbiesDict = {}
userAnimalsDict = {}
userResidenceDict = {}
userFamilyDict = {}
userTopicsDict = {}
userInterestsDict = {}
userRelationsDict = {}
placeResidenceList=[]

def getDataFromFile(userName):
    f = codecs.open(userName+'.txt','r','utf-8')
    text = f.read()
    return json.loads(text)

def getPermalink(obj):
    return obj.permalink

def getEntityCommentDictionary(entity, dict_of_comments):
    dict = {}
    # print "The entity to be matched is : " + entity
    for key in dict_of_comments.keys():
        if entity in dict_of_comments[key]:
            # print entity + " found in  " + dict_of_comments[key]
            dict[getPermalink(key)] = entity
    return dict

def textAnalysis(text, dictOfComments):
    global userPlacesDict
    global userReligionDict
    global userSexDict
    global userHobbiesDict
    global userAnimalsDict
    global userResidenceDict
    global userFamilyDict
    global userTopicsDict
    global userInterestsDict
    global userRelationsDict
    global ctr

    # textrazor.api_key = "3f25b580908bee88bf94d9b3b6e8a55040508f5b9a3e8e97dc0e8176"
    textrazor.api_key = "0f99a100cf14a59f52e0ef1b626b9d3d751f27c80e033b35cd1d5ce9"
    client=textrazor.TextRazor(extractors=["entities", "topics","entailments","relations","phrases","words"])

    response = client.analyze(text)
    entities = list(response.entities())

    entities.sort(key=lambda x: x.relevance_score, reverse=True)
    freebase_cityList=["/location/country","/location/dated_location","/location/location","/location/in_city","/location/administrative_division","/sports/sports_team_location","/location/capital_of_administrative_division","/organization/organization_scope","/periodicals/newspaper_circulation_area","/travel/travel_destination","/location/in_district","/location/citytown"]
    freebase_religionList=["/religion/religion","/people/ethnicity"]
    freebase_sexList=["/celebrities/sexual_orientation"]
    freebase_interestList=["/organization/organization","/interests/hobby","/interests/interest","/book/book_subject","/film/film_subject","/internet/website"]
    freebase_animalList=["/biology/animal","/biology/animal_breed"]

    seen=set()
    for entity in entities:
        if entity.id not in seen:
            seen.add(entity.id)
            for entity_type in entity.freebase_types:
                entity_text = entity.matched_text
                print entity_text
                if((entity_type in freebase_cityList)):
                    if(entity.relevance_score>=0.2):
                        userPlacesDict.update(getEntityCommentDictionary(entity_text, dictOfComments))
                if((entity_type in freebase_religionList)):
                    if(entity.relevance_score>=0.2):
                        userReligionDict.update(getEntityCommentDictionary(entity_text, dictOfComments))
                if((entity_type in freebase_sexList) and (entity_text not in userSexDict.values())):
                        if(entity.relevance_score>=0.2):
                            userSexDict.update(getEntityCommentDictionary(entity_text, dictOfComments))
                if((entity_type in freebase_interestList) and (entity_text not in userHobbiesDict.values())):
                    if(entity.relevance_score>=0.3):
                        userHobbiesDict.update(getEntityCommentDictionary(entity_text, dictOfComments))
                if((entity_type in freebase_animalList) and (entity_text not in userAnimalsDict.values())):
                    if(entity.relevance_score>=0.2):
                        userAnimalsDict.update(getEntityCommentDictionary(entity_text, dictOfComments))

    userPlacesDict = func(userPlacesDict)
    userReligionDict = func(userReligionDict)
    userSexDict = func(userSexDict)
    userHobbiesDict = func(userHobbiesDict)
    userAnimalsDict = func(userAnimalsDict)

    # print "User places dict"
    # pprint(userPlacesDict)
    # print "User religion dict"
    # pprint(userReligionDict)
    # print "User sex dict"
    # pprint(userSexDict)
    # print "User hobby dict"
    # pprint(userHobbiesDict)
    # print "User animal dict"
    # pprint(userAnimalsDict)

    residence_list=["live","lived","living","residing","resided"]
    source_words=text.split(" ")
    filtered_words = [w for w in source_words if w not in stopwords.words('english')]
    for words in filtered_words:
            if words in residence_list:
                 index=filtered_words.index(words)+1
                 place_of_residence = filtered_words[index]
                 #print place_of_residence
                 #placeResidenceList.append(place_of_residence)
                 response2 = client.analyze(place_of_residence)
                 location_entities = list(response2.entities())
                 seen=set()
                 for entity in location_entities:
                     if entity.id not in seen:
                         seen.add(entity.id)
                         for entity_type in entity.freebase_types:
                             entity_text = entity.matched_text
                             if((entity_type in freebase_cityList)):
                                 if(entity.relevance_score>=0.2):
                                     userResidenceDict.update(getEntityCommentDictionary(place_of_residence, dictOfComments))

    # print "User Residence"
    # pprint(userResidenceDict)
    userRelationsDict = func(userRelationsDict)

    family_list=["wife","husband","son","daughter","girlfriend","boyfriend","mom","dad","parents","mother","father","brother","sister","mum","pop","grandad","gram","granny","grandma","grandpa"]
    for phrase in response.noun_phrases():
        for word in phrase.words:
            if((word.token in family_list) and (word.token not in userResidenceDict)):
                userFamilyDict.update(getEntityCommentDictionary(word.token, dictOfComments))

    # print "User Family"
    # pprint(userFamilyDict)
    userFamilyDict = func(userFamilyDict)

    relationship_list=["gf","bf","girlfriend","boyfriend"]
    for phrase in response.noun_phrases():
        for word in phrase.words:
            if word.token in relationship_list:
                userRelationsDict.update(getEntityCommentDictionary(word.token, dictOfComments))

    # print "User Relations"
    # pprint(userRelationsDict)
    userRelationsDict = func(userRelationsDict)

    topics=list(response.topics())
    topics.sort(key=lambda x: x.score, reverse=True)

    for topic in topics:
        if topic.score >= 0.7:
            # print topic.label
            userTopicsDict.update(getEntityCommentDictionary(topic.label, dictOfComments))

    # print "User Topics"
    # pprint(userTopicsDict)
    userTopicsDict = func(userTopicsDict)

    talkedAbout=list(response.coarse_topics())
    talkedAbout.sort(key=lambda x: x.score, reverse=True)
    for talkedAboutTopic in talkedAbout:
        if talkedAboutTopic.score>=0.005:
            print(talkedAboutTopic.label)
            userInterestsDict[talkedAboutTopic.label] = ""

    # print "User interest"
    # pprint(userInterestsDict)
    # userInterestsDict = func(userInterestsDict)

def func(dict):
    key_set = set()
    for value in dict.values():
        key_set.add(value)

    updated_dict = {}
    for key in key_set:
        updated_dict[key] = []

    for key in updated_dict.keys():
        for id in dict.keys():
            if key == dict[id]:
                # print key
                array = updated_dict[key]
                list = []
                for item in array:
                    list.append(item)
                list.append(id)
                updated_dict[key] = list
    # pprint(updated_dict)
    return updated_dict

def process(username):
    dict_of_comments = gt.extractComments(username)
    text = ''
    for value in dict_of_comments.values():
        text += value + '\n'
    # print text
    textAnalysis(text, dict_of_comments)

    userAnalysisDict = {}

    userAnalysisDict["Places of Interest"] = userPlacesDict
    userAnalysisDict["Sexual Orientation"] = userSexDict
    userAnalysisDict["Hobbies/Interest/Fetishes"] = userHobbiesDict
    userAnalysisDict["Your Pets"] = userAnimalsDict
    userAnalysisDict["Where you Live"] = userResidenceDict
    userAnalysisDict["Your Family Members"] = userFamilyDict
    userAnalysisDict["Your Relationships"] = userRelationsDict
    userAnalysisDict["What you like to Discuss"] = userTopicsDict
    userAnalysisDict["Your interests"] = userInterestsDict
    filename = username + '_analysis.json'
    # f = open(filename, 'w')
    # json.dump(userAnalysisDict, f)
    # f.close()
    return json.dumps(userAnalysisDict)
    

if __name__ == '__main__':
    print process('maxwellhill')

    # dict = {"https://www.reddit.com/r/Foodforthought/comments/2v79o4/the_powerful_cheat_for_themselves_the_powerless/cofrh5c": "son", "https://www.reddit.com/r/Bad_Cop_No_Donut/comments/3ba0ql/cop_pulls_man_over_refuses_to_let_him_show/cskei95": "son", "https://www.reddit.com/r/news/comments/2xj24d/how_apple_lost_533_million_to_an_8thgrade_dropout/cp0lrty": "son", "https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvhavc": "son", "https://www.reddit.com/r/technology/comments/1kjt7j/white_house_tried_to_interfere_with_washington/cbpzlg5": "son", "https://www.reddit.com/r/worldnews/comments/1kln1n/scotland_yard_to_assess_fresh_claims_over_death/cbq79fq": "son", "https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvmd6z": "parents", "https://www.reddit.com/r/bestof/comments/3db7hr/spez_states_that_he_and_kn0wthing_didnt_create/ct3pom0": "dad", "https://www.reddit.com/r/todayilearned/comments/3b0cft/til_that_when_a_bald_eagle_loses_a_feather_it/cshxwoy": "son", "https://www.reddit.com/r/news/comments/2tyax4/fcc_calls_blocking_of_personal_wifi_hotspots/co49dqb": "son", "https://www.reddit.com/r/Fitness/comments/3orhv8/study_shows_that_beet_juice_contains_a_molecule/cw0fz98": "son", "https://www.reddit.com/r/todayilearned/comments/3ohmid/til_that_on_an_island_in_indonesia_if_a_child/cvxjjhc": "mum", "https://www.reddit.com/r/worldnews/comments/1no5le/europes_youth_unemployment_crisis_in_one_grim_map/cckpl0v": "son"}

    # pprint(dict)
    # func(dict)
    # print "Your religious and ethnic interests "
    # pprint(userReligionDict)

    # print "Your sex and/or sexual interests "
    # pprint(userSexDict)

    # print "Your hobbies/interests "
    # pprint(userHobbiesDict)

    # print "Animals you've talked about "
    # pprint(userAnimalsDict)

    # print "You live(d) in :"
    # pprint(userResidenceDict)

    # print "People in your family "
    # pprint (userFamilyDict)

    # print "You are in a relationship with:"
    # pprint(userRelationsDict)

    # print "You have talked about:"
    # pprint(userTopicsDict)

    # print "Your interests:"
    # pprint(userInterestsDict)

    # pprint (getStringFromFile('screenseer'))
    # source_str="i used to live in mumbai. i am a gay man with passion for men.My dog is a labradoodle.my hobby is gardening. i also enjoy boating. books are interesting to read. I am a hindu who is friends with some christians.i am a 14 year old girl who lives in new delhi.Honestly, I'd really like to see how it'd go for a race or two where literally the only opportunity to pass is on the track. The designed to wear quickly tyres at the moment kinda irk me. As much as they can create a significant pace difference between cars on older/newer tyres they also provide a huge disincentive to following a car on similar age tyres close enough to attempt a pass. Many times it makes more sense for drivers to hang back in cleaner air and attempt the undercut to pass them in the pits."
    # textAnalysis(getStringFromFile('screenseer'))
    # f = codecs.open('screenseer.txt','r','utf-8')
    # for line in f.read().split('\n'):
    #     textAnalysis(line)