from django.urls import path
from .views import ConsejoListView, TipListView

urlpatterns = [
    path('consejos/', ConsejoListView.as_view(), name='consejos'),
    path('tips/', TipListView.as_view(), name='tips'),
]
