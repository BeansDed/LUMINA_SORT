"""
Authentication views - Signup and login.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from ..forms import SignUpForm


def signup(request):
    """User registration view."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Welcome to LUMINA_SORT, {username}!')
            return redirect('gallery')
    else:
        form = SignUpForm()
    
    return render(request, 'editor/signup.html', {'form': form})
