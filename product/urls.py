from django.urls import path
from .views      import CategoryView, ThemeView, DetailView

urlpatterns = [
    path('/category_list', CategoryView.as_view()),
    path('/theme', ThemeView.as_view()),
    path('/detail/<int:product_id>', DetailView.as_view()),
]
