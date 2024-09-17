from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class CandidateSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    username = forms.CharField(max_length=30, required=True, label="Username")
    email = forms.EmailField(max_length=255, required=True, label="Email")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise forms.ValidationError(
                "Password must be at least 8 characters long, include an uppercase letter, a lowercase letter, a number, and a special character."
            )
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'  # Automatically set the role to 'candidate'
        if commit:
            user.save()
        return user

class SignInForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Username or Email'}),
        label="Username or Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        required=True, 
        label="Password"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")
            elif not user.is_active:
                raise forms.ValidationError("This account is inactive.")
        return cleaned_data

# Similarly, you can define forms for recruiter and admin if needed.