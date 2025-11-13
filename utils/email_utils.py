from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

def send_templated_email(subject, template_name, context, recipient_list):
    """
    Send HTML + text fallback email using templates/emails/.
    """
    context['year'] = timezone.now().year
    html_content = render_to_string(f"emails/{template_name}.html", context)
    text_content = render_to_string(f"emails/{template_name}.txt", context)

    msg = EmailMultiAlternatives(
        subject,
        text_content,
        "noreply@afrilingua.com",
        recipient_list
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
