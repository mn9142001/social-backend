from django.contrib import admin
from .models import Post, Comment, SnippetFile
# Register your models here.

admin.site.register([Post, Comment, SnippetFile])