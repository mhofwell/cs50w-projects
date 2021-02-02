from django.shortcuts import render
from . import util
from django.http import HttpResponse
from markdown2 import Markdown
from django import forms

md = Markdown()


class NewPageForm(forms.Form):
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 50, 'rows': '200'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def getpage(request, title):
    try:
        page = util.get_entry(title)
        htmlpage = md.convert(page)
        return HttpResponse(htmlpage)
    except:
        return HttpResponse('<h1>Page was not found</h1>')


def new(request):
    if request.method == "POST":
        # Process the result of the incoming POST request
        page = NewPageForm(request.POST)
        if page.is_valid():
            title = page.cleaned_data["title"]
            content = page.cleaned_data["content"]
            util.save_entry(title, content)
    return render(request, "encyclopedia/new.html", {
        "page": NewPageForm()
    })


def search(request):
    print(request.GET['q'])
    q = request.GET['q']
    if util.get_entry(q):
        page = getpage(request, q)
        return HttpResponse(page)
    else:
        pagelist = util.list_entries()
        f_list = []
        msg = "Sorry nothing matches your query!"
        for page in pagelist:
            page_l = page.lower()
            q_l = q.lower()
            if page_l.find(q_l) != -1:
                f_list.append(page)
        return render(request, "encyclopedia/search.html", {
            "f_list": f_list,
            "msg": msg
        })
