import git
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging

@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        logging.basicConfig(level=logging.INFO)

        # repo = git.Repo("ecua-ciclismo/")
        # origin = repo.remotes.origin
        # origin.pull()

        g = git.Git('ecua-ciclismo/')
        g.pull('origin','main')

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")

def current_datetime(request):
    #now = datetime.now()
    #html = "<html><body>It is now %s.</body></html>" % now
    return render(request, "politica.html")