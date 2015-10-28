from cv2 import getNumberOfCPUs
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

    filepath = 'AnonymousDataSensitivity_Responses.tsv'
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
    filepath = 'AnonymousDataSensitivity_Responses.tsv'
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

def getMatchingCombinations(features):
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
    # filepath = 'AnonymousDataSensitivity_Responses.tsv'
    # df = pd.DataFrame.from_csv(filepath, sep='\t')
    string = '{"Sexual Orientation": {}, "Hobbies/Interest/Fetishes": {"ethical": ["https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvphfs"], "smuggled": ["https://www.reddit.com/r/worldnews/comments/3ljp87/a_wikileaks_document_shows_us_had_plans_to/cv6vvz2"], "violence": ["https://www.reddit.com/r/worldnews/comments/1lbnol/saudi_arabias_cabinet_has_passed_a_ban_on/cbxnsgs"], "Signal Processing": ["https://www.reddit.com/r/science/comments/2hoawz/natures_elegant_and_efficient_vision_systems_can/ckuhnl2"], "humour": ["https://www.reddit.com/r/malaysia/comments/3nfseg/hi_malaysia_i_am_intrigued_as_to_why_you_used_the/cvnnukx"], "Nepal": ["https://www.reddit.com/r/pics/comments/3b2l6u/a_nepali_festival_to_thank_dogs_for_their/csieml8"], "mind": ["https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvpzmv", "https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvj6tj", "https://www.reddit.com/r/technology/comments/3blzxk/end_of_roaming_charges_net_neutrality_becomes_law/csng9nb", "https://www.reddit.com/r/pics/comments/3bfy7m/topless_lebanese_girls_burning_isis_flags_nsfw/cslxt8r"], "mummies": ["https://www.reddit.com/r/todayilearned/comments/3ohmid/til_that_on_an_island_in_indonesia_if_a_child/cvxjjhc"], "sex": ["https://www.reddit.com/r/science/comments/2vyb37/crows_understand_analogies_what_birds_can_teach/com4wp0"], "psychological": ["https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvhavc"], "Matthew": ["https://www.reddit.com/r/todayilearned/comments/3b0cft/til_that_when_a_bald_eagle_loses_a_feather_it/cshx8qn"], "Indian": ["https://www.reddit.com/r/worldnews/comments/368g7r/ecuador_breaks_guinness_reforestation_record/crbqk5q", "https://www.reddit.com/r/worldnews/comments/368g7r/ecuador_breaks_guinness_reforestation_record/crbqjad"], "ship": ["https://www.reddit.com/r/AskReddit/comments/3bcd9y/what_is_the_most_embarrasing_thing_you_could/csl0r2q"], "knowledge": ["https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvp8ny"], "expert": ["https://www.reddit.com/r/worldnews/comments/2oiqi9/a_boat_smuggling_215kg_of_cocaine_has_been_seized/cmnqgwy", "https://www.reddit.com/r/technology/comments/3q1njw/space_elevator_patented_by_canadian_company/cwbtoh7", "https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvm4cd"], "NSA": ["https://www.reddit.com/r/announcements/comments/3dautm/content_policy_update_ama_thursday_july_16th_1pm/ct3p53t"], "question": ["https://www.reddit.com/r/AskReddit/comments/3oft3n/reddit_what_little_things_annoy_you/cvwtiey", "https://www.reddit.com/r/news/comments/2xj24d/how_apple_lost_533_million_to_an_8thgrade_dropout/cp0lrty", "https://www.reddit.com/r/technology/comments/1kjt7j/white_house_tried_to_interfere_with_washington/cbpzu8x"], "religion": ["https://www.reddit.com/r/pics/comments/3b2l6u/a_nepali_festival_to_thank_dogs_for_their/csie6h1", "https://www.reddit.com/r/todayilearned/comments/37ixar/til_that_a_pastor_and_his_wife_kidnapped_a_4month/crnaspc"], "citations": ["https://www.reddit.com/r/Foodforthought/comments/2v79o4/the_powerful_cheat_for_themselves_the_powerless/cofrh5c"], "elephant": ["https://www.reddit.com/r/offbeat/comments/2ojp76/a_chimpanzee_is_not_entitled_to_the_same_rights/cmns2gk", "https://www.reddit.com/r/UpliftingNews/comments/2o5zmh/elephant_who_wept_through_his_rescue_officially/cmkmzkp"], "Thai": ["https://www.reddit.com/r/OldSchoolCool/comments/36zfy8/japanese_samurai_the_photo_was_taken_between_1863/crj1wx3"], "pride": ["https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvmd6z"], "Malaysian airlines": ["https://www.reddit.com/r/dataisbeautiful/comments/2vwwy5/two_malaysian_airlines_flights_were_responsible/colwfbn"], "Spain": ["https://www.reddit.com/r/worldnews/comments/2yb18y/german_parliament_approves_female_boardroom_quota/cp7w7qh"], "war crime": ["https://www.reddit.com/r/worldnews/comments/3ndnd9/un_says_us_militarys_afghan_hospital_bombing_may/cvng4bu"], "coffee": ["https://www.reddit.com/r/redditlogos/comments/1okfof/request_for_a_new_logoheader_for_rworldnews/ccxvc9j", "https://www.reddit.com/r/pics/comments/3fcyum/my_girlfriend_is_a_nanny_and_made_some_dessert/ctnk6yl", "https://www.reddit.com/r/redditlogos/comments/1okfof/request_for_a_new_logoheader_for_rworldnews/cd1uix3"], "pain": ["https://www.reddit.com/r/Fitness/comments/3omrbr/if_youre_trying_to_lose_body_fat_new_study_shows/cvz9pli"], "social website": ["https://www.reddit.com/r/bestof/comments/3db7hr/spez_states_that_he_and_kn0wthing_didnt_create/ct3pom0"], "the Maldives": ["https://www.reddit.com/r/AskReddit/comments/2tps26/all_of_your_karma_points_are_converted_to_cash/co1agdc"], "the Royal Green Jackets": ["https://www.reddit.com/r/worldnews/comments/2vyqag/braunschweig_carnival_parade_canceled_over/com31rf"], "Saudi": ["https://www.reddit.com/r/worldnews/comments/3n5b1m/saudi_arabia_insists_un_keeps_lgbt_rights_out_of/cvldwnc"], "news": ["https://www.reddit.com/r/worldnews/comments/2oiqi9/a_boat_smuggling_215kg_of_cocaine_has_been_seized/cmnlxr6", "https://www.reddit.com/r/worldnews/comments/1kln1n/scotland_yard_to_assess_fresh_claims_over_death/cbq79fq", "https://www.reddit.com/r/news/comments/3cudy6/ellen_pao_is_stepping_down_as_reddits_chief/csz3hy9", "https://www.reddit.com/r/malaysia/comments/3nbb4i/nasi_lemak_nowadays/cvmlev7", "https://www.reddit.com/r/worldnews/comments/1pezbg/nsa_spying_has_nothing_to_do_with_terrorism/cd1ych6", "https://www.reddit.com/r/pics/comments/3fb7w5/8_ton_orca_jumps_nearly_20_ft_out_of_the_water/ctnf1ul", "https://www.reddit.com/r/self/comments/3bymjd/dear_reddit_you_are_starting_to_suck/csra2l9"], "U.K.": ["https://www.reddit.com/r/pics/comments/3obojx/seen_at_the_airport_in_tel_aviv_israel/cvvtsmv"], "eBay": ["https://www.reddit.com/r/technology/comments/2xgezf/paypal_cuts_off_mega_because_it_actually_keeps/cp0dc6h"], "desert": ["https://www.reddit.com/r/science/comments/2h177b/the_sahara_is_millions_of_years_older_than/ckodbe8"], "Clint Eastwood": ["https://www.reddit.com/r/LifeProTips/comments/3kcp59/lpt_tell_older_people_your_dreams_they_just_might/cuwlog0"], "wildlife": ["https://www.reddit.com/r/pics/comments/3eyhld/cecil_the_lions_final_photograph/ctjtjgy"], "Chinese": ["https://www.reddit.com/r/worldnews/comments/2kcd2h/indigenous_communities_take_chevron_to_global/cljxytt", "https://www.reddit.com/r/worldnews/comments/3ljp87/a_wikileaks_document_shows_us_had_plans_to/cv6w1zn"], "language": ["https://www.reddit.com/r/worldnews/comments/3n5b1m/saudi_arabia_insists_un_keeps_lgbt_rights_out_of/cvl67xn"], "culture": ["https://www.reddit.com/r/bestof/comments/3db7hr/spez_states_that_he_and_kn0wthing_didnt_create/ct3q8gz", "https://www.reddit.com/r/science/comments/2n5xvh/is_cheating_a_part_of_banking_culture_some_people/cmalti6", "https://www.reddit.com/r/malaysia/comments/3nfseg/hi_malaysia_i_am_intrigued_as_to_why_you_used_the/cvnn77d"], "reddit": ["https://www.reddit.com/r/RedditTrophies/comments/2sma75/15_january_2014/cnqt58p", "https://www.reddit.com/r/pics/comments/3d5dfw/this_picture_is_going_viral_in_my_town/ct2dsv4", "https://www.reddit.com/r/bestof/comments/3db7hr/spez_states_that_he_and_kn0wthing_didnt_create/ct3ynbv", "https://www.reddit.com/r/RedditTrophies/comments/2sma75/15_january_2014/cnqzaca", "https://www.reddit.com/r/videos/comments/3pzk7f/dinosaur_video_kid_shocked_and_grateful_that_his/cwb0k3v", "https://www.reddit.com/r/AskReddit/comments/34xxzs/who_in_your_opinion_has_contributed_the_most_to/cqz7w6m"], "policemen": ["https://www.reddit.com/r/news/comments/3ne819/nypd_cop_thrown_in_psych_ward_for_exposing_arrest/cvngh18"], "federal statute": ["https://www.reddit.com/r/todayilearned/comments/3b0cft/til_that_when_a_bald_eagle_loses_a_feather_it/cshxwoy"], "cigarettes": ["https://www.reddit.com/r/politics/comments/2zt1p9/new_york_city_council_issues_formal_call_for/cpmsgeb"], "torturing": ["https://www.reddit.com/r/Fitness/comments/3orhv8/study_shows_that_beet_juice_contains_a_molecule/cw0fz98"], "RyanAir": ["https://www.reddit.com/r/CrazyIdeas/comments/1pb4a4/instead_of_seats_airplanes_should_have_bunk_beds/cd0nn52"], "fund managers": ["https://www.reddit.com/r/worldnews/comments/371bps/li_hejun_the_chinese_billionaire_who_supposedly/crj2900"]}, "What you like to Discuss": {"Bureau of Indian Affairs": ["https://www.reddit.com/r/todayilearned/comments/3b0cft/til_that_when_a_bald_eagle_loses_a_feather_it/cshxwoy"], "Williamsburg, Brooklyn": ["https://www.reddit.com/r/news/comments/3ne819/nypd_cop_thrown_in_psych_ward_for_exposing_arrest/cvngh18"], "Malaysia": ["https://www.reddit.com/r/dataisbeautiful/comments/2vwwy5/two_malaysian_airlines_flights_were_responsible/colwfbn", "https://www.reddit.com/r/malaysia/comments/3nbb4i/nasi_lemak_nowadays/cvmlev7", "https://www.reddit.com/r/malaysia/comments/3nbb4i/nasi_lemak_nowadays/cvmmfew", "https://www.reddit.com/r/malaysia/comments/3nfseg/hi_malaysia_i_am_intrigued_as_to_why_you_used_the/cvnnlm1", "https://www.reddit.com/r/worldnews/comments/2yb18y/german_parliament_approves_female_boardroom_quota/cp7w7qh"], "China": ["https://www.reddit.com/r/worldnews/comments/2kcd2h/indigenous_communities_take_chevron_to_global/cljxytt", "https://www.reddit.com/r/worldnews/comments/3ljp87/a_wikileaks_document_shows_us_had_plans_to/cv6vvz2", "https://www.reddit.com/r/worldnews/comments/371bps/li_hejun_the_chinese_billionaire_who_supposedly/crj2900"], "News": ["https://www.reddit.com/r/pics/comments/3eyhld/cecil_the_lions_final_photograph/ctjtjgy", "https://www.reddit.com/r/technology/comments/2xgezf/paypal_cuts_off_mega_because_it_actually_keeps/cp0dc6h"], "Yemen": ["https://www.reddit.com/r/worldnews/comments/3ndnd9/un_says_us_militarys_afghan_hospital_bombing_may/cvng4bu"]}, "Your interests": {"Science": "", "Violence": "", "Environment": "", "Culture": "", "Politics": "", "Law": ""}, "Your Relationships": {}, "Where you Live": {}, "Your Pets": {"mane": ["https://www.reddit.com/r/pics/comments/3eyhld/cecil_the_lions_final_photograph/ctjtjgy"], "birds": ["https://www.reddit.com/r/todayilearned/comments/3b0cft/til_that_when_a_bald_eagle_loses_a_feather_it/cshxwoy"]}, "Places of Interest": {"U.K.": ["https://www.reddit.com/r/pics/comments/3obojx/seen_at_the_airport_in_tel_aviv_israel/cvvtsmv"], "Chinese": ["https://www.reddit.com/r/worldnews/comments/2kcd2h/indigenous_communities_take_chevron_to_global/cljxytt", "https://www.reddit.com/r/worldnews/comments/3ljp87/a_wikileaks_document_shows_us_had_plans_to/cv6vvz2", "https://www.reddit.com/r/worldnews/comments/3ljp87/a_wikileaks_document_shows_us_had_plans_to/cv6w1zn"], "Congress": ["https://www.reddit.com/r/todayilearned/comments/3b0cft/til_that_when_a_bald_eagle_loses_a_feather_it/cshxwoy"], "the Maldives": ["https://www.reddit.com/r/AskReddit/comments/2tps26/all_of_your_karma_points_are_converted_to_cash/co1agdc"], "Nepal": ["https://www.reddit.com/r/pics/comments/3b2l6u/a_nepali_festival_to_thank_dogs_for_their/csieml8"], "Harrods": ["https://www.reddit.com/r/worldnews/comments/1kln1n/scotland_yard_to_assess_fresh_claims_over_death/cbq79fq"], "Brooklyn": ["https://www.reddit.com/r/news/comments/3ne819/nypd_cop_thrown_in_psych_ward_for_exposing_arrest/cvngh18"], "Saudi": ["https://www.reddit.com/r/worldnews/comments/1lbnol/saudi_arabias_cabinet_has_passed_a_ban_on/cbxnsgs", "https://www.reddit.com/r/worldnews/comments/3n5b1m/saudi_arabia_insists_un_keeps_lgbt_rights_out_of/cvl67xn", "https://www.reddit.com/r/worldnews/comments/3n5b1m/saudi_arabia_insists_un_keeps_lgbt_rights_out_of/cvldwnc"], "Somali": ["https://www.reddit.com/r/worldnews/comments/2oiqi9/a_boat_smuggling_215kg_of_cocaine_has_been_seized/cmnlxr6"], "Arabia": ["https://www.reddit.com/r/worldnews/comments/3ndnd9/un_says_us_militarys_afghan_hospital_bombing_may/cvng4bu"], "Thai": ["https://www.reddit.com/r/OldSchoolCool/comments/36zfy8/japanese_samurai_the_photo_was_taken_between_1863/crj1wx3"], "Spain": ["https://www.reddit.com/r/worldnews/comments/2yb18y/german_parliament_approves_female_boardroom_quota/cp7w7qh"]}, "Your Family Members": {"dad": ["https://www.reddit.com/r/bestof/comments/3db7hr/spez_states_that_he_and_kn0wthing_didnt_create/ct3pom0"], "mum": ["https://www.reddit.com/r/todayilearned/comments/3b0cft/til_that_when_a_bald_eagle_loses_a_feather_it/cshxwoy", "https://www.reddit.com/r/todayilearned/comments/3ohmid/til_that_on_an_island_in_indonesia_if_a_child/cvxjjhc"], "parents": ["https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvmd6z"], "son": ["https://www.reddit.com/r/Foodforthought/comments/2v79o4/the_powerful_cheat_for_themselves_the_powerless/cofrh5c", "https://www.reddit.com/r/Bad_Cop_No_Donut/comments/3ba0ql/cop_pulls_man_over_refuses_to_let_him_show/cskei95", "https://www.reddit.com/r/news/comments/2xj24d/how_apple_lost_533_million_to_an_8thgrade_dropout/cp0lrty", "https://www.reddit.com/r/explainlikeimfive/comments/3o9r4o/eli5_what_happens_in_the_brain_when_you_lose_your/cvvhavc", "https://www.reddit.com/r/technology/comments/1kjt7j/white_house_tried_to_interfere_with_washington/cbpzlg5", "https://www.reddit.com/r/worldnews/comments/1kln1n/scotland_yard_to_assess_fresh_claims_over_death/cbq79fq", "https://www.reddit.com/r/news/comments/2tyax4/fcc_calls_blocking_of_personal_wifi_hotspots/co49dqb", "https://www.reddit.com/r/Fitness/comments/3orhv8/study_shows_that_beet_juice_contains_a_molecule/cw0fz98", "https://www.reddit.com/r/worldnews/comments/1no5le/europes_youth_unemployment_crisis_in_one_grim_map/cckpl0v"]}}'
    # pprint(getUserFeatureScore(string))
    # pprint(getMatchingCombinations(getFeaturesFromJSON(string)))