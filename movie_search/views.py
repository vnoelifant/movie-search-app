from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# This is a test
def home(request):
    return HttpResponse("This is a test for movie search app skeleton!")