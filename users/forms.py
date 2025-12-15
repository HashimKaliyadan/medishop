from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()
# Registration Form
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')
# Do the two passwords match?
    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if not p1 or not p2 or p1 != p2:
            raise forms.ValidationError("Passwords don't match.")
        return p2
    
    def save(self, commit=True, set_customer=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # by default mark as customer; manager accounts should be created via admin
        if set_customer:
            user.is_customer = True
        if commit:
            user.save()
        return user
# Login Form
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid email/password.")
            if not user.is_active:
                raise forms.ValidationError("This account is inactive.")
            self.user_cache = user
        return self.cleaned_data

    def get_user(self):
        return self.user_cache