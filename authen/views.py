from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
import requests 
from .forms import SignUpForm
from django.http import HttpResponse


def home(request):
    # return render(request, 'auth/home.html')
    # def home(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None or search=="top":
        # get the top news
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}&pageSize={}".format(
            "us",1,'7324ef53767141c38cd2efd1086c3b02',8
        )
        # url = "https://newsapi.org/v2/sources?apiKey=7324ef53767141c38cd2efd1086c3b02"
    else:
        # get the search query request
        # url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
        #     search,"popularity",page,'7324ef53767141c38cd2efd1086c3b02'
        # )
        url = "https://newsapi.org/v2/sources?q={}&sortBy={}&page={}&apiKey={}&pageSize={}".format(
            search,"business",page,'7324ef53767141c38cd2efd1086c3b02',8
        )
        # url = "https://newsapi.org/v2/sources?apiKey=7324ef53767141c38cd2efd1086c3b02"

    top_headlines = "https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=7324ef53767141c38cd2efd1086c3b02"
    braking_news = "https://newsapi.org/v2/sources?country=us&apiKey=7324ef53767141c38cd2efd1086c3b02"
    r = requests.get(url=url)
    r1 = requests.get(url=top_headlines)
    r2 = requests.get(url=braking_news)
    
    data = r.json()
    data1 = r1.json()
    data2 = r2.json()
    # raise Exception("I want to know the value of this: ", data)

    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    # seprating the necessary data
    temp_img = ''
    # raise Exception("I want to know the value of this: ", context)
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"],
        })
    context1 = {
        "success": True,
        "data": [],
        "search": search
    }
    # raise Exception("I want to know the value of this: ", data1['articles'])
    for j in data1['articles']:
        context1["data"].append({
            "title": j["title"],
            "description":  "" if j["description"] is None else j["description"],
            "url": j["url"],
            "image": temp_img if j["urlToImage"] is None else j["urlToImage"],
            "publishedat": j["publishedAt"],
            "author": j["author"],
        })
        
    # raise Exception("I want to know the value of this: ", data2['sources'])

    context2 = {
        "success": True,
        "data": [],
        "search": search
    }
    # raise Exception("I want to know the value of this: ", data1['articles'])
    for j in data2['sources']:
        context2["data"].append({
            "title": j["name"],
            "description":  "" if j["description"] is None else j["description"],
            "url": j["url"],
        })
    # send the news feed to template in context
    # return render(request, 'index.html', context=context)
    return render(request, 'auth/home.html', {'context':context, 'context1':context1, 'context2': context2})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # raise Exception("I want to know the value of this: ", form)
        if form.is_valid():
            user = form.save()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'auth/signup.html', { 'form' : form })

def searchNews(request):
    q = dict(request.GET)
    query = q.get('query')
    
    url = ('https://newsapi.org/v2/everything?'
       'q='+query[0]+'&'
       'from=2021-05-07&'
       'sortBy=popularity&'
       'apiKey=7324ef53767141c38cd2efd1086c3b02')

    r = requests.get(url=url)
    data = r.json()

    data = data["articles"]
    search = ''
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    # seprating the necessary data
    temp_img = ''
    # raise Exception("I want to know the value of this: ", context)
    for i in data:
        context["data"].append({
            "title": i["title"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": temp_img if i["urlToImage"] is None else i["urlToImage"],
            "publishedat": i["publishedAt"],
        })

    # raise Exception("I want to know the value of this: ", context)
    return render(request, 'auth/search_results.html', {'context':context, 'query':query[0]})
    

