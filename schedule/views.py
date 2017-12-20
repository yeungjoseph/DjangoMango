from django.shortcuts import render

from .models import Task

# Create your views here.
def index(request):
	list_of_tasks = Task.objects.all()
	context = {'list_of_tasks': list_of_tasks}
	return render(request, 'schedule/index.html', context)