from django.shortcuts import render
from . import util
from django.http import HttpResponse
from markdown2 import Markdown

md = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def getpage(request, title):
    try:
        page = util.get_entry(title)
        print(title)
        htmlpage = md.convert(page)
        print(htmlpage)
        return HttpResponse(htmlpage)
    except:
        return HttpResponse('<h1>404 Page was not found</h1>')
