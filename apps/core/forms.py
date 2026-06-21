from django import forms
from apps.core.models import ContactInquiry, FranchiseApplication, JobApplication, NewsletterSubscriber

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Contact Number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'How can we help you?', 'rows': 4}),
        }


class FranchiseForm(forms.ModelForm):
    class Meta:
        model = FranchiseApplication
        fields = ['name', 'phone', 'email', 'city', 'investment_budget', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Target City'}),
            'investment_budget': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 15-20 Lakhs'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Brief details about your business background', 'rows': 4}),
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'resume', 'cover_letter']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Why are you a good fit for this role?', 'rows': 4}),
        }
