import git
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def update(request):
    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''
        #ddddjjj
        repo = git.Repo("ecua-ciclismo/")
        # origin = repo.remotes.origin
        # origin.pull()
        repo.config_writer()
        head = repo.heads[0]
        head.checkout(force=True,filter=['tree:0','blob:none'])
        remo = repo.remote()
        remo.pull()
        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")