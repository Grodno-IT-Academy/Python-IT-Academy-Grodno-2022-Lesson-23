from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wraper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('polls:index')
        else:
            return view_func(request, *args, **kwargs)
    return wraper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = []
            if request.user.groups.exists():
                groups = request.user.groups.all()
            # compare group name to list of allowed groups
            for group in groups:
                if group.name in allowed_roles:
                    return view_func(request, *args, **kwargs)
            return redirect('polls:index')
        return wrapper_func
    return decorator

def staff_only(view_func):
    def wraper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return HttpResponse('You are not allowed to see this page!')
    return wraper_func