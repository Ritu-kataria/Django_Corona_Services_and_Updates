from django.shortcuts import redirect, render
from users import forms
from users.forms import UserRegistrationForm, UserLoginForm, UserForm, ProfileForm
from django.contrib.auth import authenticate, login as h_login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from users.models import Profile
from django.http import HttpResponseRedirect
from datetime import datetime


# Create your views here.
def register(request):
    context = {}
    if request.method == 'POST':
        form=UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            form.save()
            messages.success(request, 'Registration Successfull!')
            return redirect('login')
        context['register_form'] = form
        
    else:
        form = UserRegistrationForm()
        context['register_form'] = form
    return render(request, "account/register.html",context)


def login(request):
    context = {}
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                h_login(request, user)
                messages.success(request, 'Login successfull!')
                return redirect('hospital_dashboard')
            else:
                messages.error(request, 'Invalid Credentials.')
                messages.error(request, form.errors)
    else:
        form = UserLoginForm()
        context['login_form'] = form
    return render(request, "account/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


def hospital_dashboard(request):
    return render(request, "account/hospital_dashboard.html")


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'account/profile-update.html'

    def post(self, request):

        post_data = request.POST or None

        user_form = UserForm(post_data, instance=request.user)
        #profile = Profile.objects.get(user = request.user)
        #profile_form = ProfileForm(request.POST, instance = profile)
        profile_form = ProfileForm(post_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('hospital_dashboard'))

        context = self.get_context_data(
                                        user_form=user_form,
                                        profile_form=profile_form
                                    )

        return self.render_to_response(context)     

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


