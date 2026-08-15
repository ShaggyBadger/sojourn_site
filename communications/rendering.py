import html
import re

from django.conf import settings
from django.urls import reverse

from core.models import SiteSettings

from .models import EmailRecipient, EmailTemplate

VARIABLE_PATTERN = re.compile(r"{{\s*([a-z_][a-z0-9_]*)\s*}}")
ALLOWED_VARIABLES = {
    "body",
    "first_name",
    "meeting_date",
    "meeting_location",
    "meeting_time",
    "notes",
    "unsubscribe_url",
}
REQUIRED_CONTEXT = {"meeting_date", "meeting_time", "meeting_location"}


class TemplateRenderError(ValueError):
    """Raised when a controlled email template cannot be rendered safely."""


def _template_variables(value):
    if value.count("{{") != value.count("}}"):
        raise TemplateRenderError("Template contains an incomplete variable.")
    return set(match.group(1) for match in VARIABLE_PATTERN.finditer(value))


def _render_value(value, context, *, escape_html=False):
    variables = _template_variables(value)
    unknown = variables - ALLOWED_VARIABLES
    if unknown:
        names = ", ".join(sorted(unknown))
        raise TemplateRenderError(f"Unknown template variable(s): {names}.")

    def replace(match):
        rendered = str(context.get(match.group(1), ""))
        return html.escape(rendered) if escape_html else rendered

    return VARIABLE_PATTERN.sub(replace, value)


def _paragraphs(value):
    return [paragraph.strip() for paragraph in value.split("\n\n") if paragraph.strip()]


def unsubscribe_url_for(recipient):
    """Return the absolute unsubscribe URL included in future messages."""
    path = reverse(
        "communications:unsubscribe",
        kwargs={"token": recipient.unsubscribe_token},
    )
    return f"{settings.PUBLIC_SITE_URL.rstrip('/')}{path}"


def render_email_template(template, context, *, recipient=None, unsubscribe_url=None):
    """Render one controlled template as subject, HTML, and plain text."""
    context = dict(context)
    if recipient is not None:
        context.setdefault("first_name", recipient.first_name)
        context.setdefault("unsubscribe_url", unsubscribe_url_for(recipient))
    if unsubscribe_url is not None:
        context["unsubscribe_url"] = unsubscribe_url

    missing = sorted(field for field in REQUIRED_CONTEXT if not context.get(field))
    if missing:
        raise TemplateRenderError(
            "Missing required context: " + ", ".join(missing) + "."
        )
    if not context.get("unsubscribe_url"):
        raise TemplateRenderError("Missing required context: unsubscribe_url.")

    subject = _render_value(template.subject_template, context).strip()
    greeting = _render_value(template.greeting, context, escape_html=True)
    standard_copy = _render_value(template.standard_copy, context, escape_html=True)
    closing = _render_value(template.closing, context, escape_html=True)
    location = html.escape(str(context["meeting_location"]))
    meeting_date = html.escape(str(context["meeting_date"]))
    meeting_time = html.escape(str(context["meeting_time"]))
    notes = _render_value(str(context.get("notes", "")), context, escape_html=True)
    body = _render_value(str(context.get("body", "")), context, escape_html=True)
    unsubscribe_url = html.escape(str(context["unsubscribe_url"]), quote=True)

    site_settings = SiteSettings.objects.first()
    hero_image = ""
    hero_image_alt = "Sojourn Baptist Church"
    if site_settings and site_settings.hero_image:
        hero_image = html.escape(site_settings.hero_image.url, quote=True)
        hero_image_alt = html.escape(
            site_settings.hero_image_alt or "Sojourn Baptist Church",
            quote=True,
        )

    image_block = ""
    if hero_image:
        image_block = f"""
            <tr><td style="padding:0;background:#141416;">
              <img src="{hero_image}" alt="{hero_image_alt}" width="620"
                style="display:block;width:100%;height:auto;border:0;">
            </td></tr>"""

    content_blocks = []
    for block in (standard_copy, body, notes):
        if block.strip():
            content_blocks.append(
                f'<p style="margin:0 0 20px;">{block.replace(chr(10), "<br>")}</p>'
            )
    content_html = "".join(content_blocks)
    html_body = f"""<!doctype html>
<html lang="en">
  <body style="margin:0;background:#f4f1ea;color:#141416;font-family:Arial,sans-serif;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background:#f4f1ea;">
      <tr><td align="center" style="padding:28px 12px;">
        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width:620px;background:#ffffff;">
          <tr><td style="background:#581827;color:#f4f1ea;padding:28px 32px;font-size:22px;font-weight:bold;">Sojourn Baptist Church</td></tr>
          {image_block}
          <tr><td style="padding:32px;">
            <p style="margin:0 0 20px;font-size:18px;">{greeting}</p>
            {content_html}
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="margin:24px 0;background:#f4f1ea;border-left:4px solid #c5a880;">
              <tr><td style="padding:16px 18px;"><strong>Meeting details</strong><br>
                <span style="color:#444;">{meeting_date}<br>{meeting_time}<br>{location}</span>
              </td></tr>
            </table>
            <p style="margin:0;white-space:pre-line;">{closing.replace(chr(10), "<br>")}</p>
          </td></tr>
          <tr><td style="padding:20px 32px;background:#141416;color:#f4f1ea;font-size:12px;">
            Sojourn Baptist Church<br>
            <a href="{unsubscribe_url}" style="color:#c5a880;">Unsubscribe from future emails</a>
          </td></tr>
        </table>
      </td></tr>
    </table>
  </body>
</html>"""

    text_parts = [
        greeting.replace("<br>", "\n"),
        *[part for part in (standard_copy, body, notes) if part.strip()],
        "Meeting details:",
        str(context["meeting_date"]),
        str(context["meeting_time"]),
        str(context["meeting_location"]),
        closing,
        f"Unsubscribe: {context['unsubscribe_url']}",
    ]
    return {
        "subject": subject,
        "html": html_body,
        "text": "\n\n".join(text_parts),
    }
