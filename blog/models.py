from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from bs4 import BeautifulSoup
# Create your models here.


WORDS_PER_MINUTE = 100
class Post(models.Model):
	
	TRENDING_POST='Trend'
	POPULAR_POST='Popular'
	RECENT_POST='Recent'
	POST_CATEGORY_CHOICES = {
    	TRENDING_POST: "Trending",
    	POPULAR_POST: "Popular",
    	RECENT_POST: "Latest",
	}
	
	DRAFT = '0'
	PUBLISH = '1'
	STATUS = {
		DRAFT: 'Draft',
        PUBLISH: 'Publish',
      }
      
	title = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True, default='', null=False)
	author = models.ForeignKey("Author", on_delete=models.CASCADE)
	tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
	
	post_category = models.CharField(
		max_length=20, 
		choices=POST_CATEGORY_CHOICES,
		default=RECENT_POST
	)
	status = models.CharField(
		max_length=20,
		choices=STATUS,
		default=DRAFT
	)
	
	updated_on = models.DateTimeField(auto_now=True)
	created_on = models.DateTimeField(auto_now_add=True)
	content = tinymce_models.HTMLField()
	def read_time(self):
	       soup = BeautifulSoup(self.content, 'html.parser')
	       text = soup.get_text()
	       word_count = len(text.split())
	       read_time = round(word_count / WORDS_PER_MINUTE)
	       return read_time
	       
	cover_image = models.ImageField(upload_to='static/images/')
		
	class meta:
		ordering = ['-created_on']
		
	def __str__(self):
		return self.title
	
	
class Author(models.Model):
	name = models.CharField(max_length=20)
	profile_img = models.ImageField(upload_to='static/images/')
	about_info = models.TextField(default="author has not yet uploaded information")
	
	class meta:
		verbose_name_plural = 'authors'
		
	def __str__(self):
		return str(self.name)
	
	
class Tag(models.Model):
	name = models.CharField(max_length=30)
	
	class meta:
		verbose_name_plural = 'tags'
	
	def __str__(self):
		return self.name

class Comment(models.Model):
	author = models.CharField(max_length=30)
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey("Post", on_delete=models.CASCADE)    
	
	def __str__(self):
		return self.author
		