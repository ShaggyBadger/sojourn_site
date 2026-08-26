from django import forms
from django.utils.translation import gettext_lazy as _


class SubscribeForm(forms.Form):
    """Public form for joining the church email list."""

    email = forms.EmailField(
        label=_("Email address"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                "autocomplete": "email",
                "class": "form-control form-control-lg",
                "placeholder": "you@example.com",
            }
        ),
    )
    first_name = forms.CharField(
        label=_("First name"),
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "given-name",
                "class": "form-control form-control-lg",
            }
        ),
    )
    last_name = forms.CharField(
        label=_("Last name"),
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "family-name",
                "class": "form-control form-control-lg",
            }
        ),
    )
    consent = forms.BooleanField(
        label=_("I agree to receive church communications by email."),
        required=True,
    )
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "autocomplete": "off",
                "class": "d-none",
                "tabindex": "-1",
                "aria-hidden": "true",
            }
        ),
    )

    def clean_email(self):
        """Use the same normalized value stored by EmailRecipient."""
        return self.cleaned_data["email"].strip().casefold()


class TemplatePreviewForm(forms.Form):
    """Structured context used to preview or test a weekly meeting template."""

    meeting_date = forms.CharField(label=_("Meeting date"), max_length=100)
    meeting_time = forms.CharField(label=_("Meeting time"), max_length=100)
    meeting_location = forms.CharField(label=_("Meeting location"), max_length=255)
    first_name = forms.CharField(
        label=_("Sample first name"), max_length=100, required=False
    )
    body = forms.CharField(
        label=_("Announcements"), required=False, widget=forms.Textarea
    )
    notes = forms.CharField(label=_("Notes"), required=False, widget=forms.Textarea)
    test_email = forms.EmailField(label=_("Test email address"), required=False)
