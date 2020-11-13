from django.shortcuts import render

from . import util

from markdown2 import Markdown
from django import forms
import random

markdowner = Markdown()

class Search(forms.Form):
    item= forms.CharField(widget=forms.TextInput(attrs={"class":"","placeholder":"Search"}))

class Post(forms.Form):
    title = forms.CharField(label="title")
    textarea=forms.CharField(widget=forms.Textarea(),label="")

class Edit(forms.Form):
    textarea= forms.CharField(widget=forms.Textarea(),label="")


def index(request):
    entries = util.list_entries()
    searches = []
    if request.method=="POST":
        form = Search(request.POST)
        if form.is_valid():
            item = form.cleaned_data["item"]
            for i in entries:
                if item in entries:
                    page = util.get_entry(item)
                    page_converted = markdowner.convert(page)
                    context = {
                        "page": page_converted,
                        "title":item,
                        "form":Search()
                    }
                    return render(request, "encyclopedia/entry.html",context)
                if item.lower() in i.lower():
                    searches.append(i)
                    context = {
                        "searches": searches,
                        "form": Search()
                    }
            return render(request, "encyclopedia/search.html",context)

        else:
            return render(request, "encyclopedia/index.html",{"form": form})

    else:
        return render(request,"encyclopedia/index.html",{
            "entries": util.list_entries(), "form":Search()
    })

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        page_converted = markdowner.convert(page)
        context = {
            "page": page_converted,
            "title": title,
            "form":Search()
        }

        return render(request, "encyclopedia/entry.html",context)
    else:
        return render(request, "encyclopedia/error.html",{"message": "Page not found", "form":Search()})

def create(request):
    if request.method=="POST":
        form= Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form":Search(),"message":"Pagealready exists"})
            else:
                util.save_entry(title,textarea)
                page = util.get_entry(title)
                page_converted = markdowner.convert(page)
                context = {
                    "form": Search(),
                    "page":page_converted,
                    "title":title
                }

                return render(request, "encyclopedia/entry.html",context)
    else:
        return render(request, "encyclopedia/create.html",{"form": Search(), "post": Post()})

def random_Page(request):
    if request.method == "GET":
        entries = util.list_entries()
        num = random.randint(0, len(entries)-1)
        page_random = entries[num]
        page = util.get_entry(page_random)
        page_converted = markdowner.convert(page)
        context = {
            "form": Search(),
            "page":page_converted,
            "title": page_random
        }
        return render(request, "encyclopedia/entry.html",context)

def edit(request,title):
    if request.method == "GET":
        page = util.get_entry(title)
        context = {
            "form": Search(),
            "edit": Edit(initial={"textarea":page}),
            "title":title
        }
        return render(request, "encyclopedia/edit.html",context)
    else:
        form=Edit(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            page = util.get_entry(title)
            page_converted = markdowner.convert(page)
            context = {
                "form": Search(),
                "page": page_converted,
                "title":title
            }
            return render(request, "encyclopedia/entry.html",context)


