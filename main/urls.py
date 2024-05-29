from django.urls import path
from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('todo-items/<int:id>', views.TodoItemDetail.as_view(), name='detail'),
    path('todo-items/<int:id>/delete/confirm', views.TodoItemDeleteConfirmation.as_view(), name='delete-confirmation'),
    path('todo-items/<int:id>/delete', views.TodoItemDelete.as_view(), name='delete'),
    path('todo-items/create', views.TodoItemAdd.as_view(), name='create'),
    path('todo-items/<int:id>/edit', views.TodoItemEdit.as_view(), name='edit'),
    path('todo-items/<int:id>/done', views.TodoItemDone.as_view(), name='done'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/create', views.CategoryAdd.as_view(), name='category-create'),
    path('categories/<int:id>/edit', views.CategoryEdit.as_view(), name='category-edit'),
    path('categories/<int:id>/delete/confirm', views.CategoryDeleteConfirmation.as_view(), name='category-delete-confirmation'),
    path('categories/<int:id>/delete', views.CategoryDelete.as_view(), name='category-delete'),
    path('categories/<int:id>/todo-items', views.TodoItemsByCategory.as_view(), name='todo-items-by-category'),
]
