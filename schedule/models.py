from django.db import models

# Create your models here.
class Task(models.Model):
	task_name = models.CharField(max_length=100)
	task_text = models.TextField(blank=True)
	due_date = models.DateField('finish by date', blank=True, null=True)
	
	def __str__(self):
		return self.task_name[:50]