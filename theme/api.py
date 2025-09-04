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


@frappe.whitelist(allow_guest=True)
def submit_contact_form(name, email, subject, message, subscribe=False):
    """Send contact form submission via email only"""
    
    # Send email notification
    frappe.sendmail(
        recipients=["simomutu8@gmail.com"],  # Replace with your email
        subject=f"New Contact Form Submission: {subject or 'No Subject'}",
        message=f"""
            <h2>New Contact Form Submission</h2>
            <p>You have received a new contact form submission:</p>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
            <p><strong>Subscribed to newsletter:</strong> {'Yes' if subscribe else 'No'}</p>
        """,
        delayed=False
    )
    
    # Add to email group if subscribed
    if subscribe:
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

    return "success"






@frappe.whitelist(allow_guest=True)
def submit_demo_request(full_name, company, email, phone=None, job_title=None, industry=None, solutions=None, message=None, subscribe=False):
    """Process demo request form submission and send to email only"""
    
    # Format solutions as a string if it's a list
    if isinstance(solutions, list):
        solutions_str = ", ".join(solutions)
    else:
        solutions_str = str(solutions) if solutions else "Not specified"
    
    # Send notification email
    email_subject = f"New Demo Request: {company} ({full_name})"
    
    email_body = f"""
    <h2>New Demo Request Received</h2>
    
    <h3>Contact Information</h3>
    <p><strong>Name:</strong> {full_name}</p>
    <p><strong>Company:</strong> {company}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Phone:</strong> {phone or 'Not provided'}</p>
    <p><strong>Job Title:</strong> {job_title or 'Not provided'}</p>
    <p><strong>Industry:</strong> {industry or 'Not provided'}</p>
    
    <h3>Solutions Interested In</h3>
    <p>{solutions_str}</p>
    
    <h3>Additional Message</h3>
    <p>{message or 'No additional message'}</p>
    
    <p><strong>Subscribed to newsletter:</strong> {'Yes' if subscribe else 'No'}</p>
    
    <p>This demo request was submitted through the website form.</p>
    """
    
    # Send email to your address
    frappe.sendmail(
        recipients=["simomutu8@gmail.com"],  # Replace with your email
        subject=email_subject,
        message=email_body,
        delayed=False
    )
    
    # Send confirmation email to the requester
    if email:
        user_subject = "Thank you for your demo request - LedgerCtrl"
        
        user_message = f"""
        <p>Dear {full_name},</p>
        
        <p>Thank you for requesting a demo of LedgerCtrl. We've received your request with the following details:</p>
        
        <p><strong>Company:</strong> {company}</p>
        <p><strong>Interested In:</strong> {solutions_str}</p>
        
        <p>Our team will review your request and contact you within 24 hours to schedule your demo at a time that's convenient for you.</p>
        
        <p>If you have any immediate questions, feel free to reply to this email or call us.</p>
        
        <p>Best regards,<br>
        The LedgerCtrl Team</p>
        """
        
        frappe.sendmail(
            recipients=[email],
            subject=user_subject,
            message=user_message,
            now=True
        )
    
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