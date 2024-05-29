from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
import datetime

current_date = datetime.datetime.now().date()

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'


class Todo(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(blank=True, null=True, validators=[MinValueValidator(current_date)])
    done = models.BooleanField(default=False)

    def __str__(self):
        return f"Todo of {self.user.username}"
