from django.urls import path
from .views import HabitListCreateView, HabitDetailView, PublicHabitListView

urlpatterns = [
    path('', HabitListCreateView.as_view(), name='habit-list-create'),
    path('<int:pk>/', HabitDetailView.as_view(), name='habit-detail'),
    path('public/', PublicHabitListView.as_view(), name='public-habit-list'),
]
