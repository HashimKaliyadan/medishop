# main/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def allow_manager(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not getattr(user, "is_manager", False):
            return redirect("/")   # change to any page you want for unauthorized
        return view_func(request, *args, **kwargs)
    return _wrapped

def allow_customer(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if not getattr(user, "is_customer", False):
            return redirect("/")   # change to customer landing if you want
        return view_func(request, *args, **kwargs)
    return _wrapped
