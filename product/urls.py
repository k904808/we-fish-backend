from .views      import CategoryListView
from django.urls import path

urlpatterns = [
    path('/category', CategoryListView.as_view())
]
