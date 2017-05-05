from django.contrib import admin
from .models import Classification, Article, Content, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


class ContentInline(admin.TabularInline):
    model = Content
    extra = 0
    # classes = ['collapse']


class ArticleAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_date'     # include a date-based drilldown navigation by that field.
    fieldsets = [
        (None,               {'fields': ['author', 'classification']}),
        ('content',          {'fields': ['title', 'source']}),
        ('Date information', {'fields': [('created_date','updated_date')]}),
    ]
    inlines = [ContentInline, CommentInline]
    list_display = ['title', 'author', 'classification', 'created_date', 'updated_date']
    list_editable = ['classification', 'updated_date']
    list_filter = ['classification', 'created_date', 'author']
    search_fields = ['title']

admin.site.register(Article, ArticleAdmin)


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent_classification')

    def parent_classification(self, obj):
        return obj.parent

    parent_classification.empty_value_display = "it's a root classification."

admin.site.register(Classification, ClassificationAdmin)
