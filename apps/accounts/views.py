from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserRegistrationForm, UserProfileForm, UserUpdateForm
from .models import UserProfile
from apps.properties.models import Inquiry


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('properties:property_list')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('properties:property_list')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'You have been logged out successfully.')
        return super().dispatch(request, *args, **kwargs)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('properties:property_list')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Real Estate Management.')
            return redirect('properties:property_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    user_properties = request.user.properties.all()[:5]

    received_inquiries = Inquiry.objects.filter(property__owner=request.user, is_read=False).select_related('property', 'user').order_by('-created_at')[:5]
    sent_inquiries = Inquiry.objects.filter(user=request.user).select_related('property').order_by('-created_at')[:5]

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_properties': user_properties,
        'received_inquiries': received_inquiries,
        'sent_inquiries': sent_inquiries,
    }
    return render(request, 'accounts/profile.html', context)
