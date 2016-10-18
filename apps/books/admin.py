from django.contrib import admin

from .models import Book, Review


class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'added_by', 'rating')
    search_fields = ('title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating')


admin.site.register(Book, BookAdmin)
admin.site.register(Review, ReviewAdmin)
