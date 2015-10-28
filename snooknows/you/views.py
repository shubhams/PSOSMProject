import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
# Create your views here.

def home(request):
	template = loader.get_template('you/home.html')
	context = RequestContext(request, {
		})

	return HttpResponse(template.render(context))

def analyse(request,username):
	username="/u/"+username
	reddit_user="https://www.reddit.com"+username
	template = loader.get_template('you/you.html')
	
	vul_score=0.45
	grad=getColour(vul_score)
	max_score=98
	abs_score=41

	subredData=getSegments({})

	(comboData,comboLabels)=getBars({})

	fields_items=getFields("")

	context = RequestContext(request, {
		'username':username,
		'reddituser': reddit_user,
		'vul_score': vul_score,
		'gradient_1': grad[0],
		'gradient_2': grad[1],
		'abs_score' : str(abs_score)+"/"+str(max_score),
		'subred_data':subredData,
		'combo_data':comboData,
		'combo_labels':comboLabels,
		'fields_items':fields_items,
		})

	return HttpResponse(template.render(context))

def getSegments(subredWeights):
	colours=["#15507a","#5eb1ba","#6ED1DB","#720733","#c9c6b5","#d10061","#e67162","#db601e","#C1E66E","#317564"]
	hilites=["#1F78B8","#6BCCD6","#A30B4A","#AB0C4D","#E8E5D3","#E8006C","#FC7D6D","#FA6E23","#43A38B","#317564"]

	i=0
	data_str="[\n"
	for key in subredWeights.keys():
		datum="{\n"
		datum+="value : "+str(subredWeights(key))+",\n"
		datum+="color : '"+colours[i]+"',\n"
		datum+="highlight : '"+hilites[i]+"',\n"
		datum+="label : '"+key+"',\n"
		datum+="},\n"
		count+=1
		data_str+datum

	data_str+="]"

	return data_str

def getBars(comboDict):
	labels_str="["
	data_str="["

	for key in comboDict.keys():
		labels_str+="'"+key+"',"
		data_str+=str(comboDict(key))+","

	labels_str+="]"
	data_str+="]"

	return data_str,labels_str


def getColour(score):
	gradient = {} 
	gradient["low"]=["#27ae60","#16a085"]
	gradient["mid"]=["#f1c40f","#f39c12"]
	gradient["high"]=["#e74c3c","#c0392b"]

	colour="high"
	
	if score<0.33:
		colour="low"
	elif score<0.66:
		colour="mid"
	else:
		colour="high"

	return gradient[colour]

def getFields(fields_json):
	fields_json='{"Sexual Orientation": {"https://www.reddit.com/r/IAmA/comments/3mkjn6/hi_im_cycling_around_the_world_so_far_27000_miles/cvfpyq6": "bike rides", "https://www.reddit.com/r/AskReddit/comments/3johsm/what_video_game_was_an_absolute_masterpiece/curj0z2": "Fantasy"}, "Hobbies/Interest/Fetishes": {"https://www.reddit.com/r/IAmA/comments/3mkjn6/hi_im_cycling_around_the_world_so_far_27000_miles/cvfpyq6": "bike rides"}, "What you like to Discuss": {"https://www.reddit.com/r/AskReddit/comments/3o7an2/what_is_the_worst_movie_you_went_to_see_in_the/cvuw5aj": "Works", "https://www.reddit.com/r/AskReddit/comments/3johsm/what_video_game_was_an_absolute_masterpiece/curj0z2": "Games on Microsoft platforms", "https://www.reddit.com/r/gameofthrones/comments/3k0trw/no_spoilers_a_friend_of_mine_just_finished_making/cuudwbw": "Best Film Empire Award winners", "https://www.reddit.com/r/photoshopbattles/comments/3kn4jv/psbattle_smiling_hedgehog_sits_with_palms/cuz0cl1": "Red pill and blue pill", "https://www.reddit.com/r/IAmA/comments/3mewn7/iama_exstripper_ama/cvfq694": "Wealth", "https://www.reddit.com/r/IAmA/comments/3mkjn6/hi_im_cycling_around_the_world_so_far_27000_miles/cvfpyq6": "Vehicles"}, "Your interests": {"https://www.reddit.com/r/IAmA/comments/3mkjn6/hi_im_cycling_around_the_world_so_far_27000_miles/cvfpyq6": "Health", "https://www.reddit.com/r/AskReddit/comments/3johsm/what_video_game_was_an_absolute_masterpiece/curj0z2": "Culture", "https://www.reddit.com/r/StarWars/comments/3pa39e/i_edited_all_of_the_trailers_and_teasers_together/cw4zfct": "Leisure", "https://www.reddit.com/r/gameofthrones/comments/3k0trw/no_spoilers_a_friend_of_mine_just_finished_making/cuudwbw": "Technology", "https://www.reddit.com/r/thewalkingdead/comments/3pbti7/spoiler_the_gun/cw4yyo4": "Belief", "https://www.reddit.com/r/IAmA/comments/3mewn7/iama_exstripper_ama/cvfq694": "Business", "https://www.reddit.com/r/ShadowBan/comments/3ngkvy/am_i_shadowbanned/cvojnt7": "Politics", "https://www.reddit.com/r/AskReddit/comments/3o7an2/what_is_the_worst_movie_you_went_to_see_in_the/cvuw5aj": "Science", "https://www.reddit.com/r/india/comments/3ngdjr/india_in_a_day_a_crowdsourced_movie_produced_by/cvnrzt2": "Arts"}, "Your Relationships": {}, "Where you live": {}, "Your Pets": {}, "Places of Interest": {"https://www.reddit.com/r/StarWars/comments/3jnnxg/looking_for_my_first_jedi_master_the_guy_who/cur6vsh": "Hahaha", "https://www.reddit.com/r/AskReddit/comments/3kvm4y/whats_your_experience_with_an_animal_entering/cv14t9f": "Delhi", "https://www.reddit.com/r/gentlemanboners/comments/3pbrw4/nicola_peltz/cw6135t": "TLA"}, "Your Family Members": {"https://www.reddit.com/r/unitedkingdom/comments/3jqkd7/looking_for_my_first_jedi_master_the_guy_who/cuxr24z": "mother"}}'
	fields_json=fields_json.encode('utf8')
	fields_dict=json.loads(fields_json)

	fields_items=[]
	for key in fields_dict:
		datum=fields_dict[key]
		values="<ul>\n"
		links="<ul>\n"
		for k in datum.keys():
			values+="<li>"+datum[k]+"</li>"
			links+='<li><a href="'+k+'">#</a></li>\n'
		values+="</ul>"
		links+="</ul>"

		fields_datum={}
		fields_datum["name"]=key
		fields_datum["values"]=values
		fields_datum["links"]=links

		fields_items.append(fields_datum)

	# print fields_items

	return fields_items

	return fields_items
