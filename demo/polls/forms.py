from django.forms import ModelForm
from .models import Question, Choice, Urlentry, Leads

class UrlentryForm(ModelForm):
    class Meta:
        model = Urlentry
        fields = ['url_text']

class LeadsForm(ModelForm):
    class Meta:
        model = Leads
        fields = ['follower_info']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']