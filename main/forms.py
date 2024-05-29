from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from main.models import Category, Todo


class TodoItemForm(forms.ModelForm):
    deadline = forms.DateTimeField(widget=forms.SelectDateWidget)
    class Meta:
        model = Todo
        fields = ['category', 'body', 'deadline']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(TodoItemForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CategoryForm, self).__init__(*args, **kwargs)


    def clean_name(self):
        name = self.cleaned_data['name']
        if Category.objects.filter(Q(name=name) & Q(user=self.user)).exists():
            raise ValidationError("Category with this name already exists!")
        return name

