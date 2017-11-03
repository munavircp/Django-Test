from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile
#class RegistrationForm(UserCreationForm):
#    email = forms.EmailField(required=True)
#
#    class Meta:
#        model = User
#        fields = {
#            'username',
#            'first_name',
#            'last_name',
#            'email',
#            'password1',
#            'password2',
#            
#
#
#        }
#
#    def save(self, commit=True):
#        user = super(RegistrationForm, self).save(commit=False)
#        user.first_name = self.cleaned_data['first_name']
#        user.last_name = self.cleaned_data['last_name']
#        user.email = self.cleaned_data['email']
#
#        if commit:
#            user.save()
#
#        return user

class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }

    password1 = forms.CharField(label=("Password"),
        widget=forms.PasswordInput(
            attrs={
        'placeholder':'read instruction at right side '
        }
        ))

    password2 = forms.CharField(label=("Password confirmation"),
        widget=forms.PasswordInput)
    
    username = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(required=True, widget=forms.TextInput)




    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name'] 
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('description', 'city', 'phone', 'website', 'image')


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',      
        )

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')    



class EditUserProfileForm(forms.ModelForm):
    
    class Meta:
        model=UserProfile
        fields=['description', 'city', 'phone', 'website', 'image'] 
 

    def __init__(self, *args, **kwargs):
        #self.user=kwargs.pop('user') 
        super(EditUserProfileForm, self).__init__(*args, **kwargs) 
        