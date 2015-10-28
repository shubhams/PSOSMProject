import json
from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
import functions.features as feat
from you.functions.scorecalculator import getUserFeatureScore,getMatchingCombinations
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

	### subreds distribution
	subredData=getSegments({})

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
	colours=["#15507a","#5eb1ba","#6ED1DB","#720733","#c9c6b5","#d10061","#e67162","#db601e","#C1E66E","#317564"]
	hilites=["#1F78B8","#6BCCD6","#A30B4A","#AB0C4D","#E8E5D3","#E8006C","#FC7D6D","#FA6E23","#43A38B","#317564"]

	i=0
	data_str="[\n"
	for key in subredWeights.keys():
		datum="{\n"
		datum+="value : "+str(subredWeights[key])+",\n"
		datum+="color : \'"+colours[i]+"\',\n"
		datum+="highlight : \'"+hilites[i]+"\',\n"
		datum+="label : \'"+key+"\',\n"
		datum+="},\n"
		count+=1
		data_str+datum

	data_str+="]"

	return data_str

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
				links+='<a href="'+href+'">#</a>'
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
