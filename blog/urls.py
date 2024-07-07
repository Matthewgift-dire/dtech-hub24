from django.urls import path
from blog import views

urlpatterns = [
	path('', views.index, name='index'),
	path('<slug:slug>', views.post_detail, name='post_detail'),
	path('tag/<tag>/', views.blog_tag, name='blog_tag'),
	path('category/<post_category>/', views.post_category, name='post_category'),
	path('author?<post_author>',views.post_author, name='post_author'),
	path('posts/<posted_by>', views.author_post, name='author_post'),
	path('search/', views.post_search, name='search'),
	path('contact/', views.blog_contact, name='contact'),
	path('contact/success/', views.success, name='success'),
	path('about/', views.about, name='about'),
	path('blog/', views.blog, name='blog'),
	path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
]