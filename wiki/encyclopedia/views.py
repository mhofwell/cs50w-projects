from django.shortcuts import render
from . import util
from django.http import HttpResponse


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def getpage(request, title):
    page = util.get_entry(title)
    # if page:
    return render(request, page)
    # else:
    # return HttpResponse('<h1>404 Page was found</h1>')
