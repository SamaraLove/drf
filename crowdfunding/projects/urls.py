from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:pk>/', views.ProjectDetail.as_view()),
    path('pledges/', views.PledgeList.as_view()),
    path('pledges/<int:pk>', views.PledgeDetail.as_view()),
    path('categories/', views.CategoryList.as_view()),
    path('categories/<str:category>', views.CategoryProject.as_view()),
    path('authors/', views.ProjectListAuthor.as_view()),
    # path('authors/(?P<category>.+)/$', views.ProjectListAuthor.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)