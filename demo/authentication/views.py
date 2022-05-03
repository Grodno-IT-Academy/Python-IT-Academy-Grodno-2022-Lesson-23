from django.shortcuts import render, redirect
from .forms import CreateUserForm, CheckCustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users, staff_only
from django.contrib.auth.models import User, Group
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .models import Profile, Custcode

#profile page
@login_required(login_url='auth:login')
# @allowed_users(allowed_roles=['customer', 'admin'])
def profile_page(request, pk):
    profile = Profile.objects.get(pk=pk)
    group = Group.objects.filter(id=profile.user.id).all()
    for grp in group:
        if str(grp).find('customer')>=0:
            groupstring = 'customer'
        else:
            groupstring = 'user'
    return render(request, 'authentication/profile.html', context={
        'profile': Profile.objects.get(pk=pk),'group':group, 'groupstring':groupstring,
    })

# Create your views here.
decorators = [login_required(login_url='auth:login'), staff_only]
@method_decorator(staff_only, name='dispatch')
class UsersView(generic.ListView):
    template_name = 'authentication/users.html'
    context_object_name = 'user_list'
    def get_queryset(self):
        return Profile.objects.all()

@login_required(login_url='auth:login')
def customers_page(request, pk):
    profile = Profile.objects.get(pk=pk)
    user = profile.user
    if not Group.objects.filter(name='customer').exists():
        Group.objects.create(name='customer')
    if request.method == "POST":
        form = CheckCustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cs = Custcode(codeword = cd['codeword'])
            #cs.save()
            if cd['codeword']=='elk':
                if not Group.objects.filter(name='customer').exists():
                    Group.objects.create(name='customer')
                user.save()
                hulk = Group.objects.get(name='customer')
                hulk.user_set.add(user)  # user added to group of hulk
                user.save()
                user.groups.add(hulk)
                hulk.save()
                user.groups.add(Group.objects.get(name='customer'))
                messages.success(request, 'User was successfully addedd to Customers group')
            else:
                messages.error(request, 'Incorrect codeword, please try again')
    else:
        form = CheckCustomerForm()
        if form.is_valid():
            form.save()
    group = Group.objects.filter(id=profile.user.id)
    for grp in group:
        if str(grp).find('customer')>=0:
            groupstring = 'customer'
        else:
            groupstring = 'user'
    return render(request, 'authentication/customer.html', context={
        'profile': Profile.objects.get(pk=pk), 'group': group, 'method': request.method,
        'form': form, 'groupstring':groupstring,
        })


@unauthenticated_user
def register_page(request):
    if not Group.objects.filter(name='customer').exists():
        Group.objects.create(name='customer')
        Group.objects.create(name='admin')
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('username'))
            return redirect('auth:login')
        else:
            messages.error(request, 'Got a registration error: ' + str(form.error_messages))
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'authentication/reg.html', context)

@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            messages.warning(request, 'Username or Password is incorrect')
    return render(request, 'authentication/login.html')

def logout_page(request):
    logout(request)
    return redirect('auth:login')