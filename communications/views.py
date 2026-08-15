import hashlib

from django.core.cache import cache
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .forms import SubscribeForm, TemplatePreviewForm
from .models import EmailRecipient, EmailTemplate
from .rendering import TemplateRenderError, render_email_template
from .services import subscribe_recipient

SIGNUP_LIMIT = 5
SIGNUP_WINDOW_SECONDS = 60 * 60


def _signup_throttle_key(request):
    """Hash the client address before using it as a cache key."""
    address = request.META.get("REMOTE_ADDR", "unknown")
    digest = hashlib.sha256(address.encode("utf-8")).hexdigest()
    return f"communications:public-signup:{digest}"


def _is_rate_limited(request):
    key = _signup_throttle_key(request)
    if cache.add(key, 1, SIGNUP_WINDOW_SECONDS):
        return False
    try:
        count = cache.incr(key)
    except ValueError:
        return False
    return count > SIGNUP_LIMIT


def subscribe(request):
    """Collect a visitor's email without revealing duplicate membership."""
    form = SubscribeForm(request.POST if request.method == "POST" else None)
    submitted = False

    if request.method == "POST" and form.is_valid():
        submitted = True
        if not _is_rate_limited(request) and not form.cleaned_data["website"]:
            subscribe_recipient(
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"].strip(),
                last_name=form.cleaned_data["last_name"].strip(),
            )
        form = SubscribeForm()

    return render(
        request,
        "communications/subscribe.html",
        {"form": form, "submitted": submitted},
    )


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
