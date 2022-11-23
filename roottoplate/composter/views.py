from django.shortcuts import render
from django.http import HttpResponseBase
# Create your views here.
def index(request):
    return HttpResponseBase("Composter composting")

