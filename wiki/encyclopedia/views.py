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
        htmlpage = md.convert(page)
        return HttpResponse(htmlpage)
    except:
        return HttpResponse('<h1>Page was not found</h1>')


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
