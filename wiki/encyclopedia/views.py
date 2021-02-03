from django.shortcuts import render
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from markdown2 import Markdown
from django import forms
from django.urls import reverse

md = Markdown()


class NewPageForm(forms.Form):
    title = forms.CharField(label="title", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your title.'}))
    content = forms.CharField(label="content", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter your content.', 'cols': 45, 'rows': '10'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def getpage(request, title):
    try:
        mdpage = util.get_entry(title)
        htmlpage = md.convert(mdpage)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": htmlpage
        })
    except:
        return render(request, "encyclopedia/error.html", {
            "error": "Page not found!",
            "title": "Error!"
        })


def edit(request):
    content = (request.GET['content'])
    title = (request.GET['title'])
    if request.method == "GET":
        return HttpResponse("yay!")


def new(request):
    if request.method == "POST":
        # Process the result of the incoming POST request
        page = NewPageForm(request.POST)
        if page.is_valid():
            title = page.cleaned_data["title"]
            content = page.cleaned_data["content"]
            if util.get_entry(title):
                return HttpResponse('<h1>Page already exists!</h1>')
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("getpage", kwargs={'title': f"{title}"}))
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
