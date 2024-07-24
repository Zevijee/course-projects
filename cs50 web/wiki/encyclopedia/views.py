import markdown2
from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import choice


from . import util

md = markdown2.markdown

class NewForm(forms.Form):
    Title = forms.CharField(max_length=200, label='')
    Body = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '20'}), label='')

class EditForm(forms.Form):
    Body = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '20'}), label='')

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = next((util.get_entry(t) for t in [title, title.capitalize(), title.upper()] if util.get_entry(t)), None)
    page_title = title if entry else title.capitalize()


    if entry:
        page = md(entry)
    else:
        return HttpResponseRedirect(reverse('not_found', args=[title]))

    return render(request, 'encyclopedia/title.html', {'page': page, 'page_title': page_title})


def search(request):
    search_entry = request.POST.get('q').strip()
    substrings = []

    for i in util.list_entries():
        if i.lower() == search_entry.lower():
            return HttpResponseRedirect(reverse('title', args=[i]))
        if search_entry.lower() in i.lower():
            substrings.append(i)

    if substrings:
        return render(request, "encyclopedia/search.html", {
            'substrings': substrings, 'search_entry': search_entry
            })
    else:
        return HttpResponseRedirect(reverse('not_found', args=[search_entry]))


def addNewPage(request):
    if request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['Title']
            for i in util.list_entries():
                if i.lower() == title.lower():
                    message = f'A page with the title {i} allready exist'
                    return render(request, "encyclopedia/addNewPage.html", {
                        'form': NewForm(), 'message': message
                    })
            body = form.cleaned_data['Body']

            util.save_entry(title.capitalize(), body)
            return redirect('title', title=title)

    return render(request, "encyclopedia/addNewPage.html", {
        'form': NewForm()
    })

def edit(request, title):
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['Body']
            util.save_entry(title, body)
            return redirect('title', title=title)


    able_to_edit = False

    for i in util.list_entries():
        if i.lower() == title.lower():
            able_to_edit = True
            break

    if not able_to_edit:
        return HttpResponseRedirect(reverse('not_found', args=[title]))

    existing_page_content = util.get_entry(title)

    initial_data = {'Body': existing_page_content}
    form = EditForm(initial=initial_data)

    return render(request, "encyclopedia/edit.html", {
        'form': form, 'title': title
    })


def not_found(request, title):
    return render(request, "encyclopedia/not_found.html", {
        'title': title
    }, status=404)

def Random_Page(request):
    entrys = util.list_entries()

    title = choice(entrys)

    return redirect('title', title=title)
