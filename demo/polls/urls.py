from django.urls import path
from . import views
#limit class views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

app_name = 'polls'
urlpatterns = [
    path('', view=views.IndexView.as_view(), name='index'),
    path('polls/new/', view=views.create_question_choices, name='new'),
    path('polls/update/<int:pk>/', view=views.update_question_choices, name="update"),
    path('choices/add/<int:pk>/', view=views.add_question, name='add_choice'),
    path('polls/delete/<int:pk>/', view=login_required(views.DeleteQuestion.as_view(), login_url=reverse_lazy('auth:login')), name='delete'),
    path('details/<int:pk>/', view=login_required(views.DetailView.as_view(), login_url=reverse_lazy('auth:login')), name='detail'),
    path('polls/<int:pk>/results/', view=login_required(views.ResultsView.as_view(), login_url=reverse_lazy('auth:login')), name='results'),
    path('polls/<int:question_id>/vote/', view=views.vote, name='vote'),
]