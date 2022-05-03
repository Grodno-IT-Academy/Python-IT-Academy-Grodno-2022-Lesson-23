from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Question, Choice, Urlentry, Leads
from django.utils import timezone
from .forms import ChoiceForm, QuestionForm, UrlentryForm, LeadsForm
#limiting user view for users not logged in
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory
from django.utils.decorators import method_decorator
from authentication.decorators import allowed_users
from django.contrib.auth.models import Group, User

#supporting functions
def is_customer(id_input):
    group = Group.objects.filter(id=id_input)
    for grp in group:
        if str(grp).find('customer') >= 0:
            groupstring = True
        else:
            groupstring = False
    return groupstring

def countme(iter):
    count=0
    for i in iter:
        count=count+1
    return count

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'questions_list'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context_object_name = 'links_list'
    def get_queryset(self):
        return Urlentry.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')[:10]
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

@method_decorator(allowed_users(allowed_roles=['customer','admin']), name='dispatch')
class CreateUrlentry(generic.CreateView):
    model = Urlentry
    fields = ['url_text']
    template_name = 'polls/new_question.html'
    def form_valid(self, form):
        cd = form.cleaned_data
        form.instance.create_date = timezone.now()
        form.instance.author = self.request.user
        form.instance.url_id = countme(Urlentry.objects.all())
        if is_customer(self.request.user.id):
            form.instance.url_short = Urlentry.num_to_sym_registered(form.instance.url_id)
        else:
            form.instance.url_short = Urlentry.num_to_sym_unregistered(form.instance.url_id)
        form.instance.snapshot = 'https://api.screenshotmachine.com?key=7a0150&url='+cd['url_text']+'&dimension=1024x768'
        form.instance.qr_code = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data='+cd['url_text']
        self.urlentry = form.save()
        form.instance.datetime_available_from = timezone.now()
        form.instance.datetime_available_to = timezone.now()
        form.instance.partner_ads = ''
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('polls:detail', args=(self.urlentry.id,))

# update view
class UpdateQuestion(generic.UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/new_question.html'
    def get_success_url(self):
        return reverse('polls:detail', args=(self.object.id,))

class DetailView(generic.DetailView):
    model = Urlentry
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
# @login_required(login_url=reverse_lazy('auth:login'))
# @allowed_users(allowed_roles=['customer'])
# def create_question_choices(request):
#     choice_formset = inlineformset_factory(Question, Choice, fields=['choice_text'], extra=4)
#     if request.method == "POST":
#         question_form = QuestionForm(request.POST)
#         if question_form.is_valid():
#             question = question_form.save(commit=False)
#             question.pub_date = timezone.now()
#             question.author = request.user
#             question.save()
#             formset = choice_formset(request.POST, instance=question)
#             if formset.is_valid():
#                 formset.save()
#                 return redirect('polls:detail', pk=question.pk)
#     else:
#         question_form = QuestionForm()
#         formset = choice_formset()
#     return render(request, 'polls/question_choices.html',{
#         'question_form': question_form,
#         'formset': formset
#     })

# create Url
@login_required(login_url=reverse_lazy('auth:login'))
def create_urls(request):
    urlentry_formset = inlineformset_factory(Urlentry, Leads, fields=['follower_info'], extra=0)
    if request.method == "POST":
        urlentry_form = UrlentryForm(request.POST)
        if urlentry_form.is_valid():
            urlentry = urlentry_form.save(commit=False)
            urlentry.create_date = timezone.now()
            urlentry.author = request.user
            urlentry.url_id = countme(Urlentry.objects.all())
            if is_customer(request.user.id):
                urlentry.url_short = Urlentry.num_to_sym_registered(urlentry.url_id)
            else:
                urlentry.url_short = Urlentry.num_to_sym_unregistered(urlentry.url_id)
            urlentry.snapshot = 'https://api.screenshotmachine.com?key=7a0150&url=' + str(urlentry_form[
                'url_text'])[73:].rstrip('</textarea>') + '&dimension=1024x768'
            urlentry.qr_code = 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=' + str(urlentry_form[
                'url_text'])[73:].rstrip('</textarea>')
            urlentry.datetime_available_from = timezone.now()
            urlentry.datetime_available_to = timezone.now()
            urlentry.partner_ads = ''
            urlentry.save()
           ############

            formset = urlentry_formset(request.POST, instance=urlentry)
            if formset.is_valid():
                formset.save()
                return redirect('polls:detail', pk=urlentry.pk)
    else:
        urlentry_form = UrlentryForm()
        formset = urlentry_formset()
    return render(request, 'polls/question_choices.html',{
        'question_form': urlentry_form,
        'formset': formset
    })
#
# @login_required(login_url=reverse_lazy('auth:login'))
# @allowed_users(allowed_roles=['customer'])
# def update_question_choices(request, pk):
#     question = get_object_or_404(Question, pk=pk)
#     choice_formset = inlineformset_factory(Question, Choice, fields=['choice_text'], extra=2)
#     if request.method == "POST":
#         question_form = QuestionForm(request.POST, instance=question)
#         question_form.save()
#         formset = choice_formset(request.POST, instance=question)
#         if question_form.is_valid() and formset.is_valid():
#             formset.save()
#             return redirect('polls:detail', pk=question.pk)
#     else:
#         question_form = QuestionForm(instance=question)
#         formset = choice_formset(instance=question)
#     return render(request, 'polls/question_choices.html',{
#         'question_form': question_form,
#         'formset': formset
#     })

@login_required(login_url=reverse_lazy('auth:login'))
@allowed_users(allowed_roles=['customer', 'admin'])
def update_urlentry(request, pk):
    urlentry = get_object_or_404(Urlentry, pk=pk)
    urlentry_formset = inlineformset_factory(Urlentry, Leads, fields=['follower_info'], extra=0)
    if request.method == "POST":
        urlentry_form = UrlentryForm(request.POST, instance=urlentry)
        urlentry_form.save()
        return redirect('polls:detail', pk=urlentry.pk)
    else:
        urlentry_form = UrlentryForm(instance=urlentry)
        formset = urlentry_formset(instance=urlentry)
    return render(request, 'polls/question_choices.html',{
        'question_form': urlentry_form,
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

def add_lead_and_redirect(request, hash):
    urlentry = get_object_or_404(Urlentry, url_short=hash)
    try:
        selected_leads = urlentry.leads_set.get(pk=request.POST['leads'])
    except (KeyError, Leads.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'urlentry': urlentry,
            'error_message': "Urlentry or Leads not found.",
        })
    else:
        selected_leads.follow_date = timezone.now()
        selected_leads.follower_info = request.META['HTTP_REFERER']
        selected_leads.follower_os_info = request.headers.get('User-Agent')
        selected_leads.follower_fromwhere = request.META['REMOTE_ADDR']
        selected_leads.save()
        return HttpResponseRedirect(urlentry.url_text)