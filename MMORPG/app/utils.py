from .models import *


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.all()
        comment = Comment.objects.all()
        context['cats'] = cats
        context['comment'] = comment

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

