from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = "Create a superuser with additional fields"

    def handle(self, *args, **options):

        options["first_name"] = input("First Name: ")
        options["last_name"] = input("Last Name: ")
        options["username"] = input("User Name: ")
        options["email"] = input("Email: ")

        try:
            super().handle(*args, **options)
        except CommandError as error:
            self.stderr.write(self.style.ERROR("Superuser creation failed."))
