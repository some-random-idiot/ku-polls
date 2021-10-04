"""KU Poll's url patterns."""

from django.urls import path
from . import views

app_name = 'polls'  # Namespacing the urls
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:error_message>', views.index, name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote')
]
