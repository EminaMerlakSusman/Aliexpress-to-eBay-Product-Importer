from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
import sys
from djangonautic.forms import HomeForm
import _sqlite3
import os.path
from djangonautic.models import Product

from djangonautic.savbrb import bla


def homepage(request):
    if request.method == "POST":
        print("request values")
        form = HomeForm(request.POST)
        if form.is_valid():
            print("Form was valid")
            text = form.cleaned_data['post']
            args = {'form': form, 'text': text}
            url = Product(productURL = text)
            url.save()
            print(os.curdir)
            from djangonautic.additem import make_api_call
            make_api_call()
            context = {'title': "URL {} has been saved to database!".format(text)}
            return render(request, "script_run.html", context=context)



    else:
        print("ewe")
        form = HomeForm()
        return render(request, "homepage.html", {'form': form, 'text': 'bla'})

def about(request):
    #return HttpResponse("about")
    return render(request, "about.html")
