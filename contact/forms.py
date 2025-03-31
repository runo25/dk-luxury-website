from django import forms
from .models import ContactInquiry

class ContactForm(forms.ModelForm):
    """Form for users to submit contact inquiries."""

    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'message'] # Fields shown to the user
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-input'}), # Example: Add CSS classes
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number (Optional)', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'Your Message', 'rows': 4, 'class': 'form-textarea'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Add further customization if needed
        self.fields['name'].label = "Full Name"
        self.fields['phone'].required = False # Ensure phone is not required by the form
