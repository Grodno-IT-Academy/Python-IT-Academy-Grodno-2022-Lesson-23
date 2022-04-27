from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Question, Choice
from django.utils import timezone
from .forms import ChoiceForm, QuestionForm
#limiting user view for users not logged in
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.utils.decorators import method_decorator
from authentication.decorators import allowed_users

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
#create question view

@method_decorator(allowed_users(allowed_roles=['customer']), name='dispatch')
class CreateQuestion(generic.CreateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/new_question.html'
    def form_valid(self, form):
        form.instance.pub_date = timezone.now()
        form.instance.author = self.request.user
        self.question = form.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('polls:detail', args=(self.question.id,))
# update view
class UpdateQuestion(generic.UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/new_question.html'
    def get_success_url(self):
        return reverse('polls:detail', args=(self.object.id,))

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
# delete view
class DeleteQuestion(generic.DeleteView):
    model = Question
    template_name = 'polls/delete_question.html'
    def get_success_url(self):
        return reverse('polls:index')
# create question with choices
@login_required(login_url=reverse_lazy('auth:login'))
@allowed_users(allowed_roles=['customer'])
def create_question_choices(request):
    choice_formset = inlineformset_factory(Question, Choice, fields=['choice_text'], extra=4)
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.pub_date = timezone.now()
            question.author = request.user
            question.save()
            formset = choice_formset(request.POST, instance=question)
            if formset.is_valid():
                formset.save()
                return redirect('polls:detail', pk=question.pk)
    else:
        question_form = QuestionForm()
        formset = choice_formset()
    return render(request, 'polls/question_choices.html',{
        'question_form': question_form,
        'formset': formset
    })
@login_required(login_url=reverse_lazy('auth:login'))
@allowed_users(allowed_roles=['customer'])
def update_question_choices(request, pk):
    question = get_object_or_404(Question, pk=pk)
    choice_formset = inlineformset_factory(Question, Choice, fields=['choice_text'], extra=2)
    if request.method == "POST":
        question_form = QuestionForm(request.POST, instance=question)
        question_form.save()
        formset = choice_formset(request.POST, instance=question)
        if question_form.is_valid() and formset.is_valid():
            formset.save()
            return redirect('polls:detail', pk=question.pk)
    else:
        question_form = QuestionForm(instance=question)
        formset = choice_formset(instance=question)
    return render(request, 'polls/question_choices.html',{
        'question_form': question_form,
        'formset': formset
    })
# function to add choice to question
@login_required(login_url=reverse_lazy('auth:login'))
def add_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
    return redirect('polls:detail', pk=question.pk)


# function view to vote without the actual view
@login_required(login_url=reverse_lazy('auth:login'))
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))