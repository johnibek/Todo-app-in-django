from django.contrib import admin
from .models import Todo, Category


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    model = Todo
    list_display = ['user' , 'datetime' ,'done']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['name' , 'slug']
    prepopulated_fields = {'slug': ('name',)}
