from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from .models import ContactInquiry
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def contact_view(request):
    """
    Handles the display and submission of the contact form.
    Sends an email notification upon successful submission.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                # Save the inquiry to the database
                inquiry = form.save()

                # Prepare email content
                subject = f"New Contact Inquiry from {inquiry.name}"
                html_message = render_to_string('contact/email/inquiry_notification.html', {'inquiry': inquiry})
                plain_message = f"Name: {inquiry.name}\nEmail: {inquiry.email}\nPhone: {inquiry.phone or 'Not provided'}\nMessage:\n{inquiry.message}"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [settings.CONTACT_FORM_RECIPIENT_EMAIL]

                # Send the email
                send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message, fail_silently=False)

                # Add success message
                messages.success(request, "Thank you for your message! We'll get back to you soon.")

                # Redirect to the same page (or a dedicated success page)
                # Redirecting helps prevent form resubmission on refresh
                return redirect('contact:contact_form') # Redirect to the named URL

            except Exception as e:
                # Log the error for debugging
                logger.error(f"Error processing contact form submission or sending email: {e}", exc_info=True)
                # Show a generic error message to the user
                messages.error(request, "Sorry, there was an error submitting your message. Please try again later.")
                # Optionally, you could re-render the form with an error message
                # context = {'form': form}
                # return render(request, 'contact/contact.html', context)

        else:
            # Form is invalid, add error message (form will show specific field errors)
            messages.error(request, "Please correct the errors below.")
            # Fall through to render the form with errors

    else: # GET request
        form = ContactForm()

    context = {
        'form': form,
    }
    return render(request, 'contact/contact.html', context)
