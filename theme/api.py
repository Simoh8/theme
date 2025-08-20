from __future__ import unicode_literals
import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def subscribe_newsletter(email):
    """Subscribe email to newsletter"""
    if not frappe.db.exists("Email Group", _("Website")):
        email_group = frappe.get_doc({
            "doctype": "Email Group",
            "title": _("Website")
        })
        email_group.insert(ignore_permissions=True)
    
    if not frappe.db.exists("Email Group Member", {"email": email, "email_group": _("Website")}):
        subscriber = frappe.get_doc({
            "doctype": "Email Group Member",
            "email": email,
            "email_group": _("Website")
        })
        subscriber.insert(ignore_permissions=True)
        
        # You might want to send a confirmation email here
        # send_confirmation_email(email)
        
    return "success"

import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def submit_contact_form(name, email, subject, message):
    """Send contact form submission via email only"""
    
    # Send email notification
    frappe.throw("simpon is using the contact form ")
    frappe.sendmail(
        recipients=["simomutu8@gmail.com"],
        subject=f"New Contact Form Submission: {subject or 'No Subject'}",
        message=f"""
            <p>You have received a new contact form submission:</p>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
        """,
        delayed=False
    )

    return "success"


@frappe.whitelist(allow_guest=True)
def submit_demo_request(data):
    """Process demo request form submission"""
    # Create a new Lead
    lead = frappe.get_doc({
        "doctype": "Lead",
        "lead_name": data.get('full_name'),
        "company_name": data.get('company'),
        "email_id": data.get('email'),
        "phone": data.get('phone'),
        "job_title": data.get('job_title'),
        "industry": data.get('industry'),
        "notes": f"Solutions Interested In: {data.get('solutions', '')}\n\nMessage: {data.get('message', '')}",
        "source": "Website Demo Request",
        "status": "Lead"
    })
    lead.insert(ignore_permissions=True)
    
    # Create Opportunity if applicable
    opportunity = frappe.get_doc({
        "doctype": "Opportunity",
        "opportunity_from": "Lead",
        "party_name": lead.name,
        "contact_email": data.get('email'),
        "opportunity_type": "Demo Request",
        "with_items": 0,
        "transaction_date": frappe.utils.nowdate(),
        "status": "Demo Scheduled"
    })
    opportunity.insert(ignore_permissions=True)
    
    # Add to email group if subscribed
    if data.get('subscribe') == 'Yes':
        if not frappe.db.exists("Email Group", _("Website")):
            email_group = frappe.get_doc({
                "doctype": "Email Group",
                "title": _("Website")
            })
            email_group.insert(ignore_permissions=True)
        
        if not frappe.db.exists("Email Group Member", {"email": data.get('email'), "email_group": _("Website")}):
            subscriber = frappe.get_doc({
                "doctype": "Email Group Member",
                "email": data.get('email'),
                "email_group": _("Website")
            })
            subscriber.insert(ignore_permissions=True)
    
    # Send notification emails
    send_demo_request_notification(data, lead.name, opportunity.name)
    
    return "success"

def send_demo_request_notification(data, lead_name, opportunity_name):
    """Send notification emails about the demo request"""
    # Email to admin/sales team
    admin_subject = f"New Demo Request: {data.get('company')} ({data.get('full_name')})"
    
    admin_message = f"""
    <p>A new demo request has been submitted through the website:</p>
    
    <p><strong>Lead:</strong> <a href="{frappe.utils.get_url_to_form('Lead', lead_name)}">{lead_name}</a></p>
    <p><strong>Opportunity:</strong> <a href="{frappe.utils.get_url_to_form('Opportunity', opportunity_name)}">{opportunity_name}</a></p>
    
    <h3>Contact Information</h3>
    <p><strong>Name:</strong> {data.get('full_name')}</p>
    <p><strong>Company:</strong> {data.get('company')}</p>
    <p><strong>Email:</strong> {data.get('email')}</p>
    <p><strong>Phone:</strong> {data.get('phone') or 'Not provided'}</p>
    <p><strong>Job Title:</strong> {data.get('job_title') or 'Not provided'}</p>
    <p><strong>Industry:</strong> {data.get('industry') or 'Not provided'}</p>
    
    <h3>Interested In</h3>
    <p>{data.get('solutions') or 'Not specified'}</p>
    
    <h3>Additional Message</h3>
    <p>{data.get('message') or 'No additional message'}</p>
    
    <p><strong>Subscribed to newsletter:</strong> {data.get('subscribe')}</p>
    """
    
    frappe.sendmail(
        recipients=["sales@ledgerctrl.com"],
        subject=admin_subject,
        message=admin_message
    )
    
    # Confirmation email to the requester
    if data.get('email'):
        user_subject = "Thank you for your demo request - LedgerCtrl"
        
        user_message = f"""
        <p>Dear {data.get('full_name')},</p>
        
        <p>Thank you for requesting a demo of LedgerCtrl. We've received your request with the following details:</p>
        
        <p><strong>Company:</strong> {data.get('company')}</p>
        <p><strong>Interested In:</strong> {data.get('solutions') or 'Not specified'}</p>
        
        <p>Our sales team will review your request and contact you within 24 hours to schedule your demo at a time that's convenient for you.</p>
        
        <p>If you have any immediate questions, feel free to reply to this email or call us at +1 (555) 123-4567.</p>
        
        <p>Best regards,<br>
        The LedgerCtrl Team</p>
        """
        
        frappe.sendmail(
            recipients=[data.get('email')],
            subject=user_subject,
            message=user_message,
            now=True
        )