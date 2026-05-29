import frappe
from frappe.utils import get_datetime


def is_email_content_empty(content: str | None) -> bool:
    return content is None or content.strip() == ""


def get_default_email_content(type: str) -> str:
    if type == "share_feedback":
        return """\
<div style="font-family: -apple-system, BlinkMacSystemFont, ‘Segoe UI’, Roboto, sans-serif; max-width: 600px; margin: 0 auto; color: #1f2937;">
  <p style="margin: 0 0 16px;">Hello,</p>
  <p style="margin: 0 0 20px;">Thanks for reaching out to us. We’d love your feedback on your recent support experience with ticket <strong>#{{ doc.name }}</strong>.{% if doc.custom_project %} (Project: {{ doc.custom_project }}){% endif %}</p>
  <p style="margin: 0 0 24px;">
    <a href="{{ url }}" style="display: inline-block; padding: 10px 20px; background-color: #171717; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: 500;">Share Feedback</a>
  </p>
  <p style="margin: 0;">Thank you!<br />Support Team</p>
</div>"""

    if type == "acknowledgement":
        return """\
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; color: #1f2937;">
  <p style="margin: 0 0 16px;">Hi,</p>
  <p style="margin: 0 0 16px;">Thank you for reaching out to us. We've received your request and created a support ticket.</p>
  <table style="margin: 0 0 16px; border-collapse: collapse;">
    <tr><td style="padding: 4px 8px 4px 0; font-weight: 600;">Ticket ID:</td><td style="padding: 4px 0;">{{ doc.name }}</td></tr>
    <tr><td style="padding: 4px 8px 4px 0; font-weight: 600;">Subject:</td><td style="padding: 4px 0;">{{ doc.subject }}</td></tr>
    {% if doc.custom_project %}<tr><td style="padding: 4px 8px 4px 0; font-weight: 600;">Project:</td><td style="padding: 4px 0;">{{ doc.custom_project }}</td></tr>{% endif %}
  </table>
  <p style="margin: 0 0 16px;">Our team is reviewing it and will get back to you shortly.</p>
  {% if ticket_url %}
  <p style="margin: 0 0 24px;">
    <a href="{{ ticket_url }}" style="display: inline-block; padding: 10px 20px; background-color: #171717; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: 500;">View Ticket</a>
  </p>
  {% endif %}
  <p style="margin: 0;">Best,<br />Support Team</p>
</div>
"""

    if type == "reply_to_agents":
        return """\
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; color: #1f2937;">
  <p style="margin: 0 0 16px;">Hello,</p>
  <p style="margin: 0 0 16px;">You have a new reply on ticket <strong>#{{ doc.name }}</strong>.</p>
  <table style="margin: 0 0 16px; border-collapse: collapse;">
    <tr><td style="padding: 4px 8px 4px 0; font-weight: 600;">Subject:</td><td style="padding: 4px 0;">{{ doc.subject }}</td></tr>
    <tr><td style="padding: 4px 8px 4px 0; font-weight: 600;">Raised By:</td><td style="padding: 4px 0;">{{ doc.raised_by }}</td></tr>
    <tr><td style="padding: 4px 8px 4px 0; font-weight: 600;">Priority:</td><td style="padding: 4px 0;">{{ doc.priority }}</td></tr>
    {% if doc.custom_project %}<tr><td style="padding: 4px 8px 4px 0; font-weight: 600;">Project:</td><td style="padding: 4px 0;">{{ doc.custom_project }}</td></tr>{% endif %}
  </table>
  <p style="margin: 0 0 24px;">
    <a href="{{ ticket_url }}" style="display: inline-block; padding: 10px 20px; background-color: #171717; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: 500;">View Ticket</a>
  </p>
  <p style="margin: 0;">Regards,<br />Support Team</p>
</div>
"""

    if type == "reply_via_agent":
        return """\
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 600px; margin: 0 auto; color: #1f2937;">
  <h2 style="margin: 0 0 8px; font-size: 18px;"><strong>Ticket #{{ doc.name }}</strong></h2>
  {% if doc.custom_project %}<p style="margin: 0 0 8px; color: #6b7280;">Project: {{ doc.custom_project }}</p>{% endif %}
  <p style="margin: 0 0 16px; color: #6b7280;">You have a new reply on this ticket</p>
  <div style="margin: 0 0 20px;">
    <p style="margin: 0 0 8px; font-weight: 600;">Message</p>
    <div style="background: #f9fafb; padding: 16px; border-radius: 8px; border: 1px solid #e5e7eb; line-height: 1.6;">
      {{ message }}
    </div>
  </div>
  <p style="margin: 0 0 16px;">Please visit the customer portal to reply to this message.</p>
  <p style="margin: 0 0 24px;">
    <a href="{{ ticket_url }}" style="display: inline-block; padding: 10px 20px; background-color: #171717; color: #ffffff; text-decoration: none; border-radius: 6px; font-weight: 500;" rel="noopener noreferrer" target="_blank">View Ticket</a>
  </p>
</div>
"""


default_banner_msg = """Thanks for reaching out 👋. This ticket was created outside our working hours. You can expect the next response by {{ next_working_day }}."""


@frappe.whitelist()
def get_banner_msg():
    """Get current and default banner message for settings UI"""

    current_msg = frappe.db.get_single_value(
        "HD Settings", "outside_working_hours_message"
    )
    enabled = frappe.db.get_single_value("HD Settings", "enable_outside_hours_banner")

    return {
        "default": default_banner_msg,
        "current": current_msg or None,
        "enabled": bool(enabled),
    }


def get_rendered_banner_msg(ticket_id):
    banner_msg = frappe.db.get_single_value(
        "HD Settings", "outside_working_hours_message"
    )
    ticket = frappe.get_doc("HD Ticket", ticket_id).as_dict()
    if not banner_msg:
        banner_msg = default_banner_msg

    next_working_day = None
    next_working_date = None
    expected_response = None

    if ticket.get("response_by"):
        next_working_day_dt = get_datetime(ticket.get("response_by"))
        next_working_day = next_working_day_dt.strftime("%A, %d %b")
        next_working_date = next_working_day_dt.strftime("%d %b")
        expected_response = next_working_day_dt.strftime("%H:%M, %A, %d %b")

    context = {
        "ticket": ticket,
        "next_working_daytime": next_working_day_dt,
        "next_working_day": next_working_day,
        "next_working_date": next_working_date,
        "expected_response": expected_response,
    }

    rendered = frappe.render_template(banner_msg, context)

    return {
        "banner_msg": rendered,
    }
