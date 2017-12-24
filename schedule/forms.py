from django import forms

from .models import Task

class TaskForm(forms.ModelForm):
	class Meta:
		model = Task
		fields = ('task_name', 'task_text', 'due_date')
		widgets = {
			'task_text': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
			'due_date': forms.SelectDateWidget(
				empty_label=('Year', 'Month', 'Day')
			),
		}
