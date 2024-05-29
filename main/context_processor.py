from .models import Category


def categories(request):
    if request.user.is_anonymous:
        return {}
    else:
        categories = Category.objects.filter(user=request.user)
        return {'categories': categories}
