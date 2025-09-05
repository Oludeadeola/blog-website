import re
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator as BaseEmailValidator
from django.utils.translation import gettext_lazy as _
from auths.models import User

PASSWORD_REGEX_FORMAT = "^(?=.*[!@#$%^&*(),.?\":{}|<>])(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
VALID_PASSWORD_FORMAT = """
It Must Contain At Least One Special Character
It Must Contain At Least One Uppercase Alphabet
It Must Contain At Least One Lowercase Alphabet
It Must Contain At Least One Digit
"""
class CustomPasswordValidator:
    help_text = _(
        "Password must match the format given\n {format}" % {"format": VALID_PASSWORD_FORMAT}
    )

    def validate(self, password, user: User = None) -> None:
        if not re.match(PASSWORD_REGEX_FORMAT, password):
            raise ValidationError(message="The "+self.help_text, code="invalid_format")

    def get_help_text(self):
        return "Your "+self.help_text

class EmailValidator(BaseEmailValidator):
    message = _("Your Email Did Not Match A Valid Email Format")
    domain_allowlist = []
