from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from .models import Todo, Category
from django.contrib import messages
from .forms import TodoItemForm, CategoryForm


class HomePageView(LoginRequiredMixin, View):
    def get(self, request):
        todo_items = Todo.objects.all().order_by('-id').filter(user=request.user)
        search_query = request.GET.get('q', '')

        if search_query:
            todo_items = todo_items.filter(Q(body__icontains=search_query) | Q(category__name__icontains=search_query))
        page_size = request.GET.get('page_size', 10)
        page = request.GET.get('page', 1)
        paginator = Paginator(todo_items, page_size)
        page_obj = paginator.page(page)

        context = {
            'search_query': search_query,
            'page_obj': page_obj,
            'page_size': page_size
        }

        return render(request, 'home.html', context)

class TodoItemDetail(View):
    def get(self, request, id):
        todo_item = Todo.objects.get(id=id)
        return render(request, 'todo/detail.html', {'todo_item': todo_item})

class TodoItemDeleteConfirmation(View):
    def get(self, request, id):
        todo_item = Todo.objects.get(id=id)
        return render(request, 'todo/delete.html', {'todo_item': todo_item})

class TodoItemDelete(View):
    def get(self, request, id):
        todo_item = Todo.objects.get(id=id)
        todo_item.delete()
        messages.success(request, 'You have successfully deleted your todo item.')
        return redirect('todo:home')

class TodoItemAdd(View):
    def get(self, request):
        form = TodoItemForm(user=request.user)
        return render(request, 'todo/create.html', {'form': form})

    def post(self, request):
        form = TodoItemForm(data=request.POST, user=request.user)
        if form.is_valid():
            Todo.objects.create(
                category=form.cleaned_data['category'],
                user=request.user,
                body=form.cleaned_data['body'],
                deadline=form.cleaned_data['deadline']
            )

            messages.info(request, 'You have successfully created a todo item.')
            return redirect('todo:home')

        else:
            return render(request, 'todo/create.html', {'form': form})


class TodoItemEdit(View):
    def get(self, request, id):
        todo_item = Todo.objects.get(id=id)
        form = TodoItemForm(instance=todo_item, user=request.user)
        return render(request, 'todo/edit.html', {'form': form})

    def post(self, request, id):
        todo_item = Todo.objects.get(id=id)
        form = TodoItemForm(instance=todo_item, data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, 'You have successfully updated your todo item.')
            return redirect('todo:home')

        else:
            return render(request, 'todo/create.html', {'form': form})

class CategoryList(View):
    def get(self, request):
        categories = Category.objects.filter(user=request.user).order_by('-id')
        return render(request, 'category/list.html', {'categories': categories})


class CategoryAdd(View):
    def get(self, request):
        form = CategoryForm(user=request.user)
        return render(request, 'category/create.html', {'form': form})

    def post(self, request):
        form = CategoryForm(data=request.POST, user=request.user)
        if form.is_valid():
            c = form.save(commit=False)
            c.user = request.user
            c.save()
            name = form.cleaned_data['name']
            messages.success(request, f'You have successfully created a category named {name}')
            return redirect('todo:home')
        else:
            return render(request, 'category/create.html', {'form': form})


class CategoryEdit(View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        form = CategoryForm(instance=category, user=request.user)
        return render(request, 'category/edit.html', {'form': form})

    def post(self, request, id):
        category = Category.objects.get(id=id)
        form = CategoryForm(instance=category, data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'You Have Successfully Updated The Category.')
            return redirect('todo:category-list')

class CategoryDeleteConfirmation(View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        form = CategoryForm(instance=category, user=request.user)
        return render(request, 'category/delete.html', {'form': form, 'category': category})


class CategoryDelete(View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        category.delete()
        messages.info(request, 'You Have Deleted The Category Successfully.')
        return redirect('todo:category-list')


class TodoItemsByCategory(LoginRequiredMixin, View):
    def get(self, request, id):
        category = Category.objects.get(id=id)
        todo_items = Todo.objects.all().order_by('-id').filter(Q(user=request.user) & Q(category=category))
        search_query = request.GET.get('q', '')

        if search_query:
            todo_items = todo_items.filter(Q(body__icontains=search_query) | Q(category__name__icontains=search_query))
        page_size = request.GET.get('page_size', 5)
        page = request.GET.get('page', 1)
        paginator = Paginator(todo_items, page_size)
        page_obj = paginator.page(page)
        context = {
            'search_query': search_query,
            'page_obj': page_obj,
            'page_size': page_size
        }

        return render(request, 'home.html', context)



class TodoItemDone(LoginRequiredMixin, View):
    def get(self, request, id):
        todo_item = Todo.objects.get(id=id)
        todo_item.done = True
        todo_item.save()
        messages.info(request, 'You have completed a task.')
        return redirect('todo:home')
