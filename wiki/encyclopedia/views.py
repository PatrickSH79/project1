from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
import re 
from urllib.parse import urlparse, parse_qs

from . import util
from . import markdown2

class SearchForm(forms.Form):
    q = forms.CharField(label="Search")

class NewArticleForm(forms.Form):
    title = forms.CharField(label='Title', required=True, strip=True)
    article = forms.CharField(widget=forms.Textarea(attrs={'name':'article', 'style':'height: 10em','cols':100}))
    action = forms.CharField(widget=forms.HiddenInput, initial='add')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show_random_article(request):
    random_article = util.get_random_entry()
    return HttpResponseRedirect(f"/wiki/{random_article}")
    
def edit_article(request, topic):
    to_edit_data = { 'title': topic, 'article': util.get_entry(topic), 'action': 'edit' }
    editform = NewArticleForm(initial=to_edit_data)
    
    return render(request, "encyclopedia/add.html", {
        "action": "edit",
        "form": editform,
        "error": None
    }) 

def load_article(request, topic):
    content = util.get_entry(topic)
    if content:
        title = re.search(r'^#(.*)$', content, re.MULTILINE)
        if title:
            title = title.group(1).strip()
        article = markdown2.markdown(content)

        return render(request, "encyclopedia/article.html", {
            "title": title,
            "article": article
        }) 

    else:        
        return render(request, "encyclopedia/404.html", {
            "topic": topic
        })

def find_article(request):
    search = SearchForm(request.POST)
    if search.is_valid():
        q = search.cleaned_data["q"]
        if q == "": 
             return HttpResponseRedirect("/wiki/")

        if util.get_entry(q):
            return HttpResponseRedirect(f"/wiki/{q}")

        else: 
            return render(request, "encyclopedia/search.html", {
                "q": q,
                "entries": util.list_search_entries(q)
            })
        
    return HttpResponseRedirect("/wiki/") 

def add(request):
    if request.method == "POST":
        newArticle = NewArticleForm(request.POST)
        if newArticle.is_valid():
            title = newArticle.cleaned_data["title"]
            action = newArticle.cleaned_data["action"]
            if util.get_entry(title) and action == 'add':
                return render(request, "encyclopedia/add.html", {
                    "form": newArticle,
                    "error": "Article already exists.",
                    "action": newArticle.cleaned_data["action"]
                })
            else:
                util.save_entry(title, newArticle.cleaned_data["article"])
                return HttpResponseRedirect(f"/wiki/{title}") 

        else:   
            return render(request, "encyclopedia/add.html", {
                "form": newArticle,
                "error": None,
                "action": "add"
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewArticleForm(),
        "error": None,
        "action": "add"
    })


