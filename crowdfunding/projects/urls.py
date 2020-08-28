from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projectsDetail/<int:pk>/', views.ProjectDetail.as_view()),
    path('pledges/', views.PledgeList.as_view()),
    path('pledges/<int:pk>', views.PledgeDetail.as_view()),
    path('projects/<int:pk>/', views.ProjectList.as_view()),

    # path('filter/', views.StoryFilterView.as_view(), name = 'filter'),
]

urlpatterns = format_suffix_patterns(urlpatterns)