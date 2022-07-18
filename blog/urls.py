from django.urls import path
from blog.views import *

urlpatterns = [
    path('', index, name="index"),
    path('create/', PostCreateView.as_view(), name='create'),
    path('create-category/', CategoryCreateView.as_view(), name='create-category'),
    path('category-posts/<slug:slug>', categoryPosts, name='category-posts'),
    path('<slug>/', PostDetailView.as_view(), name='detail'),
    path('<slug>/update', PostUpdateView.as_view(), name='update'),
    path('<slug>/delete', PostDeleteView, name='delete'),
    path('like/<slug>/', like, name='like')
]
