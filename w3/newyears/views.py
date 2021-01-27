from django.shortcuts import render
import datetime
from django.http import HttpResponse

# Create your views here.


def nye(request):
    now = datetime.datetime.now()
    return render(request, "newyears/index.html", {
        "newyear": now.month == 1 and now.date == 1
    })
