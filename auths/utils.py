from django.core.mail import EmailMultiAlternatives
from django.template import Template
from django.template.loader import get_template

PASSWORD = "password"

EMAIL = "email"

def TOKEN_CREATE_AUTHENTICATION_FAILED_FOR_USER(email, password) -> str:
    return f"""Authentication Failed, Either Because The User With Email {email} and Password {password} Does Not Exist Or They Are Not Allowed To Make This Request"""

def send_registration_successful_mail(to: list, name: str, subject: str, template=None):
    msg: EmailMultiAlternatives = EmailMultiAlternatives(subject=subject, to=to)
    msg.attach_alternative(content=template_loader(template=template, var_dict={'name': name}), mimetype='text/html')
    msg.send()
    print('Message Sent Successfully')

def template_loader(template=None, var_dict: dict = None):
    context = var_dict
    template: Template = get_template(template)
    html_content = template.render(context=context)
    return html_content
