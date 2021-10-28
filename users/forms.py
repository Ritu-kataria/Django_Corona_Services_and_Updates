from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db.models import fields
from django.contrib.auth import authenticate
from users.models import CustomUser
from users.models import Profile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'address', 'phone', 'file', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            user = CustomUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use.")

    '''def save(self, commit=True):
        user = CustomUser.objects.create_user(
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        return user'''

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("invalid credentials!")


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'email', 
            'phone', 
            'address', 
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            't_covid_beds',
            'v_covid_beds',
            'o_covid_beds',
            't_ventilators',
            'v_ventilators',
            'o_ventilators',
            't_icu_beds',
            'v_icu_beds',
            'o_icu_beds',
            't_oxygen_beds',
            'v_oxygen_beds',
            'o_oxygen_beds',
        ]