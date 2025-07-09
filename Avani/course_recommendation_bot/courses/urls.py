from .views import recommend_course
from django.urls import path, include
from .views import index
urlpatterns = [
    path("api/recommend/", recommend_course, name="recommend_course"),
    path("index/", index,name='index'),
]