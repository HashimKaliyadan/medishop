from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_redirect(request):
    user = request.user

    if getattr(user, "is_manager", False):
        return redirect("managers:dashboard")

    return redirect("customers:home")
