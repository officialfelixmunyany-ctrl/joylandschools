from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, StudentProfile
from core.models import Announcement


class TeacherLoginForm(AuthenticationForm):
    # Use AuthenticationForm defaults; keep explicit labels for clarity
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure Bootstrap form-control class is present on widgets by default.
        for name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            classes = (existing + ' form-control').strip()
            field.widget.attrs['class'] = classes


class StudentAccessForm(forms.Form):
    assessment_number = forms.CharField(required=False, label='Assessment Number')
    admission_number = forms.CharField(required=False, label='Admission Number')

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('assessment_number') and not cleaned.get('admission_number'):
            raise forms.ValidationError('Provide either assessment number or admission number')
        return cleaned


class AdminCreateUserForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)
    send_email = forms.BooleanField(required=False, initial=True, label='Send credentials by email')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'message', 'is_active', 'priority')


class RegistrationRequestForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()
    country_code = forms.CharField(max_length=8, required=False)
    phone = forms.CharField(max_length=32, required=False)
    address = forms.CharField(required=False)
    month = forms.IntegerField(required=False, min_value=1, max_value=12)
    day = forms.IntegerField(required=False, min_value=1, max_value=31)
    year = forms.IntegerField(required=False, min_value=1900, max_value=2100)
    heard_friend = forms.BooleanField(required=False)
    heard_google = forms.BooleanField(required=False)
    heard_other = forms.BooleanField(required=False)
    agree = forms.BooleanField(required=True, error_messages={'required': 'You must agree to the registration rules.'})

    def clean(self):
        cleaned = super().clean()
        # Basic sanity: must agree
        if not cleaned.get('agree'):
            raise forms.ValidationError('You must agree to the registration rules to continue.')
        return cleaned

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = 'form-control'
            if isinstance(field.widget, forms.CheckboxInput):
                css = ''
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (existing + ' ' + css).strip()
