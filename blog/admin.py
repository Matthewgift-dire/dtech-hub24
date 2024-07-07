from django.contrib import admin
from blog.models import Post, Author, Tag, Comment
from blog.forms import SignupForm
# Register your models here.

class PostAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_on',)
	search_fields = ('title', 'author',)
	prepopulated_fields = {"slug": ('title',)}
	
	
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment)
