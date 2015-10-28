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
