
# Create your views here.
# views.py

from django.shortcuts import render
from django.http import HttpResponse
import os
import time

def index(request):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_directory, 'templates')
    timestamp = int(time.time())  # Generate the timestamp

    return render(request, 'myapp/index.html', {'timestamp': timestamp})

def favicon(request):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    static_path = os.path.join(current_directory, 'static')  # Adjust the static directory path based on your project structure

    favicon_path = os.path.join(static_path, 'favicon.ico')
    if os.path.exists(favicon_path):
        with open(favicon_path, 'rb') as f:
            return HttpResponse(f.read(), content_type="image/x-icon")
    else:
        return HttpResponse(status=404)  # Return a 404 response if the file is not found
