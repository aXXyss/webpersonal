from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name', '')
            company = request.POST.get('company', '')
            email = request.POST.get('email', '')
            zone = request.POST.get('zone', '')
            content = request.POST.get('content', '')
            avisolegal = request.POST.get('avisolegal', '')
            publicidad = request.POST.get('publicidad', '')


            # Prepare the email content for the owner
            subject = f'Contact Form Submission from {name}'
            body = f'Message from {name} ({email}):\n\n Company: {company}\n\n Zone: {zone}\n\n Consiente aviso legal: {avisolegal}\n\n Consiente publicidad: {publicidad}\n\n Message: {content}'

                # Send email to the site owner
            try:
                send_mail(
                    subject,
                    body,
                    'no-reply@axxyss.com',
                    #settings.EMAIL_HOST_USER,
                    [settings.DEFAULT_FROM_EMAIL],
                )

                
                # Prepare the email content for the sender
                subject = f'Copy of Your Message to axxyss.com'
                sender_body = f'Thank you for your message! Here is a copy of what you sent:\n\n' + body

                # Send a copy to the sender
                send_mail(
                    subject,
                    sender_body,
                    'no-reply@axxyss.com',
                    #settings.EMAIL_HOST_USER,
                    [email],  # Sender's email
                )

                return render(request, 'contact/success.html')
            except Exception as e:
                print(f"Error sending email: {e}")
                form.add_error(None, "There was an error sending your message. Please try again later.")
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})