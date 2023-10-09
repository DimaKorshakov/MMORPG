from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'header', 'email', 'cat',)
    list_display_links = ('id', 'header',)
    search_fields = ('header',)
    prepopulated_fields = {"slug": ("header",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class CommentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super(CommentAdmin, self).save_model(
            request=request,
            obj=obj,
            form=form,
            change=change
        )

    list_display = ('name', 'created', 'author', 'email')
    list_filter = ('name', 'created', 'author', 'email')
    search_fields = ('name', 'created', 'author', 'email')


admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
