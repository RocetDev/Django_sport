from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from . import storage
from .forms import AthleteForm, JSONFileForm


def index(request):
    athletes = storage.read_base() 
    return render(request, 'index.html', {'athletes': athletes})


def add_form(request):
    if request.method == "POST":
        form = AthleteForm(request.POST)
        if form.is_valid():
            current_data = storage.read_base()
            current_data.append(form.cleaned_data)
            storage.write_base(current_data)
            return redirect('index')
    else:
        form = AthleteForm()

    return render(request, 'add_form.html', {'form': form})


def upload_file(request):
    if request.method == "POST":
        form = JSONFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_data = form.cleaned_data['json_file']
            current_data = storage.read_base()
            current_data.extend(uploaded_data)
            storage.write_base(current_data)
            
            return redirect('index')
    else:
        form = JSONFileForm()
        
    return render(request, 'upload_form.html', {'form': form})
