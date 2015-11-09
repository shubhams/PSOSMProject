import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import functions.features as feat
from you.functions.scorecalculator import getUserFeatureScore,getMatchingCombinations, getPercentage
# Create your views here.

def home(request):
	template = loader.get_template('you/home.html')
	context = RequestContext(request, {
		})

	return HttpResponse(template.render(context))

def analyse(request,username):
	usr=username
	username="/u/"+username
	reddit_user="https://www.reddit.com"+username
	template = loader.get_template('you/you.html')

	### fields json
	print "Analysing data of: "+usr
	userAnJSON=feat.process(usr)
	fields_items=getFields(userAnJSON)
	
	### score
	ret_score = getUserFeatureScore(userAnJSON)
	vul_score= ret_score["percent_score"]
	grad=getColour(vul_score)
	max_score=47.05
	abs_score=ret_score["user_score"]

	### combos
	combo_dict=getMatchingCombinations(userAnJSON)

	### subreds distribution
	subredPercs= getPercentage(userAnJSON)
	subredData=getSegments(subredPercs)

	new_combo_dict={}
	for key in combo_dict.keys():
		if combo_dict[key]>=0.1:
			new_combo_dict[key]=combo_dict[key]

	(comboData,comboLabels)=getBars(new_combo_dict)



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
	colours=["#BF0000","#E03800","#E38400","#E6AC00","#DED600","#B1DE00","#7BD900","#32BA00","#1D9127","#00965A"]
	hilites=["#E03838","#E36E46","#E6A853","#E0C060","#DEDA62","#BFDB4F","#A1D959","#6AAD51","#51B859","#56967D"]

	i=0
	data_list=[]

	subredW=sorted(subredWeights.items(), key=lambda x: (-x[1], x[0]))

	for sub in subredW:
		datum={}
		datum["value"]=str(int(sub[1]))
		if i>9:
			datum["color"] = colours[(i%10)+1]
			datum["highlight"] = hilites[(i%10)+1]
		else:
			datum["color"]=colours[i]
			datum["highlight"]=hilites[i]
		datum["label"]="r/"+sub[0].encode('utf8')
		i+=1
		data_list.append(datum)

	return data_list

def getBars(comboDict):
	labels_str="["
	data_str="["

	labels_list=[]
	data_list=[]

	for key in comboDict.keys():
		labels_str+="\x22"+key+"\x22 ,"
		data_str+=str(comboDict[key])+","

	for key in comboDict.keys():
		labels_list.append(key)
		data_list.append(comboDict[key])

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
	fields_json=fields_json.encode('utf8')
	fields_dict=json.loads(fields_json)

	fields_items=[]
	for key in fields_dict:
		datum=fields_dict[key]
		values="<ul>\n"
		links="<ul>\n"
		for k in datum.keys():
			values+="<li>"+k+"</li>"
			links+='<li>'
			for href in datum[k]:
				if href=="":
					continue
				links+='<a href="'+href+'" target="_blank"><i class="fa fa-external-link-square"></i> </a>'
			links+='</li>\n'
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
