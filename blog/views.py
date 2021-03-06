from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.urls import reverse

from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
	
def post_detail(request, pk, new_comment=False):		
	post = get_object_or_404(Post, pk=pk)
	form = CommentForm()
	return render(request, 'blog/post_detail.html', {'post': post,'form': form,'comment': new_comment})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('blog:post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required	
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('blog:post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
	return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('blog:post_detail', pk=pk)

@login_required
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('blog:post_list')
	
def add_comment_to_post(request, pk):
	'''
	This function is called only within blog/post_detail.html.
	Upon submitting the comment form, the comment will be added
	to the database, but will not be displayed until a moderator
	has approved it.
	'''
	post = get_object_or_404(Post, pk=pk)
	form = CommentForm(request.POST)
	if form.is_valid():
		comment = form.save(commit=False)
		if request.user.is_authenticated:
			comment.author = request.user.username
		comment.post = post
		comment.save()
		return redirect('blog:post_detail', pk=pk, new_comment=True)
	
@login_required
def comment_approve(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('blog:post_detail', pk=comment.post.pk)
	
@login_required
def comment_remove(request, pk):
	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('blog:post_detail', pk=comment.post.pk)