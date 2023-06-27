from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from store.models import UserProfile

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['user', 'phone_number', 'email', 'profile_picture']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

    def save(self, commit=True):
        user = super().save(commit=False)
        username = self.cleaned_data['user']
        password = self.cleaned_data['password']

        # Create a new user
        new_user = User.objects.create_user(username=username, password=password)

        # Associate the new user with the user profile
        user.user = new_user

        if commit:
            user.save()

        return user
