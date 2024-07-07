#libraries from Django
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout, get_user 
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

#classes from app
from .forms import SignupForm, LoginForm
from blog.models import Post, Tag, Comment, Author
from blog.forms import CommentForm, ContactForm
# Create your views here.

#home page
def index(request):
	
	username =get_user(request).username
	posts = Post.objects.filter(post_category__icontains ="popular").exclude(status='0')[:7]
	recent_posts = Post.objects.filter(post_category__icontains='recent').exclude(status='0')[:5]
	trending_posts = Post.objects.filter(post_category__icontains='trend').exclude(status='0')[:5]
	tags = Tag.objects.all()
	context = {
		'posts': posts,
		'trending_posts': trending_posts,
		'recent_posts': recent_posts,
		'tags': tags,
		'username': username,
	}
	return render(request, 'blog/index.html', context)
	
#posts details	
def post_detail(request, slug):
	post = Post.objects.get(slug=slug)
	related_posts = Post.objects.filter(tag=post.tag).exclude(title=post)[:5]
	tags = Tag.objects.all()
	comments = Comment.objects.order_by("-created_on").filter(post=post)[:7]
	form = CommentForm()
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = Comment(
				author=get_user(request).username,
				body=form.cleaned_data['body'],
				post=post,
			)
			print(comment)
			comment.save()
			return HttpResponseRedirect(request.path_info)
	context = {
		'post': post,
		'related_posts': related_posts,
		'tags': tags,
		'comments': comments,
		'form': form,
	}
	return render(request, 'blog/post_detail.html', context)
	
#tag page
def blog_tag(request, tag):
	tags_ = Tag.objects.exclude(name=tag)
	posts = Post.objects.filter(tag__name__icontains=tag).order_by("created_on")
	paginator = Paginator(posts, 5)
	page_number = request.GET.get("page", 1)
	try:
	    posts = paginator.page(page_number)
	except EmptyPage:
	    posts = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		posts = paginator.page(1)
	context = {
		'posts': posts,
		 'tags' :tags_,
	}
	
	return render(request, 'blog/post_category.html', context)
	
#category page
def post_category(request, post_category):
	tags_ = Tag.objects.exclude(name=post_category)
	posts = Post.objects.filter(post_category__icontains=post_category).order_by("created_on")
	paginator = Paginator(posts, 5)
	page_number = request.GET.get("page", 1)
	try:
	    posts = paginator.page(page_number)
	except EmptyPage:
	    posts = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		posts = paginator.page(1)
	context = {
		'posts': posts,
		 'tags' :tags_,
	}
	
	return render(request, 'blog/post_category.html', context)
	
#post author 
def post_author(request, post_author):
	author = Author.objects.get(name=post_author)
	posts = Post.objects.filter(author__name__icontains=author).order_by("created_on")
	context = {
		'author': author,
		'posts': posts
	}
	
	return render(request, 'blog/author.html', context)
	
#author posts
def author_post(request, posted_by):
	tags_ = Tag.objects.all()
	posts = Post.objects.filter(author__name__icontains=posted_by).order_by("created_on")
	paginator = Paginator(posts, 5)
	page_number = request.GET.get("page", 1)
	try:
	    posts = paginator.page(page_number)
	except EmptyPage:
	    posts = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		posts = paginator.page(1)
	context = {
		'posts': posts,
		 'tags' :tags_,
	}
	
	return render(request, 'blog/post_category.html', context)

#search page
def post_search(request):
	if request.method == 'POST':
	   search_query = request.POST['search_query']
	   posts = Post.objects.filter(Q(title__icontains=search_query) | Q(author__name__icontains=search_query))
	   #paginator = Paginator(posts, 1)
#	   page_number = request.GET.get("page", 1)
#	   try:
#	       posts = paginator.page(page_number)
#	   except EmptyPage:
#	       posts = paginator.page(paginator.num_pages)
#	   except PageNotAnInteger:
#		   posts = paginator.page(1)
	   context = {
	   	'query':search_query,
	   	'posts':posts,
	   }
	   return render(request, 'blog/search.html', context)
	else:
		return render(request, 'blog/search.html',{})
		
#contact page
def blog_contact(request):
	form = ContactForm()
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			
			EmailMessage(
				'{} From, {}'.format(subject, name),
				message,
				'form-response@DTechHub',
				['dtechhub24@gmail.com'],
				reply_to=[email]
			).send()
			
			if EmailMessage.send:
				print("email sent")
				messages.success(request, message="Form submitted successfully!")
			
			return HttpResponseRedirect('success')
			
		else:
			form = ContactForm()
			
	return render(request, 'blog/contact.html', {'form': form})
			
return_=False 
def success(request):
	global return_
	return_ = True
	if return_:
		return redirect('contact')
	
	return render(request, "blog/success.html")
	

def about(request):
	return render(request, "blog/about.html")
	
#blog page	
def blog(request):
	posts = Post.objects.all()
	tags_ = Tag.objects.all()
	paginator = Paginator(posts, 5)
	page_number = request.GET.get("page", 1)
	try:
	    posts = paginator.page(page_number)
	except EmptyPage:
	    posts = paginator.page(paginator.num_pages)
	except PageNotAnInteger:
		posts = paginator.page(1)
	context = {
		'posts': posts,
		'tags': tags_,
	}
	return render(request, "blog/post_category.html", context)
	

not_user = False
# signup page
def user_signup(request):
    form = SignupForm()
    if not_user:
    	messages.error(request, "Register with us first!")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'blog/signup.html', {'form': form})

# login page
error_check = 5
def user_login(request):
    global error_check, not_user
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('index')
            else:
            	error_check -= 1
            	messages.error(request, "Invalid Credentials")
            	print(error_check)
            	if error_check == 2:
            		messages.error(request, "oops!! seems you don't have an account with us create one!")
            	if error_check == 1:
            		not_user = True
	            	return redirect('signup')
            		
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')
    
    