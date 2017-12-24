from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm

# Create your views here.
def task_list(request):
	list_of_tasks = Task.objects.all()
	form = TaskForm(
		initial = {
			'task_name': 'Name of task',
			},
	)
	context = {'list_of_tasks': list_of_tasks, 'form': form}
	return render(request, 'schedule/task_list.html', context)

@login_required	
def task_add(request):
	if request.method == "POST":
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save(commit=False)
			task.save()
	return redirect('schedule:task_list')


@login_required	
def task_remove(request, pk):
	print('Entered function')
	task = get_object_or_404(Task, pk=pk)
	task.delete()
	return redirect('schedule:task_list') 

@login_required
def task_edit(request, pk):
	return redirect('schedule:task_list')