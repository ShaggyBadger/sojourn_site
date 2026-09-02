from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .forms import TemplatePreviewForm
from .models import EmailRecipient, EmailTemplate
from .rendering import TemplateRenderError, render_email_template

def subscribe(request):
    """Render the Zoho Campaigns signup form."""
    return render(request, "communications/subscribe.html")


def subscribe_confirmed(request):
    """Render the site-native destination for a confirmed Zoho subscription."""
    return render(request, "communications/subscribe_confirmed.html")


def unsubscribe(request, token):
    """Show and apply an idempotent unsubscribe request."""
    recipient = get_object_or_404(EmailRecipient, unsubscribe_token=token)
    if request.method == "POST":
        if recipient.status == EmailRecipient.Status.ACTIVE:
            recipient.status = EmailRecipient.Status.UNSUBSCRIBED
            recipient.unsubscribed_at = timezone.now()
            recipient.save(update_fields=("status", "unsubscribed_at", "updated_at"))
        return render(
            request,
            "communications/unsubscribe.html",
            {"unsubscribed": True},
        )
    return render(
        request,
        "communications/unsubscribe.html",
        {"unsubscribed": False},
    )


@staff_member_required
def template_preview(request, template_id):
    """Preview or send a controlled template to one explicit test address."""
    template = get_object_or_404(EmailTemplate, pk=template_id)
    initial = {
        "meeting_date": "Sunday, September 6",
        "meeting_time": "10:30 AM",
        "meeting_location": "Sojourn Baptist Church",
        "first_name": "Friend",
    }
    form = TemplatePreviewForm(
        request.POST if request.method == "POST" else None,
        initial=initial if request.method == "GET" else None,
    )
    rendered = None
    if request.method == "POST" and form.is_valid():
        context = {
            key: form.cleaned_data[key]
            for key in (
                "meeting_date",
                "meeting_time",
                "meeting_location",
                "first_name",
                "body",
                "notes",
            )
        }
        test_email = form.cleaned_data["test_email"]
        if request.POST.get("send_test") and not test_email:
            form.add_error(
                "test_email", _("Enter a test email address before sending.")
            )
        else:
            try:
                rendered = render_email_template(
                    template,
                    context,
                    unsubscribe_url=f"{settings.PUBLIC_SITE_URL.rstrip('/')}/unsubscribe/test/",
                )
            except TemplateRenderError as error:
                form.add_error(None, str(error))

        if rendered and request.POST.get("send_test") and test_email:
            message = EmailMultiAlternatives(
                subject=rendered["subject"],
                body=rendered["text"],
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[test_email],
            )
            message.attach_alternative(rendered["html"], "text/html")
            message.send()
            messages.success(request, _("The test email was sent."))
    return render(
        request,
        "communications/template_preview.html",
        {"form": form, "email_template": template, "rendered": rendered},
    )
