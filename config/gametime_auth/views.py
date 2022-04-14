from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    return render(request, "gametime_auth/profile.html", {"page_group": "profile"})
