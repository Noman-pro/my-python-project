from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPES, required=True, help_text='Select your user type.')
    profile_picture = forms.ImageField(required=False, help_text='Optional. Upload your profile picture.')
    address_line1 = forms.CharField(max_length=255, required=True, help_text='Required.')
    city = forms.CharField(max_length=100, required=True, help_text='Required.')
    state = forms.CharField(max_length=100, required=True, help_text='Required.')
    pincode = forms.CharField(max_length=6, required=True, help_text='Required. 6-digit pincode.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type'],
                address_line1=self.cleaned_data['address_line1'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                pincode=self.cleaned_data['pincode']
            )
            if self.cleaned_data.get('profile_picture'):
                profile.profile_picture = self.cleaned_data['profile_picture']
                profile.save()
        return user
