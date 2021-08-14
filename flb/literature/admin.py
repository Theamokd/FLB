from django.contrib import admin

from .models import Article, Article_image, Author, Book, Issue, Journal

# Register your models here.
admin.site.register(Journal)
admin.site.register(Issue)
admin.site.register(Article)
admin.site.register(Article_image)
admin.site.register(Author)
admin.site.register(Book)
