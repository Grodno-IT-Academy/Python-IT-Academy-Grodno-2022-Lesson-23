from django.contrib import admin
from .models import Question, Choice

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['question_text']
    list_display = ('question_text', 'pub_date', 'was_published_recently', "update_date")
    list_filter = ['update_date', 'pub_date', 'question_text']
    search_fields = ['question_text', 'pub_date', 'update_date']
    list_per_page = 5
    date_hierarchy = 'pub_date'
    ordering = ['pub_date', 'question_text']

@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    fields = ['choice_text', 'question']
    list_display = ('choice_text', 'question', 'votes')
    list_filter = ['question', 'choice_text']