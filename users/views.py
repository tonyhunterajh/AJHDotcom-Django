from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        userForm = UserRegistrationForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            username = userForm.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}. You may now login!')
            return redirect('login')
    else:
        userForm = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': userForm})

@login_required
def profile(request):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=request.user)
        profile_update_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_update_form = UserUpdateForm(instance=request.user)
        profile_update_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_update_form': user_update_form,
        'profile_update_form': profile_update_form
    }

    return render(request, 'users/profile.html', context)