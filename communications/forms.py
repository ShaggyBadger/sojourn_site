from django import forms
from django.utils.translation import gettext_lazy as _


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
