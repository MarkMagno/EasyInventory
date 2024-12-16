from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from inventory.models import UserProfile

class Command(BaseCommand):
    help = 'Create a superuser and automatically assign a UserProfile with role admin.'

    def handle(self, *args, **options):
        # Define a signal handler to create UserProfile after User is saved
        def create_userprofile(sender, instance, created, **kwargs):
            if created and instance.is_superuser and not UserProfile.objects.filter(user=instance).exists():
                UserProfile.objects.create(user=instance, role='admin')
                self.stdout.write(self.style.SUCCESS(f"UserProfile assigned to superuser '{instance.username}' with role 'admin'"))

        # Connect the signal
        post_save.connect(create_userprofile, sender=User)

        # Call the base superuser creation command
        super().handle(*args, **options)

        # Disconnect the signal to avoid unwanted behavior
        post_save.disconnect(create_userprofile, sender=User)
